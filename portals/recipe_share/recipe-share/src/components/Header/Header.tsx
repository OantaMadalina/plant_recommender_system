import React, { FC } from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header: FC = () => {
  return (
    <header className={styles.header}>
      <h1 className={styles.logo}>PlatePal</h1>
      <nav>
        <ul className={styles.navList}>
          <li><Link to="/" className={styles.navLink}>Explore</Link></li>
          <li><Link to="/recipes" className={styles.navLink}>My Recipes</Link></li>
          <li><Link to="/recipes/create" className={styles.navLink}>Create Recipe</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
