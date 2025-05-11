import uuid
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
from dotenv import load_dotenv
from gigachat import GigaChat
import json
import base64



load_dotenv()
TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN')
load_dotenv()
GIGACHAT_TOKEN = os.getenv('GIGA_ACCESS_TOKEN')

if not TMDB_ACCESS_TOKEN:
    raise ValueError("TMDB_ACCESS_TOKEN not found in .env file")

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
# Loading embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

if not GIGACHAT_TOKEN:
    raise ValueError("GIGACHAT_TOKEN not found in .env file")

def load_or_create_embeddings():
    # Path to saved embeddings file
    embeddings_file = "movie_embeddings.npy"
    data_file = "movies_metadata.csv"
    
    if os.path.exists(embeddings_file) and os.path.exists(data_file):
        print("Loading existing embeddings...")
        embeddings = np.load(embeddings_file)
        df = pd.read_csv(data_file)
        df['embedding'] = list(embeddings)
    else:
        print("Creating new embeddings...")
        # Loading data
        df = pd.read_csv("tmdb_5000_movies.csv")
        # Save required columns
        df = df[['id', 'original_title', 'overview', 'genres']].dropna()
        
        # Creating embeddings for all movie descriptions
        print("Creating movie embeddings...")
        embeddings = df['overview'].apply(lambda x: model.encode(x, show_progress_bar=False))
        df['embedding'] = embeddings
        
        # Saving embeddings and data
        np.save(embeddings_file, np.array(embeddings.tolist()))
        df.to_csv(data_file, index=False)
    
    return df

# Loading or creating embeddings
df = load_or_create_embeddings()



def generate_explanation(user_input, movie_title, movie_overview, similarity):
    """Generates explanation using GigaChat API"""
    try:
        # Get token through get_gigachat_token
        
        # Initialize GigaChat with proper authorization
        giga = GigaChat(
            credentials=GIGACHAT_TOKEN,
            verify_ssl_certs=False,
            scope="GIGACHAT_API_PERS"
        )
        
        # Form prompt
        prompt = f"""
Write a short explanation (maximum 100 words) describing why this movie is a great match for the query: "{user_input}".
Movie description: {movie_overview}
Do not repeat the movie title or retell the plot. Instead, provide a thoughtful, conversational explanation that clearly highlights the key reasons—such as themes, atmosphere, or emotional tone—that make it a strong fit. 
Imagine you're recommending it to a friend and want them to see why it matches their interest, try to use not complex language.
"""
        
        # Get response from GigaChat
        response = giga.chat(prompt)
        explanation = response.choices[0].message.content
        
        # If explanation is too long, truncate it
        if len(explanation) > 10000:
            explanation = explanation[:10000] + "..."
            
        return explanation
        
    except Exception as e:
        print(f"Error generating explanation: {str(e)}")
        # Return more informative base explanation
        if similarity > 0.8:
            return f"This movie perfectly matches your request due to its plot and themes."
        elif similarity > 0.6:
            return f"This movie well matches your request and might interest you."
        else:
            return f"This movie partially matches your request and might surprise you."


def recommend_movies(user_input, top_k=9):
    """Movie recommendations based on user input"""
    print("Processing user input...")
    user_embedding = model.encode(user_input)
    similarities = df['embedding'].apply(lambda x: cosine_similarity([user_embedding], [x])[0][0])
    df['similarity'] = similarities
    recommendations = df.sort_values('similarity', ascending=False).head(top_k)
    
    # Add poster URLs and release year for each movie
    movie_data = recommendations['id'].apply(get_movie_poster)
    recommendations['poster_path'] = movie_data.apply(lambda x: x['poster_path'])
    recommendations['release_year'] = movie_data.apply(lambda x: x['release_year'])
    
    # Add explanation for each movie
    recommendations['explanation'] = recommendations.apply(
        lambda row: generate_explanation(user_input, row['original_title'], row['overview'], row['similarity']),
        axis=1
    )
    
    # Print recommendations to console
    print("\n🎬 Recommended movies:")
    for i, row in recommendations.iterrows():
        print(f"\n🎥 {row['original_title']} ({row['release_year']})")
        print(f"📝 {row['explanation']}")
        print(f"📋 Genres: {row['genres']}")
        print(f"🔗 Poster: {row['poster_path']}")
        print("-" * 80)
    
    return recommendations[['id', 'original_title', 'overview', 'genres', 'release_year', 'poster_path', 'explanation']]

def get_movie_poster(movie_id):
    """Get movie poster and release year from TMDB by ID"""
    try:
        # Get movie information by ID
        movie_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        headers = {
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}",
            "accept": "application/json"
        }
        
        response = requests.get(movie_url, headers=headers)
        response.raise_for_status()
        movie_data = response.json()
        
        # Get poster path and release year
        poster_url = "https://via.placeholder.com/500x750?text=No+Poster+Available"
        if movie_data.get("poster_path"):
            poster_url = f"{TMDB_IMAGE_BASE_URL}{movie_data['poster_path']}"
            
        # Get year from release_date
        release_year = None
        if movie_data.get("release_date"):
            release_year = movie_data["release_date"][:4]  # Take first 4 characters (year)
            
        return {
            "poster_path": poster_url,
            "release_year": release_year
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Network error while getting data for movie {movie_id}: {str(e)}")
        return {
            "poster_path": "https://via.placeholder.com/500x750?text=Network+Error",
            "release_year": None
        }
    except Exception as e:
        print(f"Error getting data for movie {movie_id}: {str(e)}")
        return {
            "poster_path": "https://via.placeholder.com/500x750?text=Error",
            "release_year": None
        }

# Test code
if __name__ == "__main__":
    user_mood = "I want to watch a movie about a girl who is a detective"
    recommendations = recommend_movies(user_mood)
    print("\n🎬 Recommended movies:")
    for i, row in recommendations.iterrows():
        print(f"\n🎥 {row['original_title']}\n{row['overview']}\n{row['explanation']}")