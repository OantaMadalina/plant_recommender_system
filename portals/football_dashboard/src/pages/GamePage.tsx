import React, { useEffect, useState } from "react";
import Layout from "../components/Layout";
import styles from "./GamePage.module.css";
import { Game, Player, Stadium, Team } from "../models/interfaces";
import environment from "../environment";
import axios from "axios";
import { toast } from "react-toastify";
import { Link, useParams } from "react-router-dom";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import StadiumIcon from "@mui/icons-material/Stadium";
import SportsSoccerIcon from "@mui/icons-material/SportsSoccer";
import { BallTriangle } from "react-loader-spinner";

const GamePage: React.FC = () => {
    const [game, setGame] = useState<Game>();
    const [stadium, setStadium] = useState<Stadium>();
    const [firstTeam, setFirstTeam] = useState<Team>();
    const [secondTeam, setSecondTeam] = useState<Team>();
    const [isStadiumLoaded, setIsStadiumLoaded] = useState(false);
    const [scorerPlayers, setScorerPlayers] = useState<Player[]>([]);
    const [sortedScorerMinutes, setSortedScorerMinutes] = useState<any>();

    const { gameId } = useParams<{ gameId: string }>();

    const handleError = (error: unknown, context: string) => {
        if (axios.isAxiosError(error)) {
            if (error.response) {
                toast.error(
                    `${context}: ${
                        error.response.data?.error ||
                        error.response.statusText
                    }`
                );
            } else if (error.request) {
                toast.error(
                    `${context}: No response received from the server.`
                );
            } else {
                toast.error(
                    `${context}: Error setting up request: ${error.message}`
                );
            }
        } else {
            toast.error(`${context}: An unexpected error occurred: ${error}`);
        }
    };

    useEffect(() => {
        const fetchGame = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballGames`,

                    {
                        params: {
                            id: gameId,
                        },
                        ...environment.params,
                    }
                );
                console.log(response.data);
                setGame(response.data.items[0]);
            } catch (error) {
                handleError(error, "Error fetching games");
            }
        };

        fetchGame();
    }, [gameId]);

    useEffect(() => {
        const fetchPlayers = async () => {
            try {
                if (game) {
                    let receivedPlayers: Player[] = [];
                    const playerIdsString = game.scorers
                        ?.filter((scorer) => scorer.playerId !== undefined)
                        .map((scorer) => scorer.playerId)
                        .join(",");

                    if (playerIdsString) {
                        const response = await axios.get(
                            `${environment.apiPath}footballPlayers`,
                            {
                                params: {
                                    id: playerIdsString,
                                },
                                ...environment.params,
                            }
                        );

                        for (const item of response.data.items) {
                            const player: Player = { ...item.player };
                            player.signedPhotoUrl = item.signedPhotoUrl;
                            receivedPlayers.push(player);
                        }

                        setScorerPlayers(receivedPlayers);
                    }
                }
            } catch (error) {
                handleError(error, "Error fetching players that scored");
            }
        };

        const fetchTeams = async () => {
            const teamIds = `${game?.firstTeamId},${game?.secondTeamId}`;

            try {
                const response = await axios.get(
                    `${environment.apiPath}footballTeams`,
                    {
                        params: {
                            id: teamIds,
                        },
                        ...environment.params,
                    }
                );
                let receivedTeams: Team[] = [];

                for (const item of response.data.items) {
                    const team: Team = { ...item.team };
                    team.signedPhotoUrl = item.signedPhotoUrl;
                    receivedTeams.push(team);
                }

                console.log("horse: " + JSON.stringify(response.data.items[0]));

                if (receivedTeams[0].id === game!.firstTeamId) {
                    setFirstTeam(receivedTeams[0]);
                    setSecondTeam(receivedTeams[1]);
                } else {
                    setFirstTeam(receivedTeams[1]);
                    setSecondTeam(receivedTeams[0]);
                }
            } catch (error) {
                handleError(error, "Error fetching teams");
            }
        };

        if (game) {
            fetchTeams();
            fetchPlayers();

            const scorerMinutes = game.scorers
                ?.flatMap((scorer) =>
                    scorer?.minutes?.map((minute) => ({
                        playerId: scorer.playerId,
                        minute: minute,
                        teamId: scorer.teamId,
                    }))
                )
                .sort((a, b) => a.minute - b.minute);

            if (scorerMinutes?.length && scorerMinutes?.length > 0) {
                setSortedScorerMinutes(scorerMinutes);
            }
        }
    }, [game]);

    useEffect(() => {
        const fetchStadium = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}stadiums`,

                    {
                        params: {
                            id: firstTeam?.stadiumId,
                        },
                        ...environment.params,
                    }
                );

                const receivedStadium: Stadium = {
                    ...response.data.items[0].stadium,
                };
                receivedStadium.signedPhotoUrl =
                    response.data.items[0].signedPhotoUrl;

                console.log("Stadium" + JSON.stringify(receivedStadium));
                setStadium(receivedStadium);
            } catch (error) {
                handleError(error, "Error fetching games");
            }
        };

        if (firstTeam) {
            fetchStadium();
        }
    }, [firstTeam]);

    useEffect(() => {
        if (stadium) {
            setIsStadiumLoaded(true);
        }
    }, [stadium]);

    return (
        <Layout>
            <div className={styles.game}>
                {secondTeam && isStadiumLoaded ? (
                    <>
                        <div
                            className={styles.background}
                            style={{
                                backgroundImage: `url(${stadium?.signedPhotoUrl})`,
                            }}
                        />
                        <div className={styles.teamsContainer}>
                            <div className={styles.team}>
                                {firstTeam && (
                                    <>
                                        <Link
                                            to={`/teams/${firstTeam.id}`}
                                            className={styles.teamLink}
                                        >
                                            <img
                                                src={firstTeam.signedPhotoUrl}
                                                alt="First Team Badge"
                                                className={styles.teamBadge}
                                            />
                                        </Link>
                                        <span>{firstTeam.teamName}</span>
                                    </>
                                )}
                                <div className={styles.teamScore}>
                                    {game?.firstTeamScore ?? 0}
                                </div>
                            </div>
                            <span className={styles.scoreSeparator}>-</span>
                            <div className={styles.team}>
                                <div className={styles.teamScore}>
                                    {game?.secondTeamScore ?? 0}
                                </div>
                                {secondTeam && (
                                    <>
                                        <span>{secondTeam.teamName}</span>
                                        <Link
                                            to={`/teams/${secondTeam.id}`}
                                            className={styles.teamLink}
                                        >
                                            <img
                                                src={secondTeam.signedPhotoUrl}
                                                alt="Second Team Badge"
                                                className={styles.teamBadge}
                                            />
                                        </Link>
                                    </>
                                )}
                            </div>
                        </div>
                        <div className={styles.gameDetails}>
                            <div className={styles.gameDateAndTime}>
                                <CalendarMonthIcon></CalendarMonthIcon>
                                {game?.gameDateAndTime.split("T")[0]}
                                <AccessTimeIcon></AccessTimeIcon>
                                {game?.gameDateAndTime.split("T")[1]}
                            </div>
                            <div className={styles.stadiumDetails}>
                                <StadiumIcon></StadiumIcon>
                                {stadium?.stadiumName}
                                <div>({stadium?.stadiumCapacity} seats)</div>
                            </div>
                            <hr className={styles.customHr} />
                            <span className={styles.matchSummaryTitle}>
                                Match Summary
                            </span>
                            <div className={styles.scorersList}>
                                {sortedScorerMinutes ? (
                                    sortedScorerMinutes.map(
                                        (scorer: any, index: any) => {
                                            const player = scorerPlayers.find(
                                                (p) => p.id === scorer.playerId
                                            );
                                            const displayName = player
                                                ? player.fullName
                                                : scorer.playerId;

                                            const justifyContentStyle =
                                                scorer.teamId ===
                                                game?.secondTeamId
                                                    ? "flex-end"
                                                    : "flex-start";
                                            return (
                                                <div
                                                    key={index}
                                                    className={
                                                        styles.gameDetailsScorer
                                                    }
                                                    style={{
                                                        display: "flex",
                                                        justifyContent:
                                                            justifyContentStyle,
                                                        width: "90%",
                                                        marginBottom: "10px",
                                                        marginRight: "10px",
                                                        fontWeight: "500",
                                                        color: "#e1ffc4",
                                                    }}
                                                >
                                                    <SportsSoccerIcon
                                                        style={{
                                                            marginRight: "10px",
                                                        }}
                                                    ></SportsSoccerIcon>
                                                    {scorer.minute}'{" "}
                                                    {displayName}
                                                </div>
                                            );
                                        }
                                    )
                                ) : (
                                    <span
                                        style={{
                                            fontWeight: "600",
                                            color: "#dcdcdc",
                                        }}
                                    >
                                        No scorers. Boring.
                                    </span>
                                )}
                            </div>
                        </div>
                    </>
                ) : (
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
                )}
            </div>
        </Layout>
    );
};

export default GamePage;
