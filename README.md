# 🎬 Movie Recommendation System

A movie recommendation system that helps you find the perfect film based on your text description. Uses modern artificial intelligence technologies to understand your preferences and suggest the most suitable movies.

## ✨ Key Features

- 🎯 **Smart Search** - find movies using text descriptions with semantic search
- 🤖 **AI Explanations** - get personalized explanations of why a movie matches your preferences
- 🎨 **Modern Interface** - beautiful and user-friendly design with dark mode support
- ♿ **Accessibility** - special mode for visually impaired users with enlarged fonts and contrast
- 🎬 **Rich Database** - access to an extensive movie database through TMDB API
- 📱 **Responsive Design** - proper display on all devices

## 🛠 Technologies

- **Backend:**
  - Python 3.13
  - Flask (web framework)
  - Sentence Transformers (semantic search)
  - GigaChat API (explanation generation)
  - TMDB API (movie information)
  - Pandas & NumPy (data processing)
  - scikit-learn (similarity calculations)

- **Frontend:**
  - HTML5/CSS3
  - JavaScript (ES6+)
  - Responsive Design
  - Modern CSS Animations

## 📥 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vougeress/haid_project
   cd movie-recommendations
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys:**
   Create a `.env` file in the root directory and add:
   ```
   TMDB_ACCESS_TOKEN=your_tmdb_token
   GIGA_ACCESS_TOKEN=your_gigachat_token
   ```

## 🚀 Running the Application

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Open in browser:**
   ```
   http://localhost:5001
   ```

## 💡 How to Use

1. **Searching for Movies:**
   - Enter a description of the movie you want to watch
   - Or select one of the suggested options
   - Press the search button or Enter

2. **Viewing Results:**
   - Browse through recommended movies
   - Click "Why this movie?" to get an explanation
   - Use "Show More" for additional recommendations

3. **Interface Settings:**
   - Toggle between dark/light theme
   - Enable accessibility mode if needed

## 📁 Project Structure

```
movie-recommendations/
├── app.py              # Main application file with Flask routes
├── recommendation.py   # Core recommendation logic and AI integration
├── static/            # Static files
│   ├── style.css     # Styles and themes
│   ├── script.js     # Frontend functionality
│   ├── images/       # Images and assets
│   │   └── logo.png  # Application logo
│   └── fonts/        # Custom fonts
│       ├── raydis.woff
│       ├── raydis.ttf
│       └── raydis.otf
├── templates/         # HTML templates
│   └── index.html    # Main page template
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (not in repo)
└── docs/             # Documentation
    ├── api.md        # API documentation and endpoints
    ├── architecture.md # System architecture overview
    ├── development.md # Development guide
    └── user_guide.md  # User manual and features
```

## 🔧 Functionality

### Semantic Search
- Movie search based on semantic query matching using Sentence Transformers
- Considers context and meaning of descriptions
- Supports natural language input
- Uses cosine similarity for matching

### AI Explanations
- Personalized recommendation explanations using GigaChat API
- Takes into account your query and movie features
- Helps understand why a movie matches your preferences
- Concise and friendly explanations

### Movie Data
- Integration with TMDB API for movie information
- Automatic poster retrieval
- Release year information
- Genre categorization

### Interface
- Modern responsive design
- Smooth animations and transitions
- Dark mode support
- Accessibility mode for visually impaired users
- Interactive movie cards with hover effects

## 🤝 Contributing

We welcome your contributions to the project! If you want to help:

1. Fork the repository
2. Create a branch for your changes
3. Make your changes
4. Create a Pull Request

## 📝 License

MIT

## 📚 Documentation

Detailed documentation is available in the `docs` directory:

- [API Documentation](docs/api.md) - Complete API reference with endpoints and examples
- [Architecture Overview](docs/architecture.md) - System design and technical architecture
- [Development Guide](docs/development.md) - Guidelines for developers
- [User Guide](docs/user_guide.md) - User manual and feature documentation

Each component of the system is thoroughly documented to help developers understand and extend the functionality.

## 👨‍💻 Authors

- Strelkov Vladislav
- Petrova Ekaterina
- Sofin Mikhail

---

⭐ If you like the project, don't forget to give it a star! 