# Project Architecture

## Overview

The project is built on a client-server architecture using Flask as the backend and a modern web interface for the frontend.

## System Components

### 1. Backend (Flask)

#### Core Modules:
- `app.py` - main application file
- `recommendation.py` - recommendation logic

#### API Endpoints:
- `GET /` - main page
- `POST /recommend` - get recommendations
- `GET /health` - service health check

### 2. Frontend

#### Structure:
- `templates/index.html` - main template
- `static/style.css` - styles
- `static/script.js` - client-side logic

#### Main Components:
- Search bar
- Movie cards
- Theme switcher
- Accessibility mode

### 3. External Services

#### TMDB API
- Movie information retrieval
- Poster loading
- Metadata retrieval

#### GigaChat API
- Recommendation explanation generation
- Semantic query analysis

## Data Flow

1. User enters a query
2. Query is processed on the frontend
3. Sent to the backend
4. Backend:
   - Generates query embeddings
   - Finds similar movies
   - Retrieves additional information from TMDB
   - Generates explanations via GigaChat
5. Results are sent to the frontend
6. Frontend displays recommendations

## Security

- API keys stored in `.env`
- Input data validation
- Error handling at all levels
- Secure HTTP headers

## Scalability

- Modular architecture
- Embedding caching
- Asynchronous request processing
- Horizontal scaling capability 