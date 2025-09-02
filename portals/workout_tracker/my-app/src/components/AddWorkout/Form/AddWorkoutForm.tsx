import React, { useEffect, useState } from "react";
import axios from "axios";
import styles from "./AddWorkoutForm.module.css";
import ExerciseSearch from "../Search/ExerciseSearch";
import { Exercise, Workout } from "../../../interface";
import environment from "../../../environment";
import { toast } from "react-toastify";

const AddWorkoutForm: React.FC = () => {
  const [workoutName, setWorkoutName] = useState("");
  const [workoutDate, setWorkoutDate] = useState("");
  const [selectedExercises, setSelectedExercises] = useState<Exercise[]>([]);
  const [suggestedCategories, setSuggestedCategories] = useState<string[]>([]);
  const [suggestedMuscleGroups, setSuggestedMuscleGroups] = useState<string[]>([]);
  const [notes, setNotes] = useState("");
  const [workoutDuration, setWorkoutDuration] = useState("");

  useEffect(() => {
    const newSuggestedCategories = Array.from(
      new Set(
        selectedExercises
          .map(ex => ex.category)
          .filter((category): category is string => Boolean(category))
      )
    );

    const newSuggestedMuscleGroups = Array.from(
      new Set(
        selectedExercises
          .flatMap(ex => ex.muscleGroups || [])
          .filter((muscleGroup): muscleGroup is string => Boolean(muscleGroup))
      )
    );

    setSuggestedCategories(newSuggestedCategories);
    setSuggestedMuscleGroups(newSuggestedMuscleGroups);
  }, [selectedExercises]);

  const handleExerciseSelect = (exercise: Exercise) => {
    const isAlreadySelected = selectedExercises.some(
      (selectedExercise) => selectedExercise.exerciseId === exercise.exerciseId
    );

    if (!isAlreadySelected) {
      const newExercise: Exercise = {
        exerciseId: exercise.exerciseId,
        exerciseName: exercise.exerciseName,
        description: exercise.description,
        category: exercise.category,
        muscleGroups: exercise.muscleGroups,
        youtubeLink: exercise.youtubeLink,
      };

      setSelectedExercises((prev) => [...prev, newExercise]);
    } else {
      toast.error("Exercise is already selected.");
    }
  };

  const handleExerciseRemove = (exerciseId: string) => {
    setSelectedExercises(prev =>
      prev.filter(exercise => exercise.exerciseId !== exerciseId)
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const workoutData: Workout = {
      workoutId: "",
      workoutName,
      workoutDate,
      exerciseIds: selectedExercises.map((exercise) => exercise.exerciseId),
      notes,
      workoutDuration: parseInt(workoutDuration),
    };

    try {
      const response = await axios.post(
        `${environment.apiPath}workouts`,
        workoutData,
        {
          ...environment.params,
        }
      );
      if (response.status === 200) {
        toast.success("Workout added successfully!");
        setWorkoutName("");
        setWorkoutDate("");
        setSelectedExercises([]);
        setNotes("");
        setWorkoutDuration("");
        setSuggestedCategories([]);
        setSuggestedMuscleGroups([]);
      }
    } catch (error) {
      toast.error("Failed to add workout. Please try again.");
    }
  };

  return (
    <form className={styles.addWorkoutForm} onSubmit={handleSubmit}>
      <div className={styles.formGroup}>
        <label htmlFor="workoutName">Workout Name:</label>
        <input
          type="text"
          id="workoutName"
          value={workoutName}
          onChange={(e) => setWorkoutName(e.target.value)}
          required
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="workoutDate">Workout Date:</label>
        <input
          type="date"
          id="workoutDate"
          value={workoutDate}
          onChange={(e) => setWorkoutDate(e.target.value)}
          min="1900-01-01"
          max="2100-12-31"
          required
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="exerciseSearch">Search and Add Exercises:</label>
        <ExerciseSearch
          onExerciseSelect={handleExerciseSelect}
          suggestedCategories={suggestedCategories}
          suggestedMuscleGroups={suggestedMuscleGroups}
        />
      </div>

      <div className={styles.formGroup}>
        <label>Selected Exercises:</label>
        <ul className={styles.scrollableList}>
          {selectedExercises.map((exercise) => (
            <li key={exercise.exerciseId}>
              {exercise.exerciseName}
              <button
                type="button"
                onClick={() => handleExerciseRemove(exercise.exerciseId)}
                className={styles.removeButton}
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      </div>

      <div className={styles.formGroup}>
        <label htmlFor="notes">Notes:</label>
        <textarea
          id="notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="workoutDuration">Duration (minutes):</label>
        <input
          type="number"
          id="workoutDuration"
          value={workoutDuration}
          onChange={(e) => setWorkoutDuration(e.target.value)}
          required
        />
      </div>
      <button type="submit" className={styles.submitButton}>Add Workout</button>
    </form>
  );
};

export default AddWorkoutForm;
