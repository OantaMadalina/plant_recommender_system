import React, { useCallback, useEffect, useState } from "react";
import axios from "axios";
import "./ExerciseSearch.module.css";
import { Exercise } from "../../../interface";
import environment from "../../../environment";
import { toast } from "react-toastify";

interface ExerciseSearchProps {
  onExerciseSelect: (exercise: Exercise) => void;
  suggestedCategories: string[];
  suggestedMuscleGroups: string[];
}

const ExerciseSearch: React.FC<ExerciseSearchProps> = ({
  onExerciseSelect,
  suggestedCategories,
  suggestedMuscleGroups,
}) => {
  const [exerciseName, setExerciseName] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [muscleGroupFilter, setMuscleGroupFilter] = useState("");
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

  const fetchExercises = useCallback(async () => {
    setLoading(true);

    try {
      const response = await axios.get(`${environment.apiPath}exercises`, {
        params: {
          exerciseName,
          category: categoryFilter,
          muscleGroup: muscleGroupFilter,
        },
        ...environment.params,
      });

      if (response.data.length === 0) {
        toast.info("No exercises found.");
      } else {
        setExercises(response.data);
      }
    } catch (err) {
      toast.error("Failed to fetch exercises.");
    } finally {
      setLoading(false);
    }
  }, [exerciseName, categoryFilter, muscleGroupFilter]);

  useEffect(() => {
    if (exerciseName || categoryFilter || muscleGroupFilter) {
      fetchExercises();
    } else {
      setExercises([]);
    }
  }, [exerciseName, categoryFilter, muscleGroupFilter, fetchExercises]);

  const handleSelect = (exercise: Exercise) => {
    onExerciseSelect(exercise);
  };

  const debounce = (func: Function, delay: number) => {
    let timer: NodeJS.Timeout;
    return (...args: any[]) => {
      clearTimeout(timer);
      timer = setTimeout(() => func(...args), delay);
    };
  };

  const handleExerciseNameChange = debounce((e: React.ChangeEvent<HTMLInputElement>) => {
    setExerciseName(e.target.value);
  }, 300);

  return (
    <div className="exercise-search">
      <button className="dropdown-toggle" onClick={() => setIsOpen(!isOpen)}>
        {isOpen ? "Hide Exercises" : "Show Exercises"}
      </button>
      {isOpen && (
        <div className="dropdown-content">
          <div className="search-filters">
            <input
              type="text"
              placeholder="Search by name..."
              onChange={handleExerciseNameChange}
            />
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="">Filter by category...</option>
              {suggestedCategories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
            <select
              value={muscleGroupFilter}
              onChange={(e) => setMuscleGroupFilter(e.target.value)}
            >
              <option value="">Filter by muscle group...</option>
              {suggestedMuscleGroups.map((muscleGroup) => (
                <option key={muscleGroup} value={muscleGroup}>
                  {muscleGroup}
                </option>
              ))}
            </select>
          </div>
          {loading && <p>Loading...</p>}
          <ul>
            {exercises.map((exercise) => (
              <li key={exercise.exerciseId} onClick={() => handleSelect(exercise)}>
                {exercise.exerciseName}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ExerciseSearch;
