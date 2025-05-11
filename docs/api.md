# API Documentation

## Endpoints

### 1. GET /
Main page of the application.

**Response:**
- HTML page with application interface

### 2. POST /recommend
Get movie recommendations based on text description.

**Request Body:**
```json
{
    "description": "string"  // Description of desired movie
}
```

**Response:**
```json
{
    "status": "success",
    "recommendations": [
        {
            "id": "integer",
            "title": "string",
            "overview": "string",
            "genres": "string",
            "release_date": "string",
            "poster_url": "string",
            "explanation": "string"
        }
    ]
}
```

**Error Response:**
```json
{
    "status": "error",
    "error": "string"  // Error description
}
```

### 3. GET /health
Service health check.

**Response:**
```json
{
    "status": "healthy",
    "message": "Recommendation service is running"
}
```

## Data Models

### Recommendation
```json
{
    "id": "integer",          // Movie ID
    "title": "string",        // Movie title
    "overview": "string",     // Movie description
    "genres": "string",       // Genres
    "release_date": "string", // Release date
    "poster_url": "string",   // Poster URL
    "explanation": "string"   // Recommendation explanation
}
```

## Error Codes

- 200: Successful request
- 400: Invalid request format
- 500: Internal server error

## Usage Examples

### Getting Recommendations

```bash
curl -X POST http://localhost:5001/recommend \
     -H "Content-Type: application/json" \
     -d '{"description": "I want to watch a movie about a female detective"}'
```

### Health Check

```bash
curl http://localhost:5001/health
```

## Limitations

- Maximum description length: 1000 characters
- Number of recommendations: up to 9 movies
- Request rate: no more than 10 requests per minute 