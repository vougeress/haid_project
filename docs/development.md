# Development Guide

## Environment Setup

### Requirements
- Python 3.13+
- pip
- git

### Installing Dependencies

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
# or
venv\Scripts\activate  # for Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### API Key Configuration

1. Get API keys:
   - TMDB API: https://www.themoviedb.org/settings/api
   - GigaChat API: https://developers.sber.ru/portal/products/gigachat

2. Create `.env` file:
```
TMDB_ACCESS_TOKEN=your_tmdb_token
GIGA_ACCESS_TOKEN=your_gigachat_token
```

## Project Structure

```
movie-recommendations/
├── app.py              # Main application file
├── recommendation.py   # Recommendation logic
├── static/            # Static files
│   ├── style.css     # Styles
│   ├── script.js     # JavaScript
│   └── fonts/        # Fonts
├── templates/         # HTML templates
│   └── index.html    # Main page
├── docs/             # Documentation
│   ├── api.md       # API documentation
│   ├── architecture.md # Architecture
│   └── development.md  # Development guide
└── requirements.txt   # Dependencies
```

## Development

### Running in Development Mode

```bash
python app.py
```

### Testing

1. Run tests:
```bash
python -m pytest tests/
```

2. Check coverage:
```bash
coverage run -m pytest tests/
coverage report
```

### Linting

```bash
flake8 .
black .
```

## Git Workflow

### Branches

- `main` - main branch
- `develop` - development branch
- `feature/*` - feature branches
- `bugfix/*` - bug fix branches

### Commits

Use the following format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- feat: new feature
- fix: bug fix
- docs: documentation changes
- style: formatting
- refactor: refactoring
- test: tests
- chore: dependency updates

### Pull Request

1. Create a branch for the new feature
2. Make changes
3. Create Pull Request
4. Wait for code review
5. Make changes if needed
6. After approval, PR will be merged into main

## Deployment

### Preparation

1. Update version in `app.py`
2. Update CHANGELOG.md
3. Create tag:
```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

### Deployment

1. Clone repository to server
2. Install dependencies
3. Configure environment variables
4. Start application:
```bash
python app.py
```

## Monitoring

- Logs: `logs/app.log`
- Metrics: Prometheus + Grafana
- Errors: Sentry

## Security

- Regularly update dependencies
- Check code for vulnerabilities
- Use secure development practices
- Store secrets in environment variables 