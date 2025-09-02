import React, { useEffect, useState } from "react";
import Layout from "../components/Layout";
import styles from "./TeamPage.module.css";
import { useNavigate, useParams } from "react-router-dom";
import { toast } from "react-toastify";
import axios from "axios";
import environment from "../environment";
import { Player, Stadium, Team } from "../models/interfaces";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import PublicIcon from "@mui/icons-material/Public";
import StadiumIcon from "@mui/icons-material/Stadium";
import LocationCityIcon from "@mui/icons-material/LocationCity";
import LocationOnIcon from "@mui/icons-material/LocationOn";
import GroupsIcon from "@mui/icons-material/Groups";
import GrassIcon from "@mui/icons-material/Grass";
import CustomCountryFlag from "../components/CustomCountryFlag";
import PositionComponent from "../components/PositionComponent";
import InfoIcon from "@mui/icons-material/Info";
import { BallTriangle } from "react-loader-spinner";

const TeamPage: React.FC = () => {
    const [team, setTeam] = useState<Team>();
    const [stadium, setStadium] = useState<Stadium>();
    const [teamPlayers, setTeamPlayers] = useState<Player[]>([]);
    const { teamId } = useParams<{ teamId: string }>();

    const navigate = useNavigate();

    const handlePlayerNavigation = (playerId: number | undefined) => {
        if (playerId) {
            navigate(`/players/${playerId}`);
        }
    };

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
        const fetchTeam = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballTeams`,

                    {
                        params: {
                            id: teamId,
                        },
                        ...environment.params,
                    }
                );

                const receivedTeam: Team = { ...response.data.items[0].team };
                receivedTeam.signedPhotoUrl =
                    response.data.items[0].signedPhotoUrl;

                setTeam(receivedTeam);
            } catch (error) {
                handleError(error, "Error fetching team");
            }
        };

        fetchTeam();
    }, [teamId]);

    useEffect(() => {
        const fetchStadium = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}stadiums`,

                    {
                        params: {
                            id: team?.stadiumId,
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

        if (team) {
            fetchStadium();
        }
    }, [team]);

    useEffect(() => {
        const fetchTeamPlayers = async () => {
            try {
                if (teamId) {
                    let receivedPlayers: Player[] = [];

                    const response = await axios.get(
                        `${environment.apiPath}footballPlayers`,
                        {
                            params: {
                                teamId: teamId,
                            },
                            ...environment.params,
                        }
                    );

                    for (const item of response.data.items) {
                        const player: Player = { ...item.player };
                        player.signedPhotoUrl = item.signedPhotoUrl;
                        receivedPlayers.push(player);
                    }

                    setTeamPlayers(receivedPlayers);
                }
            } catch (error) {
                handleError(error, "Error fetching team players");
            }
        };

        fetchTeamPlayers();
    }, [teamId]);

    return (
        <Layout>
            <div className={styles.pageDiv}>
                {team && teamPlayers ? (
                    <div className={styles.teamAndStadium}>
                        <div className={styles.teamDiv}>
                            <div className={styles.BadgeAndDetails}>
                                <img
                                    src={team.signedPhotoUrl}
                                    alt={`ID ${team.id}`}
                                    className={styles.teamBadge}
                                />
                                <div className={styles.teamGeneralDetails}>
                                    <h1>{team.teamName}</h1>
                                    <hr className={styles.nameHr}></hr>
                                    <div className={styles.moreTeamDetails}>
                                        <div>
                                            <CalendarMonthIcon></CalendarMonthIcon>
                                            Founded:{" "}
                                            <span
                                                style={{
                                                    fontWeight: "normal",
                                                    fontStyle: "italic",
                                                }}
                                            >
                                                {team.founded}
                                            </span>
                                        </div>
                                        <div>
                                            <PublicIcon></PublicIcon>
                                            Country:{" "}
                                            <span
                                                style={{
                                                    fontWeight: "normal",
                                                    fontStyle: "italic",
                                                }}
                                            >
                                                {team.country}
                                            </span>
                                            <CustomCountryFlag
                                                nationality={team.country}
                                                height="26px"
                                                width="34px"
                                            ></CustomCountryFlag>
                                        </div>
                                        {stadium && (
                                            <div>
                                                <LocationCityIcon></LocationCityIcon>{" "}
                                                City:{" "}
                                                <span
                                                    style={{
                                                        fontWeight: "normal",
                                                        fontStyle: "italic",
                                                    }}
                                                >
                                                    {stadium.city}
                                                </span>
                                            </div>
                                        )}
                                        {stadium && (
                                            <div>
                                                <StadiumIcon></StadiumIcon>{" "}
                                                Stadium:{" "}
                                                <span
                                                    style={{
                                                        fontWeight: "normal",
                                                        fontStyle: "italic",
                                                    }}
                                                >
                                                    {stadium.stadiumName}
                                                </span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                            <hr className={styles.teamDetailsHr}></hr>
                            <h1 className={styles.squadTitle}>Team Squad</h1>
                            <ul className={styles.playerList}>
                                {teamPlayers.map((player) => (
                                    <li key={player.id} onClick={() => {}}>
                                        <div
                                            className={styles.playerContainer}
                                            onClick={() =>
                                                handlePlayerNavigation(
                                                    player.id
                                                )
                                            }
                                        >
                                            <div
                                                className={
                                                    styles.positionAndName
                                                }
                                            >
                                                <PositionComponent
                                                    fieldPosition={
                                                        player.fieldPosition
                                                    }
                                                ></PositionComponent>
                                                <span
                                                    style={{
                                                        fontWeight: "600",
                                                        minWidth: "150px",
                                                    }}
                                                >
                                                    {player.fullName}
                                                </span>
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
                                            <div className={styles.moreInfo}>
                                                <span
                                                    style={{
                                                        fontWeight: "800",
                                                        fontSize: "18px",
                                                    }}
                                                >
                                                    More{" "}
                                                </span>
                                                <InfoIcon></InfoIcon>
                                            </div>
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                        <div className={styles.verticalLine}></div>
                        <div className={styles.stadiumDiv}>
                            <img
                                src={stadium?.signedPhotoUrl}
                                alt={`ID ${team.id}`}
                                className={styles.stadiumPhoto}
                            />
                            <h1>{stadium?.stadiumName}</h1>
                            <hr className={styles.stadiumNameHr}></hr>
                            <div className={styles.moreStadiumDetails}>
                                <div>
                                    <LocationOnIcon></LocationOnIcon>
                                    <span>
                                        Address:{" "}
                                        <span
                                            style={{
                                                fontWeight: "normal",
                                                fontStyle: "italic",
                                            }}
                                        >
                                            {stadium?.address}, {stadium?.city}
                                        </span>
                                    </span>
                                </div>
                                <div>
                                    <GroupsIcon></GroupsIcon>
                                    <span>
                                        Capacity:{" "}
                                        <span
                                            style={{
                                                fontWeight: "normal",
                                                fontStyle: "italic",
                                            }}
                                        >
                                            {stadium?.stadiumCapacity} seats
                                        </span>
                                    </span>
                                </div>
                                <div>
                                    <GrassIcon></GrassIcon>
                                    <span>
                                        Surface:{" "}
                                        <span
                                            style={{
                                                fontWeight: "normal",
                                                fontStyle: "italic",
                                            }}
                                        >
                                            {stadium?.surface}
                                        </span>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
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

export default TeamPage;
