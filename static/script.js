async function getRecommendations() {
    const description = document.getElementById('movieDescription').value;

    
    if (!description.trim()) {
        alert('Пожалуйста, введите описание фильма');
        return;
    }

    // Показываем индикатор загрузки
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');

    try {
        const response = await fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description: description,
                top_k: 9  // Фиксированное значение
            })
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data.recommendations);
        } else {
            throw new Error(data.error || 'Произошла ошибка при поиске фильмов');
        }
    } catch (error) {
        document.getElementById('error').classList.remove('hidden');
        console.error('Error:', error);
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

function displayResults(recommendations) {
    const moviesList = document.getElementById('moviesList');
    const showMoreBtn = document.getElementById('showMoreBtn');
    moviesList.innerHTML = '';
    
    // Сохраняем все рекомендации в глобальной переменной
    window.allRecommendations = recommendations;
    // Индекс текущей позиции
    window.currentIndex = 0;
    
    // Добавляем обработчик события для кнопки
    showMoreBtn.onclick = showNextMovies;
    
    // Показываем первые 3 фильма
    showNextMovies();
    
    document.getElementById('results').classList.remove('hidden');
}

function addRowHoverHandlers() {
    const movieCards = document.querySelectorAll('.movie-card');
    movieCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const thisTop = card.getBoundingClientRect().top;
            movieCards.forEach(otherCard => {
                if (Math.abs(otherCard.getBoundingClientRect().top - thisTop) < 2) {
                    otherCard.classList.add('row-hover');
                }
            });
        });
        card.addEventListener('mouseleave', function() {
            movieCards.forEach(otherCard => {
                otherCard.classList.remove('row-hover');
            });
        });
    });
}

function showNextMovies() {
    const moviesList = document.getElementById('moviesList');
    const showMoreBtn = document.getElementById('showMoreBtn');
    
    // Получаем следующие 3 фильма
    const nextMovies = window.allRecommendations.slice(
        window.currentIndex,
        window.currentIndex + 3
    );
    
    // Отображаем фильмы
    nextMovies.forEach(movie => {
        const movieCard = createMovieCard(movie);
        moviesList.appendChild(movieCard);
    });
    
    // Обновляем индекс
    window.currentIndex += 3;
    
    // Проверяем, остались ли еще фильмы
    if (window.currentIndex < window.allRecommendations.length) {
        showMoreBtn.style.display = 'block';
    } else {
        showMoreBtn.style.display = 'none';
    }
    // После добавления новых карточек навешиваем обработчики
    addRowHoverHandlers();
}

function createMovieCard(movie) {
    const movieCard = document.createElement('div');
    movieCard.className = 'movie-card';
    
    // Форматируем дату выпуска
    const releaseDate = movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A';
    
    // Форматируем жанры
    let genres = 'N/A';
    try {
        if (movie.genres) {
            const genresList = JSON.parse(movie.genres);
            genres = genresList.map(g => g.name).join(', ');
        }
    } catch (e) {
        console.error('Error parsing genres:', e);
    }
    
    movieCard.innerHTML = `
        <img src="${movie.poster_url}" 
             alt="${movie.title}" 
             class="movie-poster"
             onload="this.classList.add('loaded')"
             onerror="this.src='https://via.placeholder.com/500x750?text=Error+Loading+Poster'; this.classList.add('loaded')">
        <div class="movie-info">
            <h3 class="movie-title">${movie.title}</h3>
            <div class="movie-meta">
                <span class="movie-year">${releaseDate}</span>
                <span class="movie-genres">${genres}</span>
            </div>
            <p class="movie-overview">${movie.overview}</p>
            <button class="explanation-toggle" onclick="toggleExplanation(this)">Why this movie?</button>
            <div class="movie-explanation" style="display: none;">
                <p>${movie.explanation}</p>
            </div>
        </div>
    `;
    return movieCard;
}

function toggleExplanation(button) {
    const explanation = button.nextElementSibling;
    if (explanation.style.display === "none") {
        explanation.style.display = "block";
        button.textContent = "Hide explanation";
    } else {
        explanation.style.display = "none";
        button.textContent = "Why this movie?";
    }
}

// Load saved theme and set up prompt buttons
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    const themeSwitch = document.querySelector('.theme-switch i');
    if (savedTheme === 'dark') {
        themeSwitch.classList.remove('fa-moon');
        themeSwitch.classList.add('fa-sun');
    }

    document.querySelectorAll('.prompt-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.getElementById('movieDescription').value = this.textContent;
            // Автоматически запускаем поиск
            getRecommendations();
        });
    });

    // Добавляем случайные цвета кнопкам
    const promptButtons = document.querySelectorAll('.prompt-btn');
    promptButtons.forEach(button => {
        if (Math.random() < 1) {
            const randomColor = Math.floor(Math.random() * 10) + 1;
            button.classList.add(`color-${randomColor}`);
        }
    });

    // После загрузки страницы навешиваем обработчики на уже существующие карточки
    addRowHoverHandlers();
}); 