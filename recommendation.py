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
    data_file = "movies_metadata.csv"
    
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
        df = df[['id', 'original_title', 'overview', 'genres']].dropna()
        
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

def recommend_movies(user_input, top_k=12):
    print("Обработка ввода пользователя...")
    user_embedding = model.encode(user_input)
    similarities = df['embedding'].apply(lambda x: cosine_similarity([user_embedding], [x])[0][0])
    df['similarity'] = similarities
    recommendations = df.sort_values('similarity', ascending=False).head(top_k)
    
    # Добавляем URL постеров и год выпуска для каждого фильма
    movie_data = recommendations['id'].apply(get_movie_poster)
    recommendations['poster_path'] = movie_data.apply(lambda x: x['poster_path'])
    recommendations['release_year'] = movie_data.apply(lambda x: x['release_year'])
    
    return recommendations[['id', 'original_title', 'overview', 'genres', 'release_year', 'poster_path']]

def get_movie_poster(movie_id):
    """Получение постера фильма и года выпуска из TMDB по ID"""
    try:
        # Получаем информацию о фильме по ID
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
            "accept": "application/json"
        }
        
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        movie_data = response.json()
        
        # Получаем путь к постеру и год выпуска
        poster_url = "https://via.placeholder.com/500x750?text=No+Poster+Available"
        if movie_data.get("poster_path"):
            poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_data['poster_path']}"
            
        # Получаем год из release_date
        release_year = None
        if movie_data.get("release_date"):
            release_year = movie_data["release_date"][:4]  # Берем первые 4 символа (год)
            
        return {
            "poster_path": poster_url,
            "release_year": release_year
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при получении данных для фильма {movie_id}: {str(e)}")
        return {
            "poster_path": "https://via.placeholder.com/500x750?text=Network+Error",
            "release_year": None
        }
    except Exception as e:
        print(f"Ошибка при получении данных для фильма {movie_id}: {str(e)}")
        return {
            "poster_url": "https://via.placeholder.com/500x750?text=Error+Loading+Poster",
            "release_year": None
        }

# Тестовый код
if __name__ == "__main__":
    user_mood = "I want to watch a movie about a girl who is a detective"
    recommendations = recommend_movies(user_mood)
    print("\n🎬 Рекомендованные фильмы:")
    for i, row in recommendations.iterrows():
        print(f"\n🎥 {row['original_title']}\n{row['overview']}")