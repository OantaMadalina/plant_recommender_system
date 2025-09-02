import React, { useContext, useState } from 'react'
import { NavLink } from 'react-router-dom'
import styles from './Navbar.module.css'
import AppContext from '../context/AppContext';
import LogoutIcon from '@mui/icons-material/Logout';
import Person2Icon from '@mui/icons-material/Person2';

const Navbar: React.FC = () => {
    const [showModal, setShowModal] = useState(false);
    const { isLoggedIn, validUser, setIsLoggedIn } = useContext(AppContext);

    const logout = () => {
        setIsLoggedIn(false);
        setShowModal(false);
        localStorage.removeItem("isLoggedIn");
    };

    const handleCancel = () => {
        setShowModal(false);
    };

    return (
        <header className={styles.navbar}>
            {isLoggedIn &&
                <nav>
                    <ul>
                        <NavLink
                            to="/fixtures"
                            className={({ isActive }) => (isActive ? styles.active : styles.notActive)}
                        >
                            <li>
                                Fixtures
                            </li>
                        </NavLink>
                        <NavLink
                            to="/standings"
                            className={({ isActive }) => (isActive ? styles.active : styles.notActive)}
                        >
                            <li>
                                Standings
                            </li>
                        </NavLink>
                        <NavLink
                            to="/players"
                            className={({ isActive }) => (isActive ? styles.active : styles.notActive)}
                        >
                            <li>
                                Players
                            </li>
                        </NavLink>
                    </ul>
             </nav>
            }
            <h1>Football Dashboard ⚽︎ Ronaldo = 𓃵 </h1>
            {isLoggedIn &&
                <div className={styles.profileAndLogout} onClick={() => {setShowModal(true)}}>
                    <Person2Icon></Person2Icon>
                    <span>{validUser.fullName}</span>
                    <LogoutIcon fontSize='large' style={{ marginLeft: '15px' }}></LogoutIcon>
                </div>
            }
            {showModal && (
                <div className={styles.modalOverlay}>
                    <div
                        className={styles.modal}
                    >
                        <div
                            className={styles.backgroundImage}
                            style={{
                                backgroundImage: `url('/assets/logout.jpg')`,
                                backgroundSize: 'cover',
                                backgroundPosition: 'center',
                                backgroundRepeat: 'no-repeat',
                            }}
                        />
                        <h2 style={{ paddingBottom: '10px', fontSize: '35px', fontWeight: 'bolder' }}>Confirm Logout</h2>
                        <span style={{fontSize: '25px', fontWeight: 'bolder' }}>Are you sure you want to get out of the pitch?</span>
                        {/* <img src={"/assets/logout.jpg"} alt="Logout" className={styles.logoutPhoto} /> */}
                        <div className={styles.modalActions}>
                        <button onClick={logout} className={styles.confirmButton}>
                            Confirm
                        </button>
                        <button onClick={handleCancel} className={styles.cancelButton}>
                            Cancel
                        </button>
                        </div>
                    </div>
                </div>
            )}
        </header>
    )
}

export default Navbar