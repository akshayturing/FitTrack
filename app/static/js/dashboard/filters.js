/**
 * Filter management for workouts
 */

// Filter state
let currentFilters = {
    focus: '',
    difficulty: '',
    duration: ''
};

/**
 * Initialize filter event listeners
 */
function initializeFilters() {
    // Set up event listeners for filters
    searchInput.addEventListener('input', applyFilters);
    
    focusFilter.addEventListener('change', ev => {
        currentFilters.focus = ev.target.value;
        applyFilters();
    });
    
    difficultyFilter.addEventListener('change', ev => {
        currentFilters.difficulty = ev.target.value;
        applyFilters();
    });
    
    durationFilter.addEventListener('change', ev => {
        currentFilters.duration = ev.target.value;
        applyFilters();
    });
}

/**
 * Apply all active filters to the workout list
 */
function applyFilters() {
    const query = searchInput.value.toLowerCase();
    
    // Apply filters and search to all workouts
    const filteredWorkouts = allWorkouts.filter(workout => {
        // Text search filter
        const matchesSearch = query === '' || 
            workout.name.toLowerCase().includes(query) ||
            workout.description.toLowerCase().includes(query) ||
            workout.focus_area.toLowerCase().includes(query);
        
        // Focus area filter
        const matchesFocus = currentFilters.focus === '' || 
            workout.focus_area.toLowerCase() === currentFilters.focus.toLowerCase();
        
        // Difficulty filter
        const matchesDifficulty = currentFilters.difficulty === '' || 
            workout.difficulty.toLowerCase() === currentFilters.difficulty.toLowerCase();
        
        // Duration filter
        const matchesDuration = currentFilters.duration === '' || 
            matchDurationFilter(workout.duration_minutes, currentFilters.duration);
        
        return matchesSearch && matchesFocus && matchesDifficulty && matchesDuration;
    });
    
    renderWorkoutCards(filteredWorkouts);
}

/**
 * Check if a workout's duration matches the selected duration filter
 * @param {number} workoutDuration - Workout duration in minutes
 * @param {string} durationFilter - Selected duration filter value
 * @returns {boolean} Whether the workout matches the duration filter
 */
function matchDurationFilter(workoutDuration, durationFilter) {
    switch (durationFilter) {
        case '0-15':
            return workoutDuration <= 15;
        case '15-30':
            return workoutDuration > 15 && workoutDuration <= 30;
        case '30-60':
            return workoutDuration > 30 && workoutDuration <= 60;
        case '60+':
            return workoutDuration > 60;
        default:
            return true;
    }
}