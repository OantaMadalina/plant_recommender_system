import { useState } from 'react';
import styles from "./SignsList.module.css";

interface SignsAsButtonsProps{
  setSign: React.Dispatch<React.SetStateAction<string>>;
  selectedSign: string;
}

const SignsAsButtons: React.FC<SignsAsButtonsProps> = ({ setSign, selectedSign }) => {
  const signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    return (
      <div className={styles["signs-list"]}>
        {signs.map((sign) => (<button key={sign} className={sign === selectedSign ? styles["sign-button-selected"]:styles["sign-button"]} onClick={() => setSign(sign)}>{sign}</button>))}
      </div>
    )
  }

export default SignsAsButtons;
