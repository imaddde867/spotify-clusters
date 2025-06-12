/**
 * Enhanced Spotify AI Recommendations
 * Modern JavaScript with proper error handling, dark mode, and accessibility features
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorAlert = document.getElementById('errorAlert');
    const resultsContainer = document.getElementById('resultsContainer');
    const submitBtn = document.getElementById('submitBtn');
    const welcomeSection = document.getElementById('welcomeSection');
    const themeToggle = document.getElementById('themeToggle');

    // Initialize components
    initializeTheme();
    loadPopularExamples();
    initializeEventListeners();
    
    /**
     * Set up all event listeners
     */
    function initializeEventListeners() {
        // Theme toggle handler
        themeToggle.addEventListener('click', toggleTheme);
        
        // Keyboard shortcuts
        initializeKeyboardShortcuts();
        
        // Accessibility improvements
        initializeAccessibility();
    }

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        try {
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

            // Make API request with timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout
            
            try {
                const response = await fetch('/recommend', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (!response.ok) {
                    throw new Error(`Server responded with status: ${response.status}`);
                }

                const result = await response.json();

                if (result.success) {
                    showResults(result);
                    // Log successful search for analytics
                    console.log(`Search successful: ${data.song_name} by ${data.artist_name || 'unknown'}`);
                } else {
                    showError(result.error || 'Unable to find recommendations for this song. Try a different track or check the spelling.');
                }
            } catch (fetchError) {
                console.error('Fetch error:', fetchError);
                if (fetchError.name === 'AbortError') {
                    showError('Request timed out. The server is taking too long to respond. Please try again later.');
                } else {
                    showError('Network error. Please check your connection and try again.');
                }
            }
        } catch (error) {
            console.error('Form submission error:', error);
            showError('An unexpected error occurred. Please try again.');
        } finally {
            hideLoading();
        }
    });

    /**
     * Load popular song examples from the API
     */
    async function loadPopularExamples() {
        const suggestionGrid = document.getElementById('suggestion-grid');

        try {
            // Add a timeout to the fetch request
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
            
            const response = await fetch('/api/popular-examples?count=3', {
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                throw new Error(`Server responded with status: ${response.status}`);
            }
            
            const result = await response.json();

            if (result.success && result.examples && result.examples.length > 0) {
                // Clear loading state
                suggestionGrid.innerHTML = '';

                // Add new examples
                result.examples.forEach(example => {
                    const button = createSuggestionButton(example);
                    suggestionGrid.appendChild(button);
                });
            } else {
                console.warn('API returned success but no examples');
                loadFallbackExamples();
            }
        } catch (error) {
            console.error('Error loading popular examples:', error);
            loadFallbackExamples();
        }
    }
    
    /**
     * Create a suggestion button element
     * @param {Object} example - The song example with song and artist properties
     * @returns {HTMLElement} - The button element
     */
    function createSuggestionButton(example) {
        const button = document.createElement('button');
        button.className = 'suggestion-btn';
        button.dataset.song = example.song;
        button.dataset.artist = example.artist;
        button.setAttribute('aria-label', `Try ${example.song} by ${example.artist}`);

        button.innerHTML = `
            <span class="suggestion-song">${escapeHtml(example.song)}</span>
            <span class="suggestion-artist">${escapeHtml(example.artist)}</span>
        `;

        // Add click handler
        button.addEventListener('click', function() {
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
        
        return button;
    }

    /**
     * Load fallback examples when API fails
     */
    function loadFallbackExamples() {
        const suggestionGrid = document.getElementById('suggestion-grid');
        const fallbackExamples = [
            { song: 'Bohemian Rhapsody', artist: 'Queen' },
            { song: 'Blinding Lights', artist: 'The Weeknd' },
            { song: 'Shape of You', artist: 'Ed Sheeran' }
        ];

        suggestionGrid.innerHTML = '';

        fallbackExamples.forEach(example => {
            const button = createSuggestionButton(example);
            suggestionGrid.appendChild(button);
        });
        
        // Add a subtle indicator that these are fallback examples
        const fallbackNotice = document.createElement('div');
        fallbackNotice.className = 'fallback-notice';
        fallbackNotice.textContent = 'Using default suggestions';
        fallbackNotice.style.fontSize = '0.75rem';
        fallbackNotice.style.color = 'var(--text-muted)';
        fallbackNotice.style.textAlign = 'center';
        fallbackNotice.style.marginTop = '0.5rem';
        suggestionGrid.appendChild(fallbackNotice);
    }

    // This function is redundant since we're adding event listeners when creating buttons
    // Removing it to avoid duplication

    /**
     * Show loading state with animated steps
     */
    function showLoading() {
        loadingIndicator.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = 'Generating...';
        submitBtn.setAttribute('aria-busy', 'true');

        // Animate loading steps
        animateLoadingSteps();
        
        // Announce to screen readers
        announceToScreenReader('Finding similar songs. Please wait.');
    }

    /**
     * Hide loading state and reset UI
     */
    function hideLoading() {
        loadingIndicator.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = 'Find Similar Songs';
        submitBtn.setAttribute('aria-busy', 'false');

        // Reset loading steps
        resetLoadingSteps();
    }

    /**
     * Initialize theme based on user preference or system setting
     */
    function initializeTheme() {
        // Check for saved theme preference, system preference, or default to light mode
        const savedTheme = localStorage.getItem('theme');
        
        if (savedTheme) {
            // Use saved preference if available
            document.documentElement.setAttribute('data-theme', savedTheme);
        } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            // Use system preference if no saved preference
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            // Default to light mode
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
        
        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!localStorage.getItem('theme')) {
                // Only auto-switch if user hasn't set a preference
                const newTheme = e.matches ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', newTheme);
            }
        });
    }

    /**
     * Toggle between light and dark themes
     */
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        // Add a subtle animation
        document.body.style.transition = 'background-color 0.3s ease';
        setTimeout(() => {
            document.body.style.transition = '';
        }, 300);
        
        // Announce theme change to screen readers
        announceToScreenReader(`${newTheme} mode activated`);
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

    /**
     * Show error message with animation
     * @param {string} message - The error message to display
     */
    function showError(message) {
        const errorMessageEl = document.getElementById('errorMessage');
        errorMessageEl.textContent = message;
        errorAlert.style.display = 'block';
        errorAlert.classList.add('fade-in');
        errorAlert.setAttribute('role', 'alert');
        errorAlert.setAttribute('aria-live', 'assertive');

        // Scroll to error
        errorAlert.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Log error for analytics
        console.error('User-facing error:', message);
    }

    /**
     * Hide error message
     */
    function hideError() {
        errorAlert.style.display = 'none';
        errorAlert.classList.remove('fade-in');
        errorAlert.removeAttribute('role');
        errorAlert.removeAttribute('aria-live');
    }

    /**
     * Display recommendation results
     * @param {Object} result - The API response with recommendations
     */
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
        recommendationsList.innerHTML = ''; // Clear previous results
        
        // Create and append track items
        result.recommendations.forEach((track, index) => {
            const trackItem = createTrackItem(track, index);
            recommendationsList.appendChild(trackItem);
        });

        // Initialize action buttons
        initializeActionButtons(result);

        // Show results with animation
        resultsContainer.style.display = 'block';
        resultsContainer.classList.add('fade-in');
        
        // Set focus for accessibility
        document.getElementById('searchInfo').setAttribute('tabindex', '-1');
        document.getElementById('searchInfo').focus();

        // Scroll to results
        setTimeout(() => {
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
        
        // Announce to screen readers
        announceToScreenReader(`Found ${result.recommendations.length} recommendations for ${query.song_name}`);
    }
    
    /**
     * Create a track item element
     * @param {Object} track - The track data
     * @param {number} index - The track index
     * @returns {HTMLElement} - The track item element
     */
    function createTrackItem(track, index) {
        const trackItem = document.createElement('div');
        trackItem.className = 'track-item fade-in';
        trackItem.style.animationDelay = `${index * 0.05}s`;
        trackItem.setAttribute('role', 'listitem');
        
        const trackNumber = document.createElement('div');
        trackNumber.className = 'track-number';
        trackNumber.textContent = index + 1;
        
        const trackInfo = document.createElement('div');
        trackInfo.className = 'track-info';
        
        const trackName = document.createElement('div');
        trackName.className = 'track-name';
        trackName.textContent = track.track_name;
        
        const trackArtist = document.createElement('div');
        trackArtist.className = 'track-artist';
        trackArtist.textContent = track.artist_name;
        
        trackInfo.appendChild(trackName);
        trackInfo.appendChild(trackArtist);
        
        const trackMeta = document.createElement('div');
        trackMeta.className = 'track-meta';
        
        if (track.genre) {
            const genreTag = document.createElement('span');
            genreTag.className = 'genre-tag';
            genreTag.textContent = track.genre;
            trackMeta.appendChild(genreTag);
        }
        
        const popularityScore = document.createElement('span');
        popularityScore.className = 'popularity-score';
        popularityScore.textContent = track.popularity;
        trackMeta.appendChild(popularityScore);
        
        const spotifyBtn = document.createElement('button');
        spotifyBtn.className = 'spotify-btn';
        spotifyBtn.textContent = 'Spotify';
        spotifyBtn.setAttribute('aria-label', `Open ${track.track_name} by ${track.artist_name} on Spotify`);
        spotifyBtn.addEventListener('click', () => {
            searchOnSpotify(track.track_name, track.artist_name);
        });
        trackMeta.appendChild(spotifyBtn);
        
        trackItem.appendChild(trackNumber);
        trackItem.appendChild(trackInfo);
        trackItem.appendChild(trackMeta);
        
        return trackItem;
    }

    /**
     * Update playlist statistics display
     * @param {Array} recommendations - The list of recommended tracks
     */
    function updatePlaylistStats(recommendations) {
        const playlistStats = document.getElementById('playlistStats');

        // Calculate stats
        const genres = recommendations.map(track => track.genre).filter(Boolean);
        const uniqueGenres = [...new Set(genres)];
        const avgPopularity = Math.round(
            recommendations.reduce((sum, track) => sum + (track.popularity || 0), 0) / 
            (recommendations.length || 1)  // Avoid division by zero
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

    /**
     * Initialize action buttons for the results section
     * @param {Object} result - The API response with recommendations
     */
    function initializeActionButtons(result) {
        // Share button
        const shareBtn = document.getElementById('shareBtn');
        shareBtn.addEventListener('click', function() {
            const query = result.search_query;
            const shareText = `Check out this AI-generated playlist based on "${query.song_name}"${query.artist_name ? ` by ${query.artist_name}` : ''}! 🎵`;

            try {
                if (navigator.share) {
                    navigator.share({
                        title: 'Spotify AI Recommendations',
                        text: shareText,
                        url: window.location.href
                    }).catch(err => {
                        console.warn('Share failed:', err);
                        fallbackShare();
                    });
                } else {
                    fallbackShare();
                }
            } catch (e) {
                console.error('Share error:', e);
                fallbackShare();
            }
            
            function fallbackShare() {
                try {
                    navigator.clipboard.writeText(shareText + ' ' + window.location.href);
                    showToast('Link copied to clipboard!');
                } catch (clipboardErr) {
                    console.error('Clipboard error:', clipboardErr);
                    showToast('Sharing not supported on this browser');
                }
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
            
            // Announce to screen readers
            announceToScreenReader('Starting a new search');
        });
    }

    function hideResults() {
        resultsContainer.style.display = 'none';
        resultsContainer.classList.remove('fade-in');
    }

    /**
     * Show a toast notification
     * @param {string} message - The message to display
     * @param {number} duration - How long to show the toast in ms (default: 3000)
     */
    function showToast(message, duration = 3000) {
        // Remove any existing toasts
        const existingToasts = document.querySelectorAll('.toast-notification');
        existingToasts.forEach(toast => {
            document.body.removeChild(toast);
        });
        
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast-notification';
        toast.textContent = message;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'polite');
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
                if (document.body.contains(toast)) {
                    document.body.removeChild(toast);
                }
            }, 300);
        }, duration);
    }

    /**
     * Escape HTML special characters to prevent XSS
     * @param {string} text - The text to escape
     * @returns {string} - The escaped text
     */
    function escapeHtml(text) {
        if (!text) return '';
        
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, function(m) { return map[m]; });
    }

    /**
     * Search for a track on Spotify
     * @param {string} trackName - The name of the track
     * @param {string} artistName - The name of the artist
     */
    window.searchOnSpotify = function(trackName, artistName) {
        const query = encodeURIComponent(`${trackName} ${artistName}`);
        const spotifyUrl = `https://open.spotify.com/search/${query}`;
        
        try {
            window.open(spotifyUrl, '_blank', 'noopener,noreferrer');
            showToast('🎧 Opening in Spotify...');
        } catch (e) {
            console.error('Error opening Spotify:', e);
            showToast('Could not open Spotify. Please check your browser settings.');
        }
    };
    
    /**
     * Announce a message to screen readers
     * @param {string} message - The message to announce
     */
    function announceToScreenReader(message) {
        // Create or use existing live region
        let liveRegion = document.getElementById('sr-announcer');
        
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.id = 'sr-announcer';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            liveRegion.className = 'sr-only';
            liveRegion.style.cssText = 'position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0;';
            document.body.appendChild(liveRegion);
        }
        
        // Update the live region
        liveRegion.textContent = message;
    }

    function initializeKeyboardShortcuts() {
        // Keyboard shortcuts
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

            // Ctrl/Cmd + D to toggle dark mode
            if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                e.preventDefault();
                toggleTheme();
            }
        });
    }

    function initializeAccessibility() {
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

        // Auto-focus on song name input
        document.getElementById('songName').focus();
    }
});
