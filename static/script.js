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
        movieCard.innerHTML = `
            <h3>${movie.title}</h3>
            <p>${movie.overview}</p>
        `;
        moviesList.appendChild(movieCard);
    });

    document.getElementById('results').classList.remove('hidden');
} 