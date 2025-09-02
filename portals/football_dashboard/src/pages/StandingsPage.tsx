import React, { ChangeEvent, useEffect, useState } from 'react'
import Layout from '../components/Layout'
import styles from './StandingsPage.module.css'
import axios from 'axios';
import { toast } from 'react-toastify';
import environment from '../environment';
import { TopScorer, Standing, Team, Player } from '../models/interfaces';
import { BallTriangle } from 'react-loader-spinner';
import { useNavigate } from 'react-router-dom';

const StandingsPage: React.FC = () => {
    const [standings, setStandings] = useState<Standing[]>();
    const [topScorers, setTopScorers] = useState<TopScorer[]>();
    const [topScorerPlayers, setTopScorerPlayers] = useState<Player[]>();
    const [isLoading, setIsLoading] = useState(false);
    const [teams, setTeams] = useState<Team[]>([]);
    const [selectedOption, setSelectedOption] = useState<string>('table');

    const navigate = useNavigate();

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
        const fetchStandings = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballStandings`,
                    {
                        ...environment.params
                    }
                );
                setStandings(response.data.items);
            }  catch (error) {
                handleError(error, 'Error fetching standings');
            }
        };

        const fetchTopScorers = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballTopScorers`,
                    {
                        ...environment.params
                    }
                );
                setTopScorers(response.data.items);
            }  catch (error) {
                handleError(error, 'Error fetching top scorers');
            }
        };

        setIsLoading(true);
        fetchStandings();
        fetchTopScorers();
        setIsLoading(false);
    }, []);

    useEffect(() => {
        const fetchTeams = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballTeams`,
                    {
                        ...environment.params
                    }
                );
                let receivedTeams: Team[] = [];

                for (const item of response.data.items) {
                const team: Team = { ...item.team };
                team.signedPhotoUrl = item.signedPhotoUrl
                receivedTeams.push(team)
                }

                setTeams(receivedTeams);
            }  catch (error) {
                handleError(error, 'Error fetching teams');
            }
        };

        const fetchPlayers = async () => {
            try {
                if (topScorers) {
                    let receivedPlayers: Player[] = [];
                    const playerIdsString = topScorers
                        .map((scorer) => scorer.player_id)
                        .join(",");

                    console.log("players " + topScorers[0].player_id)

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

                        setTopScorerPlayers(receivedPlayers);
                    }
                }
            } catch (error) {
                handleError(error, "Error fetching players that scored");
            }
        };

        setIsLoading(true);
        fetchTeams();
        fetchPlayers();
        setIsLoading(false);
    }, [standings, topScorers]);

    const handleChange = (event: ChangeEvent<HTMLSelectElement>) => {
        setSelectedOption(event.target.value);
    };

    const standingsTeamIds = standings?.map((standing) => standing.team_id).filter(Boolean) || [];
    const missingTeams = teams.filter((team) => !standingsTeamIds.includes(team.id ?? -1));

    const completeStandingsList = [
      ...(standings || []).filter((standing) => standing.team_id !== undefined),
      ...missingTeams.map((team, index) => ({
        team_id: team.id,
        position: (standings?.length || 0) + index + 1,
        points: 0,
        goalsScored: 0,
        goalsConceded: 0,
        gamesPlayed: 0,
      })),
    ];

    // Sort the complete list by position
    completeStandingsList.sort((a, b) => a.position - b.position);

    const handleTeamNavigation = (teamId: number | undefined) => {
        if (teamId) {
          navigate(`/teams/${teamId}`);
        }
    };

    const handlePlayerNavigation = (playerId: number | undefined) => {
        if (playerId) {
          navigate(`/players/${playerId}`);
        }
    };

    return (
        <Layout>
            <h1 className={styles.heading}>Standings</h1>
            <div className={styles.pageDiv}>
                <label htmlFor="viewDropdown" className={styles.viewDropdown}>Choose View: </label>
                <select id="viewDropdown" value={selectedOption} onChange={handleChange} className={styles.viewSelect}>
                    <option value="table" className={styles.viewSelect}>Table</option>
                    <option value="top-scorers">Top Scorers</option>
                </select>

                {selectedOption === 'table' ? (
                    !isLoading && standings ? (
                        <ul className={styles.standingsList}>
                            {completeStandingsList.map((standing, index) => (
                                <li key={index} className={styles.standingItem} onClick={() => handleTeamNavigation(standing.team_id)}>
                                    <div className={styles.teamInfo}>
                                        <div className={styles.positionInfo}>
                                            <strong>Pos. </strong>
                                            <div className={styles.position}>{standing.position}</div>
                                        </div>
                                        <div className={styles.teamNameAndBadge}>
                                            <strong>Team: </strong>
                                            <img src={teams.find((team) => team.id === standing.team_id)?.signedPhotoUrl} alt="Team " className={styles.teamPhoto} />
                                            <div className={styles.teamName}>{teams.find((team) => team.id === standing.team_id)?.teamName}</div>
                                        </div>
                                    </div>
                                    <div className={styles.standingDetails}>
                                        <div className={styles.standingDetail}>
                                            <strong title="Goals Scored">GS:</strong>
                                            <div>{standing.goalsScored}</div>
                                        </div>
                                        <div className={styles.standingDetail}>
                                            <strong title="Goals Conceded">GC: </strong>
                                            <div>{standing.goalsConceded}</div>
                                        </div>
                                        <div className={styles.standingDetail}>
                                            <strong title="Games Played">GP: </strong>
                                            <div>{standing.gamesPlayed}</div>
                                        </div>
                                        <div className={styles.standingDetail}>
                                            <strong>Points: </strong>
                                            <div className={styles.points}>{standing.points}</div>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
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
                    )
                ) : (
                    <ul className={styles.standingsList}>
                        {(topScorers && topScorerPlayers) ? topScorers.map((scorer, index) => (
                            <li key={index} className={styles.playerItem}  onClick={() => handlePlayerNavigation(scorer.player_id)}>
                                <div className={styles.scorerInfo}>
                                    <span className={styles.position} style={{color: 'white', width: '60px'}}>{index + 1}.</span>
                                    <div className={styles.playerNameAndPhoto}>
                                        <img src={topScorerPlayers.find(player => player.id! === scorer.player_id)?.signedPhotoUrl} alt="Player" className={styles.playerPhoto} />
                                        <span className={styles.playerName}> {topScorerPlayers.find(player => player.id! === scorer.player_id)?.fullName}</span>
                                    </div>
                                    <div className={styles.teamDetails}>
                                        <img src={teams.find(team => topScorerPlayers.find(player => player.id! === scorer.player_id)?.teamId === team.id)?.signedPhotoUrl} alt="Team Badge" className={styles.teamBadge} />
                                        <span className={styles.teamNameTopScorers}>{teams.find(team => topScorerPlayers.find(player => player.id! === scorer.player_id)?.teamId === team.id)?.teamName}</span>
                                    </div>
                                </div>
                                <span className={styles.goalsScored}>{scorer.goals_scored} <span style={{ color:'white', fontSize:'large', opacity:'0.6' }}>goal(s)</span></span>
                            </li>
                        )) :
                        <span
                            style={{
                                fontWeight: "600",
                                color: "#434343",
                                fontSize: "large",
                            }}
                        >
                            No scorers. Boring.
                        </span>
                        }
                    </ul>
                )}
            </div>
        </Layout>
    );
}

export default StandingsPage