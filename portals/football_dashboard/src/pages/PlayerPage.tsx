import axios from 'axios';
import React, { useEffect, useState } from 'react'
import styles from "./PlayerPage.module.css"
import { Link, useParams } from 'react-router-dom';
import { toast } from 'react-toastify';
import { Player, Team } from '../models/interfaces';
import environment from '../environment';
import Layout from '../components/Layout';
import KeyboardDoubleArrowUpIcon from '@mui/icons-material/KeyboardDoubleArrowUp';
import CustomCountryFlag from '../components/CustomCountryFlag';
import MyLocationIcon from '@mui/icons-material/MyLocation';
import Diversity3Icon from '@mui/icons-material/Diversity3';
import HeightIcon from '@mui/icons-material/Height';
import ScaleIcon from '@mui/icons-material/Scale';
import { BallTriangle } from 'react-loader-spinner';

const PlayerPage: React.FC = () => {
    const [player, setPlayer] = useState<Player>();
    const [team, setTeam] = useState<Team>();
    const { playerId } = useParams<{ playerId: string }>();
    const [imagesLoaded, setImagesLoaded] = useState(false);

    const handleError = (error: unknown, context: string) => {
        if (axios.isAxiosError(error)) {
            if (error.response) {
                toast.error(`${context}: ${error.response.data?.error || error.response.statusText}`);
            } else if (error.request) {
                toast.error(`${context}: No response received from the server.`);
            } else {
                toast.error(`${context}: Error setting up request: ${error.message}`);
            }
        } else {
            toast.error(`${context}: An unexpected error occurred: ${error}`);
        }
    };

    useEffect(() => {
        const fetchPlayer = async () => {
            try {
                if (playerId) {

                    const response = await axios.get(
                        `${environment.apiPath}footballPlayers`,
                        {
                            params: {
                                id: playerId,
                            },
                            ...environment.params
                        }
                    );

                    const receivedPlayer: Player = { ...response.data.items[0].player };
                    receivedPlayer.signedPhotoUrl = response.data.items[0].signedPhotoUrl;

                    setPlayer(receivedPlayer);
                }
            }  catch (error) {
              handleError(error, 'Error fetching player');
            }
        };

        fetchPlayer();
    }, [playerId]);

    useEffect(() => {
        const fetchTeam = async () => {
            try {
              const response = await axios.get(
                `${environment.apiPath}footballTeams`,

                {
                    params: {
                        id: player?.teamId  ,
                    },
                  ...environment.params
                }
              );

              const receivedTeam: Team = { ...response.data.items[0].team };
              receivedTeam.signedPhotoUrl = response.data.items[0].signedPhotoUrl

              setTeam(receivedTeam);
            } catch (error) {
              handleError(error, 'Error fetching team');
            }
        };

        if (player) {
            fetchTeam();
        }
    }, [player]);

    const getFieldPositionClass = (fieldPosition: string) => {
        switch (fieldPosition) {
          case 'Defender':
            return styles.defenderArea;
          case 'Midfielder':
            return styles.midfielderArea;
          case 'Attacker':
            return styles.attackerArea;
          case 'Goalkeeper':
            return styles.gkArea;
          default:
            return '';
        }
      };

    const handleImageLoad = () => {
    if (imagesLoaded) return;
    setImagesLoaded(true);
    };


    return (
        <Layout>
            <div className={styles.pageDiv}>
                {player && team ?
                    (
                    <div className={styles.playerDiv}>
                        <div className={styles.playerOverview}>
                            <div className={styles.playerPhotoAndName}>
                                <img src={player.signedPhotoUrl} alt="Player " className={styles.playerPhoto} onLoad={handleImageLoad} />
                                <span className={styles.playerName}>{player.fullName}</span>
                                <Link to={`/teams/${team?.id}`} className={styles.teamLink}>
                                    <img src={team?.signedPhotoUrl} alt="Team " className={styles.teamPhoto} onLoad={handleImageLoad} />
                                </Link>
                            </div>
                            <div className={styles.playerDetails}>
                                <div className={styles.playerDetailsColumn}>
                                    <div className={styles.playerDetail}>
                                        <div style={{ fontWeight: 'bold', width: '200px' }}>First name: </div>
                                        <div className={styles.playerDetailText} title={player.firstName}>
                                            {player.firstName}</div>
                                        </div>
                                    <div className={styles.playerDetail} title={player.fullName}>
                                        <div style={{ fontWeight: 'bold', width: '200px' }}>Full name: </div>
                                        <div className={styles.playerDetailText}>
                                            {player.fullName}
                                        </div>
                                    </div>
                                    <div className={styles.playerDetail}>
                                        <div style={{ fontWeight: 'bold', width: '200px' }}>Age: </div>
                                        <div className={styles.playerDetailText}>
                                            {player.age} y.o.
                                        </div>
                                    </div>
                                    <div className={styles.playerDetail}>
                                        <div style={{ fontWeight: 'bold', width: '200px'}}>Nationality: </div>
                                        <div className={styles.playerDetailText} title={player.nationality}>
                                            {player.nationality}
                                            <CustomCountryFlag nationality={player.nationality} height='26px' width='34px'></CustomCountryFlag>
                                        </div>
                                    </div>
                                </div>
                                <div className={styles.playerDetailsColumn}>
                                    <div className={styles.playerDetail}>
                                        <MyLocationIcon className={styles.playerDetailIcon} />
                                        <div style={{ fontWeight: 'bold', width: '150px' }}>Position: </div>
                                        <div className={styles.playerDetailText}>
                                            {player.fieldPosition !== "" ? player.fieldPosition : "-"}
                                        </div>
                                    </div>
                                    <div className={styles.playerDetail}>
                                        <Diversity3Icon className={styles.playerDetailIcon} />
                                        <div style={{ fontWeight: 'bold', width: '150px' }}>Team: </div>
                                        <div className={styles.playerDetailText}>
                                            {team?.teamName ? team.teamName : "-"}
                                        </div>
                                    </div>
                                    <div className={styles.playerDetail}>
                                        <HeightIcon className={styles.playerDetailIcon} />
                                        <div style={{ fontWeight: 'bold', width: '150px' }}>Height: </div>
                                        <div className={styles.playerDetailText}>
                                            {player.height !== "" ? player.height : "-"}
                                        </div>
                                    </div>
                                    <div className={styles.playerDetail}>
                                        <ScaleIcon className={styles.playerDetailIcon} />
                                        <div style={{ fontWeight: 'bold', width: '150px' }}>Weight: </div>
                                        <div className={styles.playerDetailText}>
                                            {player.weight !== "" ? player.weight : "-"}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className={styles.heatmap}>
                            <div className={styles.verticalLine}></div>
                                <div className={styles.heatmapTitleAndContent}>
                                    <h1 className={styles.heatmapTitle}>Heatmap</h1>
                                    <div className={styles.footballPitchAndLegend}>
                                        <div className={styles.footballPitch}>
                                            <img src={"/assets/football_field.png"} alt={`Player ${player.fullName}`}  className={styles.footballPhoto} onLoad={handleImageLoad} />
                                            <div className={`${getFieldPositionClass(player.fieldPosition)} ${styles.commonStyles}`}>{player.fieldPosition}</div>
                                        </div>

                                        <div className={styles.pitchLegend}>
                                            <KeyboardDoubleArrowUpIcon className={styles.attackingDirection}></KeyboardDoubleArrowUpIcon>
                                            <span style={{ fontWeight: 'bolder', fontSize: '18px', opacity: '0.6' }}>Attacking Direction</span>
                                        </div>
                                    </div>
                                </div>
                        </div>
                    </div>) :
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
                }
            </div>
        </Layout>
    )
}

export default PlayerPage