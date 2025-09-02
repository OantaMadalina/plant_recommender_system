import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppContext from "../context/AppContext";
import styles from "./LoginPage.module.css";
import Layout from "../components/Layout";

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);
    const { isLoggedIn, setIsLoggedIn, validUser } = useContext(AppContext);
    console.log(isLoggedIn);
    const navigate = useNavigate();

    const login = (username: string, password: string) => {
        if (username === validUser.username && password === validUser.password) {
            setIsLoggedIn(true);
            console.log("suca");
            return true;
        }
        return false;
      };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (login(username, password)) {
            navigate("/fixtures");
        } else {
            setError("Invalid username or password!");
        }
    };

    return (
        <Layout>
            <div className={styles.pageDiv}>
                <img src={"/assets/football_dashboard_logo.png"} alt="App logo" className={styles.webLogo} />
                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={styles.inputGroup}>
                        <label>Username: </label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => {
                                setUsername(e.target.value);
                                setError("");
                            }}
                        />
                    </div>
                    <div className={styles.inputGroup}>
                        <label>Password: </label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => {
                                setPassword(e.target.value);
                                setError("");
                            }}
                        />
                    </div>
                    <button type="submit" className={styles.button}>
                        Login
                    </button>
                    {error && <p className={styles.error}>{error}</p>}
                </form>
            </div>
        </Layout>
    );
};

export default LoginPage;
