from flask import Flask, render_template, request, jsonify
from flask_restx import Api, Resource, fields
from recommendation import recommend_movies
import logging

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Определение главной страницы ДО создания API
@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

# Создание API
api = Api(
    app,
    version='1.0',
    title='Movie Recommendation API',
    description='API для получения рекомендаций фильмов на основе текстового описания',
    doc='/docs'  # URL для Swagger UI
)

# Определение моделей для Swagger
recommendation_model = api.model('Recommendation', {
    'title': fields.String(description='Название фильма'),
    'overview': fields.String(description='Описание фильма')
})

recommendation_response = api.model('RecommendationResponse', {
    'status': fields.String(description='Статус запроса'),
    'recommendations': fields.List(fields.Nested(recommendation_model), description='Список рекомендаций')
})

recommendation_request = api.model('RecommendationRequest', {
    'description': fields.String(required=True, description='Описание желаемого фильма'),
    'top_k': fields.Integer(description='Количество рекомендаций (по умолчанию 10)', default=10)
})

error_model = api.model('Error', {
    'status': fields.String(description='Статус ошибки'),
    'error': fields.String(description='Описание ошибки')
})

@api.route('/recommend')
class MovieRecommendation(Resource):
    @api.expect(recommendation_request)
    @api.response(200, 'Success', recommendation_response)
    @api.response(400, 'Bad Request', error_model)
    @api.response(500, 'Internal Server Error', error_model)
    def post(self):
        """Получить рекомендации фильмов на основе текстового описания"""
        try:
            data = api.payload
            
            if not data or 'description' not in data:
                return {
                    'status': 'error',
                    'error': 'Пожалуйста, предоставьте описание фильма в поле "description"'
                }, 400
            
            description = data['description']
            top_k = data.get('top_k', 10)
            
            logger.info(f"Получен запрос на рекомендации. Описание: {description}")
            
            recommendations = recommend_movies(description, top_k)
            result = []
            for _, row in recommendations.iterrows():
                result.append({
                    'title': row['title'],
                    'overview': row['overview']
                })
                
            logger.info(f"Найдено {len(result)} рекомендаций")
            return {
                'status': 'success',
                'recommendations': result
            }
            
        except Exception as e:
            logger.error(f"Ошибка при обработке запроса: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }, 500

@api.route('/health')
class HealthCheck(Resource):
    @api.response(200, 'Success')
    def get(self):
        """Проверка работоспособности сервиса"""
        return {
            'status': 'healthy',
            'message': 'Сервис рекомендаций работает'
        }

if __name__ == '__main__':
    logger.info("Запуск сервера рекомендаций...")
    app.run(debug=True, host='0.0.0.0', port=5001) 