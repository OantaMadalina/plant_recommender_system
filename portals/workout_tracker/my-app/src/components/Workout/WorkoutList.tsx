import React, { useEffect, useState } from "react";
import axios from "axios";
import { Workout } from "../../interface";
import WorkoutListItem from "./WorkoutListItem";
import environment from "../../environment";
import styles from "./WorkoutList.module.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const WorkoutList: React.FC = () => {
  const [workouts, setWorkouts] = useState<Workout[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWorkouts = async () => {
      setLoading(true);

      try {
        const { data } = await axios.get<Workout[]>(`${environment.apiPath}workouts`, {
          ...environment.params,
        });

        if (data.length > 0) {
          setWorkouts(data);
        } else {
          toast.info("No workouts available.");
        }
      } catch (err: any) {
        toast.error("An error occurred while fetching workouts.");
      } finally {
        setLoading(false);
      }
    };

    fetchWorkouts();
  }, []);

  if (loading) return <div className={styles.loader}>Loading...</div>;

  return (
    <div className={styles.workoutList}>
      <h1 className={styles.pageTitle}>My Workouts</h1>
      <ul className={styles.workoutListItems}>
        {workouts.map((workout) => (
          <WorkoutListItem key={workout.workoutId} workout={workout} />
        ))}
      </ul>

      <ToastContainer />
    </div>
  );
};

export default WorkoutList;
