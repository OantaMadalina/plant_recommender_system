import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { Workout, Exercise } from "../../interface";
import environment from "../../environment";
import styles from "./WorkoutDetails.module.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

interface CompletedProgress {
  completedRepetitions: number;
  completedSets: number;
}

const WorkoutDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [workout, setWorkout] = useState<Workout | null>(null);
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [completedProgress, setCompletedProgress] = useState<{ [exerciseId: string]: CompletedProgress }>({});

  useEffect(() => {
    const fetchWorkoutDetails = async () => {
      setLoading(true);

      try {
        const { data } = await axios.get<{
          statusCode: number;
          workout: Workout;
          exercises: Exercise[];
        }>(`${environment.apiPath}workouts/${id}`, {
          ...environment.params,
        });

        if (data.statusCode === 200) {
          setWorkout(data.workout);
          setExercises(data.exercises);
          const initialProgress = data.exercises.reduce((acc, exercise) => {
            acc[exercise.exerciseId] = { completedRepetitions: 0, completedSets: 0 };
            return acc;
          }, {} as { [key: string]: CompletedProgress });

          setCompletedProgress(initialProgress);
        } else {
          toast.error("Failed to fetch workout details.");
        }
      } catch (err) {
        toast.error("An error occurred while fetching workout details.");
      } finally {
        setLoading(false);
      }
    };

    fetchWorkoutDetails();
  }, [id]);

  const handleIncrement = (exerciseId: string, type: "repetitions" | "sets") => {
    setCompletedProgress((prevProgress) => {
      const currentProgress = prevProgress[exerciseId];
      const total = exercises.find((ex) => ex.exerciseId === exerciseId);

      if (type === "repetitions" && currentProgress.completedRepetitions < (total?.repetitions || 0)) {
        return {
          ...prevProgress,
          [exerciseId]: {
            ...currentProgress,
            completedRepetitions: currentProgress.completedRepetitions + 1,
          },
        };
      }

      if (type === "sets" && currentProgress.completedSets < (total?.totalSets || 0)) {
        return {
          ...prevProgress,
          [exerciseId]: {
            ...currentProgress,
            completedSets: currentProgress.completedSets + 1,
            completedRepetitions: 0,
          },
        };
      }

      return prevProgress;
    });
  };


  const handleDecrement = (exerciseId: string, type: "repetitions" | "sets") => {
    setCompletedProgress((prevProgress) => {
      const currentProgress = prevProgress[exerciseId];

      return {
        ...prevProgress,
        [exerciseId]: {
          ...currentProgress,
          [type === "repetitions" ? "completedRepetitions" : "completedSets"]: Math.max(
            0,
            currentProgress[type === "repetitions" ? "completedRepetitions" : "completedSets"] - 1
          ),
        },
      };
    });
  };

  if (loading) return <div>Loading...</div>;
  if (!workout) return <div>No workout found</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>{workout.workoutName || "Workout Details"}</h1>
      <p className={styles.info}>
        <span className={styles.infoTitle}>Workout Date:</span> {workout.workoutDate}
      </p>
      <p className={styles.info}>
        <span className={styles.infoTitle}>Workout Duration:</span> {workout.workoutDuration || "Not specified"} minutes
      </p>
      <p className={`${styles.info} ${styles.notes}`}>
        <span className={styles.infoTitle}>Notes:</span> {workout.notes || "No notes available"}
      </p>

      {exercises.length > 0 && (
        <div>
          <h2 className={styles.title}>Exercises</h2>
          <ul className={styles.exerciseList}>
            {exercises.map((exercise) => (
              <li key={exercise.exerciseId} className={styles.exerciseItem}>
                <h3 className={styles.exerciseTitle}>{exercise.exerciseName}</h3>
                <p className={styles.exerciseDetail}>
                  <span className={styles.infoTitle}>Description:</span> {exercise.description || "No description available"}
                </p>
                <p className={styles.exerciseDetail}>
                  <span className={styles.infoTitle}>Category:</span> {exercise.category || "Not specified"}
                </p>
                <p className={styles.exerciseDetail}>
                  <span className={styles.infoTitle}>Muscle Groups:</span> {exercise.muscleGroups?.join(", ") || "Not specified"}
                </p>
                <div className={styles.progressContainer}>
                  <p>
                    Completed Repetitions: {completedProgress[exercise.exerciseId]?.completedRepetitions} / {exercise.repetitions}
                    {completedProgress[exercise.exerciseId]?.completedRepetitions == exercise.repetitions && (
                      <span className={styles.checkmark}>✔</span>
                    )}
                  </p>
                  <button onClick={() => handleIncrement(exercise.exerciseId, "repetitions")}>+ Rep</button>
                  <button onClick={() => handleDecrement(exercise.exerciseId, "repetitions")}>- Rep</button>
                </div>

                <div className={styles.progressContainer}>
                  <p>
                    Completed Sets: {completedProgress[exercise.exerciseId]?.completedSets} / {exercise.totalSets}
                    {completedProgress[exercise.exerciseId]?.completedSets == exercise.totalSets && (
                      <span className={styles.checkmark}>✔</span>
                    )}
                  </p>
                  <button onClick={() => handleIncrement(exercise.exerciseId, "sets")}>+ Set</button>
                  <button onClick={() => handleDecrement(exercise.exerciseId, "sets")}>- Set</button>
                </div>

                {exercise.youtubeLink && (
                  <p>
                    <a href={exercise.youtubeLink} target="_blank" rel="noopener noreferrer" className={styles.link}>
                      Watch Video
                    </a>
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      <ToastContainer />
    </div>
  );
};

export default WorkoutDetails;
