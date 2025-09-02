import React from "react";
import { Link } from "react-router-dom";
import WorkoutList from "../components/Workout/WorkoutList";
import styles from "./Dashboard.module.css";

const Dashboard: React.FC = () => {
  return (
    <div className={styles.container}>
      <main className={styles.mainContent}>
        <h1 className={styles.pageTitle}>Dashboard</h1>
        <Link to="/add-workout" className={styles.addWorkoutLink}>Add New Workout</Link>
        <WorkoutList />
      </main>
    </div>
  );
};

export default Dashboard;
