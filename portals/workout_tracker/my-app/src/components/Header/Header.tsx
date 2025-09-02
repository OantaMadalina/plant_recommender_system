import React from "react";
import { Link } from "react-router-dom";
import styles from "./Header.module.css";

interface HeaderProps {
  toggleDarkMode: () => void;
  isDarkMode: boolean;
}

const Header: React.FC<HeaderProps> = ({ toggleDarkMode, isDarkMode }) => {
  return (
    <header className={styles.header}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>FitTrack</Link>
        <nav className={styles.navLinks}>
          <Link to="/" className={styles.navLink}>Dashboard</Link>
          <Link to="/add-workout" className={styles.navLink}>Add Workout</Link>
        </nav>
        <button className={styles.toggleButton} onClick={toggleDarkMode}>
          {isDarkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </div>
    </header>
  );
};

export default Header;
