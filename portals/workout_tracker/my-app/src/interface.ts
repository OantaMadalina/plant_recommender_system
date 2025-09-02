export interface Workout {
    workoutId: string;
    workoutName?: string;
    workoutDate: string;
    exerciseIds: string[];
    notes?: string;
    workoutDuration?: number;
  }

  export interface Exercise {
    exerciseId: string;
    exerciseName: string;
    description?: string;
    category?: string;
    muscleGroups?: string[];
    youtubeLink?: string;
    repetitions?: number;
    totalSets?: number;
  }
