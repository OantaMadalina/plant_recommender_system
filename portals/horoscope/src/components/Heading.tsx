import { useNavigate } from 'react-router-dom';
import styles from "./Heading.module.css";


const Heading = () => {
  const navigate = useNavigate();

  const goToAdminPage = () => {
    navigate('/admin');
  };

  const goToMainPage = () => {
    navigate('/');
  };

    return (
    <div className={styles["heading"]}>
      <button onClick={goToMainPage} className={styles["heading-title"]}><h1>Horoscope</h1></button>
      <div className={styles["buttons-container"]}>
        <button onClick={goToAdminPage} className={styles["heading-button"]}><h3>Admin</h3></button>
        <button className={styles["heading-button"]}><h3>Sign In</h3></button>
        <button className={styles["heading-button"]}><h3>Register</h3></button>
        <button className={styles["heading-button"]}><h3>Log Out</h3></button>
      </div>
    </div>)
  }

export default Heading;
