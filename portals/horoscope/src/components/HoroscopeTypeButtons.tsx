import { useState } from 'react';
import styles from "./HoroscopeTypeButtons.module.css";

interface HoroscopeTypeButtonsProps{
  setType: React.Dispatch<React.SetStateAction<string>>;
  selectedType: string;
}

const HoroscopeTypeButtons: React.FC<HoroscopeTypeButtonsProps> = ({setType, selectedType}) => {
    return (
      <div className={styles['horoscope-buttons-container']}>
        <button className={selectedType === "Daily" ? styles["horoscope-buttons-selected"]:styles["horoscope-buttons"]} onClick={() => setType("Daily")}>Daily</button>
        <button className={selectedType === "Monthly" ? styles["horoscope-buttons-selected"]:styles["horoscope-buttons"]} onClick={() => setType("Monthly")}>Monthly</button>
      </div>
    )
  }

export default HoroscopeTypeButtons;