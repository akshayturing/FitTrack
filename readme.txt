# FitTrack


## Introduction
FitTrack is a personalized fitness tracking application that empowers users to take control of their workout routines. The platform allows administrators or fitness professionals to define reusable workout templates consisting of exercises, which users can browse and select. Once a workout is chosen, users can log their daily progress by specifying the number of sets, repetitions, and weights for each exercise — tagged with a specific date. The backend will be implemented using Flask, exposing secure RESTful APIs with proper relational database models and token-based authentication. The frontend (potentially using React) will offer an intuitive interface for registration, login, workout selection, session entry, and progress tracking. The project architecture emphasizes modularity, scalability, and data integrity, with room to integrate analytics and adaptive training recommendations in the future.
## Conversations

### 1. Design the Data Models and Database Schema
Define the relational structure of the application using SQLAlchemy. This includes creating models for User, Workout, Exercise, WorkoutAssignment (linking a user to a workout), WorkoutSession (individual logged date), and SetLog (recording each set with reps, weight, and optionally RPE). Determine required constraints such as primary/foreign keys, uniqueness, and nullability. Discuss whether nutrition goals are part of this phase or remain separate.

### 2. Implement Authentication and User Management
Establish user registration and login routes using JWT for secure access. Decide on fields required during signup (name, email, password), password hashing mechanism, and token expiration strategy. Create decorators or middleware to protect routes and restrict access to authenticated users only. Optionally, prepare for roles (admin/user) if future authorization is needed.

### 3. Create Admin Routes to Manage Workouts and Exercises
Design routes for admins to create and manage workouts and their associated exercises. Define exercise fields like name, type (e.g. strength, cardio), default reps/sets, and target muscle groups. Allow workouts to consist of multiple exercises in a defined sequence. Ensure proper validation and nesting of input payloads.

### 4. Build User Workflow for Selecting a Workout
Enable users to browse a list of available workouts and select one to begin tracking. Upon selection, link the user to the workout using a WorkoutAssignment table. Ensure that duplicate assignments are avoided, and allow users to remove or switch plans.

### 5.  Develop Session Logging API
Allow users to log their workout activity on a given date. They should be able to submit:
Which assigned workout they’re performing
Date of session
For each exercise: sets performed, number of reps, weight used
This data will be stored in WorkoutSession and SetLog tables. Include input validation, support for partial entries, and timestamp tracking.

### 6. Build Frontend Components for Interaction
Develop the UI using React (or another frontend framework of your choice). Focus on:
User registration & login forms
Dashboard to view available workouts and make a selection
Session logging form with dynamic inputs for sets/reps/weights
A view to see workout history and progress summaries
Design for responsiveness and simplicity, allowing quick logging after workouts.

### 7. Backend Debugging & Performance Optimization 
To enhance overall code quality and project maintainability, it's important to focus on debugging existing errors, optimizing performance, and refactoring the structure into clear, modular components. This involves identifying problematic patterns or inaccessible attributes, improving the way test environments and dependencies are configured, and separating different responsibilities across files and directories. Modularizing the code helps ensure each part of the system is easier to understand, test, and extend over time. The goal is to make the application more robust, scalable, and developer-friendly

### 8. Final Testing, Deployment
The final phase for FitTrack involves validating that all authentication, user session, and workout-related endpoints behave as expected across protected routes. Remaining unit test failures—including login flow mismatches, unreadable password fields, and expired tokens—must be resolved with consistent error handling and secure JWT logic. Cleanup efforts include modularizing route files, ensuring correct fixture registration, and aligning API responses with standardized formats.


## Code Execution Screenshots
### Conversation 1: Execution Output
![Conversation 1 Execution](https://drive.google.com/file/d/1APs8kd9OiFR8raQJ3KrFeZ40rJ8UHZeO/view?usp=drive_link)
### Conversation 2: Execution Output
![Conversation 2 Execution](https://drive.google.com/file/d/1LliBjpcB6mHD4rzG_tVf-3Dk7fRiF45z/view?usp=drive_link)
### Conversation 3: Execution Output
![Conversation 3 Execution](https://drive.google.com/file/d/1GIz_awmnw-Jbk8u3fFcQD-bCYldDoSks/view?usp=drive_link)
### Conversation 4: Execution Output
![Conversation 4 Execution](https://drive.google.com/file/d/1MFK1mVpXUAMkw0eyFU9JKSb6NlA74TvM/view?usp=drive_link)
### Conversation 5: Execution Output
![Conversation 5 Execution](https://drive.google.com/file/d/15E8hjed-ggeSo_tZhG9Mp26wyt4zNhMU/view?usp=drive_link)
### Conversation 6: Execution Output
![Conversation 6 Execution](https://drive.google.com/file/d/1tyQeVgUHHOt39Jm_Xd3ppFDZYGFbIQCV/view?usp=drive_link)
### Conversation 7: Execution Output
![Conversation 7 Execution](https://drive.google.com/file/d/1fGM3l83LCCEpbMWiDz-HkUSC4tA6edLQ/view?usp=drive_link)
### Conversation 8: Execution Output
![Conversation 8 Execution](https://drive.google.com/file/d/1CnmemXoWGlBNvDSzozq-IWP5VxMNk9Fz/view?usp=drive_link)


## Unit Test Outputs and Coverage
The following test cases validate critical components of the system.
### Conversation 1 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1-kKAFsDQSNIsFUTUKw-VdcaNYx0MX4rS/view?usp=drive_link)

### Conversation 2 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1Rf5CxOOhDKMXe42r49Zdc7gPhClASrx6/view?usp=drive_link)

### Conversation 3 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1M-7iziPNDHU1SocGJ7X9Ytc1pho5gRUv/view?usp=drive_link)

### Conversation 4 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1UgVylFb535lBLnepzMCSHr0Mc39PO2i-/view?usp=drive_link)

### Conversation 5 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1GqkTC0v-xGXrbyr9TXOylgV2JKBcfEwd/view?usp=drive_link)

### Conversation 6 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/15a8z2vMjRj7XIjlIss5viDwVoh40At3q/view?usp=drive_link)

### Conversation 7 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1uAkmpW3us0rDrsLijS2wHVVkkLnMaAjj/view?usp=drive_link)

### Conversation 8 Test Results
- **Test 1**: 
  ![Test 1](https://drive.google.com/file/d/1SH9JfXnP-wKspuPQsc5aoczAYu2fbVLd/view?usp=drive_link)