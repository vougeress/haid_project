import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')
if not TMDB_ACCESS_TOKEN:
    raise ValueError("TMDB_ACCESS_TOKEN не найден в .env файле")

print(f"TMDB_ACCESS_TOKEN: {TMDB_ACCESS_TOKEN[:10]}...") # Показываем только первые 10 символов для безопасности
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
# Загрузка модели эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_or_create_embeddings():
    # Путь к файлу с сохраненными эмбеддингами
    embeddings_file = "movie_embeddings.npy"
    data_file = "movie_data.csv"
    
    if os.path.exists(embeddings_file) and os.path.exists(data_file):
        print("Загрузка существующих эмбеддингов...")
        embeddings = np.load(embeddings_file)
        df = pd.read_csv(data_file)
        df['embedding'] = list(embeddings)
    else:
        print("Создание новых эмбеддингов...")
        # Загрузка данных
        df = pd.read_csv("tmdb_5000_movies.csv")
        # Сохраняем нужные столбцы
        df = df[['id', 'title', 'overview', 'genres', 'release_date']].dropna()
        
        # Создание эмбеддингов для всех описаний фильмов
        print("Создание эмбеддингов фильмов...")
        embeddings = df['overview'].apply(lambda x: model.encode(x, show_progress_bar=False))
        df['embedding'] = embeddings
        
        # Сохранение эмбеддингов и данных
        np.save(embeddings_file, np.array(embeddings.tolist()))
        df.to_csv(data_file, index=False)
    
    return df

# Загрузка или создание эмбеддингов
df = load_or_create_embeddings()

def recommend_movies(user_input, top_k=10):
    print("Обработка ввода пользователя...")
    user_embedding = model.encode(user_input)
    similarities = df['embedding'].apply(lambda x: cosine_similarity([user_embedding], [x])[0][0])
    df['similarity'] = similarities
    recommendations = df.sort_values('similarity', ascending=False).head(top_k)
    
    # Добавляем URL постеров для каждого фильма
    recommendations['poster_url'] = recommendations['id'].apply(get_movie_poster)
    
    return recommendations[['id', 'title', 'overview', 'genres', 'release_date', 'poster_url']]

def get_movie_poster(movie_id):
    """Получение постера фильма из TMDB по ID"""
    try:
        # Получаем информацию о фильме по ID
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
        headers = {
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
            "accept": "application/json"
        }
        
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        movie_data = response.json()
        
        # Получаем путь к постеру из массива posters
        if movie_data.get("posters") and len(movie_data["posters"]) > 0:
            poster_path = movie_data["posters"][0]["file_path"]
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
            
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при получении постера для фильма {movie_id}: {str(e)}")
        return "https://via.placeholder.com/500x750?text=Network+Error"
    except Exception as e:
        print(f"Ошибка при получении постера для фильма {movie_id}: {str(e)}")
        return "https://via.placeholder.com/500x750?text=Error+Loading+Poster"

# Тестовый код
if __name__ == "__main__":
    user_mood = "I want to watch a movie about a girl who is a detective"
    recommendations = recommend_movies(user_mood)
    print("\n🎬 Рекомендованные фильмы:")
    for i, row in recommendations.iterrows():
        print(f"\n🎥 {row['title']}\n{row['overview']}")