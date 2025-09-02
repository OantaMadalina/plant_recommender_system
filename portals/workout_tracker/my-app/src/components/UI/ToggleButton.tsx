import React from "react";
// import "./ToggleButton.css";

interface ToggleButtonProps {
  isVisible: boolean;
  toggleVisibility: () => void;
}

const ToggleButton: React.FC<ToggleButtonProps> = ({
  isVisible,
  toggleVisibility,
}) => {
  return (
    <button onClick={toggleVisibility}>
      {isVisible ? "Hide Add Workout Form" : "Add New Workout"}
    </button>
  );
};

export default ToggleButton;
