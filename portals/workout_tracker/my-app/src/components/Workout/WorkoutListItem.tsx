import React from "react";
import { Link } from "react-router-dom";
import { Workout } from "../../interface";
import styles from "./WorkoutListItem.module.css";

interface WorkoutListItemProps {
  workout: Workout;
}

const WorkoutListItem: React.FC<WorkoutListItemProps> = ({ workout }) => {
  const formatDuration = (duration: number | undefined) => {
    if (duration === undefined) return "N/A";
    return `${duration} min`;
  };

  const formatDate = (date: string) => new Date(date).toLocaleDateString();

  return (
    <li className={styles.item}>
      <Link to={`/workouts/${workout.workoutId}`} className={styles.link}>
        <div className={styles.content}>
          <h2 className={styles.title}>{workout.workoutName}</h2>
          <div className={styles.details}>
            <p className={styles.date}><strong>Date:</strong> {formatDate(workout.workoutDate)}</p>
            <p className={styles.duration}><strong>Duration:</strong> {formatDuration(workout.workoutDuration)}</p>
            <p className={styles.notes}><strong>Notes:</strong> {workout.notes || "No notes available"}</p>
          </div>
        </div>
      </Link>
    </li>
  );
};

export default WorkoutListItem;
