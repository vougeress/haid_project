import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

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
    return df.sort_values('similarity', ascending=False).head(top_k)[['id', 'title', 'overview', 'genres', 'release_date']]

# Тестовый код
if __name__ == "__main__":
    user_mood = "I want to watch a movie about a girl who is a detective"
    recommendations = recommend_movies(user_mood)
    print("\n🎬 Рекомендованные фильмы:")
    for i, row in recommendations.iterrows():
        print(f"\n🎥 {row['title']}\n{row['overview']}")