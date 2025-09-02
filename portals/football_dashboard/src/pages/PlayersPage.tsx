import React, { useState } from "react";
import Layout from "../components/Layout";
import styles from "./PlayersPage.module.css";
import axios from "axios";
import environment from "../environment";
import { Player } from "../models/interfaces";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import CustomCountryFlag from "../components/CustomCountryFlag";
import PositionComponent from "../components/PositionComponent";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { BallTriangle } from "react-loader-spinner";

const PlayersPage: React.FC = () => {
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [players, setPlayers] = useState<Player[]>();
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleSearch = async () => {
        console.log("Search query:", searchQuery);

        setIsLoading(true);
        await fetchPlayers();
        setIsLoading(false);
    };

    const handleError = (error: unknown, context: string) => {
        if (axios.isAxiosError(error)) {
            if (error.response) {
                toast.error(`${context}: ${error.response.data?.message || error.response.statusText}`);
            } else if (error.request) {
                toast.error(`${context}: No response received from the server.`);
            } else {
                toast.error(`${context}: Error setting up request: ${error.message}`);
            }
        } else {
            toast.error(`${context}: An unexpected error occurred: ${error}`);
        }
    };

    const fetchPlayers = async () => {
        try {
            if (searchQuery) {
                let receivedPlayers: Player[] = [];

                const response = await axios.get(
                    `${environment.apiPath}footballPlayers`,
                    {
                        params: {
                            name: searchQuery,
                            size: 10,
                        },
                        ...environment.params
                    }
                );

                if (response.data.count === 0) {
                    setPlayers(undefined);
                    return;
                }

                for (const item of response.data.items) {
                    const player: Player = { ...item.player };
                    player.signedPhotoUrl = item.signedPhotoUrl;
                    receivedPlayers.push(player);
                }

                setPlayers(receivedPlayers);
            }
        }  catch (error) {
          handleError(error, 'Error fetching player');
        }
    };

    const handlePlayerNavigation = (playerId: number | undefined) => {
        if (playerId) {
          navigate(`/players/${playerId}`);
        }
    };

    return (
        <Layout>
            <h1 className={styles.heading}>Players</h1>
            <div className={styles.pageDiv}>
                <div className={styles.searchContainer}>
                    <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search by player's name"
                    className={styles.searchInput}
                    />
                    <button onClick={handleSearch} className={styles.confirmButton}>
                        Search
                    </button>
                </div>
                {!isLoading ?
                    <ul className={styles.standingsList}>
                        {players ? players.map((player, index) => (
                            <li key={index} className={styles.playerItem}  onClick={() => handlePlayerNavigation(player.id)}>
                                <div className={styles.scorerInfo}>
                                    <span className={styles.position} style={{color: 'white', width: '60px'}}>{index + 1}.</span>
                                    <div className={styles.playerNameAndPhoto}>
                                        <img src={player.signedPhotoUrl} alt="Player" className={styles.playerPhoto} />
                                        <span className={styles.playerName}> {player.fullName}</span>
                                    </div>
                                    <PositionComponent
                                        fieldPosition={
                                            player.fieldPosition
                                        }
                                    ></PositionComponent>
                                    <div
                                        style={{
                                            fontWeight: "600",
                                            marginLeft: "5px",
                                        }}
                                    >
                                        <CustomCountryFlag
                                            nationality={
                                                player.nationality
                                            }
                                            height="26px"
                                            width="34px"
                                        ></CustomCountryFlag>
                                    </div>
                                </div>
                                <div style={{ display:"flex", gap:"5px", opacity:"0.7"}}>
                                    <span>Check player's profile</span>
                                    <ArrowForwardIosIcon></ArrowForwardIosIcon>
                                </div>
                            </li>
                        )) :
                        <img src={"/assets/football_search.png"} alt="Football Search" className={styles.searchPhoto} />
                        }
                    </ul> : (
                        <div className={styles.centered}>
                            <BallTriangle
                                height={150}
                                width={150}
                                radius={5}
                                color="grey"
                                ariaLabel="ball-triangle-loading"
                                wrapperStyle={{}}
                                wrapperClass=""
                                visible={true}
                            />
                        </div>
                    )
                }
            </div>
        </Layout>
    );
};

export default PlayersPage;
