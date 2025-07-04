/**
 * Main entry point for the dashboard page
 */

// DOM Elements
const workoutList = document.getElementById('workoutList');
const searchInput = document.getElementById('searchWorkouts');
const focusFilter = document.getElementById('filterFocusArea');
const difficultyFilter = document.getElementById('filterDifficulty');
const durationFilter = document.getElementById('filterDuration');

// Global state
let allWorkouts = [];

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

/**
 * Initialize the dashboard application
 */
async function initializeApp() {
    // Initialize filters
    initializeFilters();
    
    // Load workouts
    try {
        showLoadingState();
        allWorkouts = await fetchUserWorkouts();
        
        if (allWorkouts.length === 0) {
            showNoWorkoutsState();
        } else {
            renderWorkoutCards(allWorkouts);
        }
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        showErrorState();
    }
}