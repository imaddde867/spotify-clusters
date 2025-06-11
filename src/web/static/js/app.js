// Modern Spotify AI Recommendations - Clean JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorAlert = document.getElementById('errorAlert');
    const resultsContainer = document.getElementById('resultsContainer');
    const submitBtn = document.getElementById('submitBtn');

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Get form data
        const formData = new FormData(form);
        const data = {
            song_name: formData.get('song_name').trim(),
            artist_name: formData.get('artist_name').trim(),
            playlist_size: parseInt(formData.get('playlist_size'))
        };

        // Validate input
        if (!data.song_name) {
            showError('Please enter a song name');
            return;
        }

        // Show loading state
        showLoading();
        hideError();
        hideResults();

        try {
            // Make API request
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                showResults(result);
            } else {
                showError(result.error || 'An error occurred while generating recommendations');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    });

    function showLoading() {
        loadingIndicator.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Generating...';
    }

    function hideLoading() {
        loadingIndicator.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = 'Generate Playlist';
    }

    function showError(message) {
        document.getElementById('errorMessage').textContent = message;
        errorAlert.style.display = 'block';
        errorAlert.classList.add('fade-in');

        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function hideError() {
        errorAlert.style.display = 'none';
        errorAlert.classList.remove('fade-in');
    }

    function showResults(result) {
        // Update search info
        const searchInfo = document.getElementById('searchInfo');
        const query = result.search_query;

        let searchText = `Found ${result.recommendations.length} recommendations for "${query.song_name}"`;
        if (query.artist_name) {
            searchText += ` by ${query.artist_name}`;
        }

        if (result.note) {
            searchText += ` • ${result.note}`;
        }

        searchInfo.textContent = searchText;

        // Update recommendations list
        const recommendationsList = document.getElementById('recommendationsList');
        let recommendationsHTML = '';

        result.recommendations.forEach((track, index) => {
            recommendationsHTML += `
                <div class="track-item fade-in" style="animation-delay: ${index * 0.05}s">
                    <div class="track-number">${index + 1}</div>
                    <div class="track-info">
                        <div class="track-name">${escapeHtml(track.track_name)}</div>
                        <div class="track-artist">${escapeHtml(track.artist_name)}</div>
                    </div>
                    <div class="track-meta">
                        ${track.genre ? `<span class="genre-tag">${escapeHtml(track.genre)}</span>` : ''}
                        <span class="popularity-score">${track.popularity}</span>
                        <button class="spotify-btn" onclick="searchOnSpotify('${escapeHtml(track.track_name)}', '${escapeHtml(track.artist_name)}')">
                            Spotify
                        </button>
                    </div>
                </div>
            `;
        });

        recommendationsList.innerHTML = recommendationsHTML;

        // Show results with animation
        resultsContainer.style.display = 'block';
        resultsContainer.classList.add('fade-in');

        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    function hideResults() {
        resultsContainer.style.display = 'none';
        resultsContainer.classList.remove('fade-in');
    }

    // Utility function to escape HTML
    function escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    // Function to search on Spotify
    window.searchOnSpotify = function(trackName, artistName) {
        const query = encodeURIComponent(`${trackName} ${artistName}`);
        const spotifyUrl = `https://open.spotify.com/search/${query}`;
        window.open(spotifyUrl, '_blank');
    };

    // Auto-focus on song name input
    document.getElementById('songName').focus();

    // Add enter key support for all inputs
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') {
                e.preventDefault();
                form.dispatchEvent(new Event('submit'));
            }
        });
    });

    // Add subtle hover effects
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.track-item')) {
            e.target.closest('.track-item').style.transform = 'translateX(4px)';
        }
    });

    document.addEventListener('mouseout', function(e) {
        if (e.target.closest('.track-item')) {
            e.target.closest('.track-item').style.transform = 'translateX(0)';
        }
    });
});
