from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource, fields
from recommendation import recommend_movies, get_movie_poster
import logging

app = Flask(__name__)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main page definition BEFORE API creation
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

# API creation
api = Api(
    app,
    version='1.0',
    title='Movie Recommendation API',
    description='API for getting movie recommendations based on a text description',
    doc='/docs'  # URL for Swagger UI
)

# Swagger models definition
recommendation_model = api.model('Recommendation', {
    'id': fields.Integer(description='Movie ID'),
    'original_title': fields.String(description='Movie title'),
    'overview': fields.String(description='Movie overview'),
    'genres': fields.String(description='Movie genre(s)'),
    'release_year': fields.String(description='Release date'),
    'poster_url': fields.String(description='URL of the movie poster')
})

recommendation_response = api.model('RecommendationResponse', {
    'status': fields.String(description='Request status'),
    'recommendations': fields.List(fields.Nested(recommendation_model), description='List of recommendations')
})

recommendation_request = api.model('RecommendationRequest', {
    'description': fields.String(required=True, description='Description of the desired movie')
})

error_model = api.model('Error', {
    'status': fields.String(description='Error status'),
    'error': fields.String(description='Error description')
})

@api.route('/recommend')
class MovieRecommendation(Resource):
    @api.expect(recommendation_request)
    @api.response(200, 'Success', recommendation_response)
    @api.response(400, 'Bad Request', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def post(self):
        """Get movie recommendations based on a text description"""
        try:
            data = api.payload
            
            if not data or 'description' not in data:
                return {
                    'status': 'error',
                    'error': 'Please provide a movie description in the "description" field'
                }, 400
            
            description = data['description']
            
            logger.info(f"Recommendation request received. Description: {description}")
            
            recommendations = recommend_movies(description)
            result = []
            for _, row in recommendations.iterrows():
                result.append({
                    'id': row['id'],
                    'title': row['original_title'],
                    'overview': row['overview'],
                    'genres': row['genres'],
                    'release_date': row['release_year'],
                    'poster_url': row['poster_path']
                })
                
            logger.info(f"Found {len(result)} recommendations")
            return {
                'status': 'success',
                'recommendations': result
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }, 500

@api.route('/health')
class HealthCheck(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Service health check"""
        return {
            'status': 'healthy',
            'message': 'Recommendation service is running'
        }

if __name__ == '__main__':
    logger.info("Starting recommendation server...")
    app.run(debug=True, host='0.0.0.0', port=5001) 