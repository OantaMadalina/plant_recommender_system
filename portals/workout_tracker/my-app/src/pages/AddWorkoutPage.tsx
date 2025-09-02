import React from "react";
import AddWorkoutForm from "../components/AddWorkout/Form/AddWorkoutForm";
import styles from "./AddWorkoutPage.module.css";

const AddWorkoutPage: React.FC = () => {
  return (
    <div className={styles.container}>
      <main className={styles.mainContent}>
        <h1 className={styles.pageTitle}>Add New Workout</h1>
        <p className={styles.pageDescription}>Fill out the form below to add a new workout to your list.</p>
        <AddWorkoutForm />
      </main>
    </div>
  );
};

export default AddWorkoutPage;
