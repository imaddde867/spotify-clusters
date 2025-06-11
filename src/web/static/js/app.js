// Enhanced Spotify AI Recommendations - Better UX JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorAlert = document.getElementById('errorAlert');
    const resultsContainer = document.getElementById('resultsContainer');
    const submitBtn = document.getElementById('submitBtn');
    const welcomeSection = document.getElementById('welcomeSection');

    // Initialize suggestion buttons
    initializeSuggestions();

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
            showError('Please enter a song name to get started');
            return;
        }

        // Hide welcome section and show loading
        hideWelcome();
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
                showError(result.error || 'Unable to find recommendations for this song. Try a different track or check the spelling.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            hideLoading();
        }
    });

    function initializeSuggestions() {
        const suggestionBtns = document.querySelectorAll('.suggestion-btn');
        suggestionBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const song = this.dataset.song;
                const artist = this.dataset.artist;

                document.getElementById('songName').value = song;
                document.getElementById('artistName').value = artist;

                // Smooth scroll to form
                document.querySelector('.search-section').scrollIntoView({
                    behavior: 'smooth'
                });

                // Focus on the form
                setTimeout(() => {
                    document.getElementById('songName').focus();
                }, 500);
            });
        });
    }

    function showLoading() {
        loadingIndicator.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Generating...';

        // Animate loading steps
        animateLoadingSteps();
    }

    function hideLoading() {
        loadingIndicator.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = 'Generate Playlist';

        // Reset loading steps
        resetLoadingSteps();
    }

    function animateLoadingSteps() {
        const steps = ['step1', 'step2', 'step3'];
        let currentStep = 0;

        // Reset all steps
        steps.forEach(stepId => {
            const step = document.getElementById(stepId);
            step.classList.remove('active', 'completed');
        });

        // Activate first step
        document.getElementById(steps[0]).classList.add('active');

        const stepInterval = setInterval(() => {
            if (currentStep < steps.length - 1) {
                // Mark current as completed
                document.getElementById(steps[currentStep]).classList.remove('active');
                document.getElementById(steps[currentStep]).classList.add('completed');

                // Activate next step
                currentStep++;
                document.getElementById(steps[currentStep]).classList.add('active');
            } else {
                clearInterval(stepInterval);
            }
        }, 800);
    }

    function resetLoadingSteps() {
        const steps = ['step1', 'step2', 'step3'];
        steps.forEach(stepId => {
            const step = document.getElementById(stepId);
            step.classList.remove('active', 'completed');
        });
    }

    function hideWelcome() {
        if (welcomeSection) {
            welcomeSection.style.display = 'none';
        }
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

        let searchText = `Found ${result.recommendations.length} AI-powered recommendations for "${query.song_name}"`;
        if (query.artist_name) {
            searchText += ` by ${query.artist_name}`;
        }

        if (result.note) {
            searchText += ` • ${result.note}`;
        }

        searchInfo.textContent = searchText;

        // Update playlist stats
        updatePlaylistStats(result.recommendations);

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

        // Initialize action buttons
        initializeActionButtons(result);

        // Show results with animation
        resultsContainer.style.display = 'block';
        resultsContainer.classList.add('fade-in');

        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
    }

    function updatePlaylistStats(recommendations) {
        const playlistStats = document.getElementById('playlistStats');

        // Calculate stats
        const genres = recommendations.map(track => track.genre).filter(Boolean);
        const uniqueGenres = [...new Set(genres)];
        const avgPopularity = Math.round(
            recommendations.reduce((sum, track) => sum + track.popularity, 0) / recommendations.length
        );

        playlistStats.innerHTML = `
            <div class="stat-item">
                <span>📊 ${recommendations.length} tracks</span>
            </div>
            <div class="stat-item">
                <span>🎵 ${uniqueGenres.length} genres</span>
            </div>
            <div class="stat-item">
                <span>⭐ ${avgPopularity} avg popularity</span>
            </div>
        `;
    }

    function initializeActionButtons(result) {
        // Share button
        const shareBtn = document.getElementById('shareBtn');
        shareBtn.addEventListener('click', function() {
            const query = result.search_query;
            const shareText = `Check out this AI-generated playlist based on "${query.song_name}"${query.artist_name ? ` by ${query.artist_name}` : ''}! 🎵`;

            if (navigator.share) {
                navigator.share({
                    title: 'Spotify AI Recommendations',
                    text: shareText,
                    url: window.location.href
                });
            } else {
                // Fallback: copy to clipboard
                navigator.clipboard.writeText(shareText + ' ' + window.location.href);
                showToast('Link copied to clipboard!');
            }
        });

        // New search button
        const newSearchBtn = document.getElementById('newSearchBtn');
        newSearchBtn.addEventListener('click', function() {
            hideResults();
            document.getElementById('songName').value = '';
            document.getElementById('artistName').value = '';
            document.getElementById('songName').focus();

            // Show welcome section again
            if (welcomeSection) {
                welcomeSection.style.display = 'block';
            }

            // Scroll to top
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    function hideResults() {
        resultsContainer.style.display = 'none';
        resultsContainer.classList.remove('fade-in');
    }

    function showToast(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow-lg);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(toast);
            }, 300);
        }, 3000);
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

        // Show feedback
        showToast('Opening in Spotify...');
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

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            document.getElementById('songName').focus();
        }

        // Escape to clear and start over
        if (e.key === 'Escape') {
            if (resultsContainer.style.display !== 'none') {
                document.getElementById('newSearchBtn').click();
            }
        }
    });

    // Add CSS for toast animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(100%); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
});
