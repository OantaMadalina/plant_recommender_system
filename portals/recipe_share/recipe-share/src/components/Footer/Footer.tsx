import React from "react";
import styles from './Footer.module.css';

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <p>&copy; 2024 PlatePal</p>
      <p>All rights reserved Cavendish Bootcamp Alumni</p>
    </footer>
  );
};

export default Footer;
