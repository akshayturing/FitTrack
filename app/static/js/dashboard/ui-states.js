/**
 * UI state management functions
 */

/**
 * Show loading state for the workout list
 */
function showLoadingState() {
    workoutList.innerHTML = `
        <div class="col-12">
            <div class="loading-spinner">
                <i class="fas fa-spinner fa-spin">
</i>
<p>
Loading your workouts...

</p>
        </div>
    </div>
`;
}

/**

Show error state for the workout list */ function showErrorState() { workoutList.innerHTML = `
<div>
        <div class="no-workouts">
<i class="fas fa-exclamation-circle"></i>

<h3>
Oops! Something went wrong

</h3>
<p>
We couldn't load your workouts at this time. Please try refreshing the page or come back later.

</p>
</div>
    </div>
`;
}

/**

Show empty state when no workouts are available */ function showNoWorkoutsState() { workoutList.innerHTML = `
<div>
        <div class="no-workouts">
<i class="fas fa-dumbbell"></i>

<h3>
No Workouts Found

</h3>
<p>
You don't have any workout plans assigned yet. Contact your trainer to get started with your fitness journey!

</p>
</div>
    </div>
`;
}

/**

Show no results state when filters return no workouts */ function showNoResultsState() { workoutList.innerHTML = `<div>
        <div class="no-workouts">
<i class="fas fa-filter"></i>

<h3>
No matching workouts

</h3>
<p>
Try adjusting your filters to see more results.

</p>
</div>
    </div>
`;
}