/**
 * Workout card rendering functions
 */

/**
 * Generate HTML for a single workout card
 * @param {Object} workout - Workout data
 * @returns {string} HTML for the workout card
 */
function generateWorkoutCard(workout) {
    return `
<div>
        <div class="card workout-card">
            <div class="card-header">
<h5>
${workout.name}

</h5>
</div>
<div>
                <div class="mb-3">
<span>
${capitalizeFirstLetter(workout.focus_area)}

</span>
<span>
${capitalizeFirstLetter(workout.difficulty)}

</span>
<span>
${formatDuration(workout.duration_minutes)}

</span>
</div>
<p>
${workout.description}

</p>
<div>
<small>
<i class="fas fa-dumbbell me-1"></i>

${workout.exercises.length} exercises

</small>
<small>
                        ${workout.equipment_required ? ' <i class="fas fa-tools me-1"></i> Equipment needed' : '<i class="fas fa-home me-1"></i>No equipment'}

</small>
</div>
<a>
<i class="fas fa-play-circle me-1"></i>

Start Workout

</a>
            </div>
        </div>
    </div>
`;
}

/**

Render workout cards to the workout list element

@param {Array} workouts - Array of workout objects
*/
function renderWorkoutCards(workouts) {
if (workouts.length === 0) {
showNoResultsState();
return;
}

const cardsHtml = workouts.map(workout => generateWorkoutCard(workout)).join('');
workoutList.innerHTML = cardsHtml;
}