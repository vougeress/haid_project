async function getRecommendations() {
    const description = document.getElementById('movieDescription').value;
    const topK = document.getElementById('topK').value;
    
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
                top_k: parseInt(topK)
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
    moviesList.innerHTML = '';

    recommendations.forEach(movie => {
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
            </div>
        `;
        moviesList.appendChild(movieCard);
    });

    document.getElementById('results').classList.remove('hidden');
} 