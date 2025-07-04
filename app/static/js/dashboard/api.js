/**
 * API functions for the dashboard
 */

/**
 * Load all workouts assigned to the current user
 * @returns {Promise} Promise that resolves with workouts data
 */
async function fetchUserWorkouts() {
    const userId = getUserId();
    const response = await fetch(`/api/users/${userId}/workouts`);
    
    if (!response.ok) {
        throw new Error(`Error fetching workouts: ${response.status}`);
    }
    
    const data = await response.json();
    return data.workouts || [];
}