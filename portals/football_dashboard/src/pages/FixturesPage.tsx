import React, { useContext } from "react";
import Layout from "../components/Layout";
import styles from "./FixturesPage.module.css";
import GameList from "../components/GameList";
import AppContext from "../context/AppContext";

const FixturesPage: React.FC = () => {
    const { isLoggedIn } = useContext(AppContext);
    console.log(isLoggedIn);

    return (
        <Layout>
            <h1 className={styles.heading}>Premier League Fixtures</h1>
            {/* <div className={styles.heading}>
          <div className={styles.emptyDiv}></div>
          <div className={styles.headingTitle}>
            <h1>Premier League Fixtures</h1>
          </div>
          <div className={styles.emptyDiv}></div>
        </div> */}
            <GameList />
        </Layout>
    );
};

export default FixturesPage;
