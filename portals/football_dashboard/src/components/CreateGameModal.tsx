import React, { useEffect, useState } from 'react';
import styles from './CreateGameModal.module.css';
import { Game, Player, Scorer, ScorerOutput, Team } from '../models/interfaces';
import environment from '../environment';
import axios from 'axios';
import SportsSoccerIcon from '@mui/icons-material/SportsSoccer';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import AddGoalForm from './AddGoalForm';
import { toast } from 'react-toastify';
import PositionComponent from './PositionComponent';

interface CreateGameModalProps {
    show: boolean;
    onClose: () => void;
    onCreate: (newGame: Game) => void;
    games: Game[];
    teams: Team[];
}

const CreateGameModal: React.FC<CreateGameModalProps> = ({ show, onClose, onCreate, games, teams }) => {
    const [firstTeamId, setFirstTeamId] = useState<number | null>(null);
    const [firstTeam, setFirstTeam] = useState<Team | null>(null);
    const [secondTeamId, setSecondTeamId] = useState<number | null>(null);
    const [secondTeam, setSecondTeam] = useState<Team | null>(null);
    const [firstTeamScore, setFirstTeamScore] = useState<number>(0);
    const [secondTeamScore, setSecondTeamScore] = useState<number>(0);
    const [gameDateAndTime, setGameDateAndTime] = useState<string>("");
    const [firstTeamPlayers, setFirstTeamPlayers] = useState<Player[]>([]);
    const [secondTeamPlayers, setSecondTeamPlayers] = useState<Player[]>([]);
    const [firstTeamScorers, setFirstTeamScorers] = useState<Scorer[]>([]);
    const [secondTeamScorers, setSecondTeamScorers] = useState<Scorer[]>([]);
    const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
    const [selectedScorer, setSelectedScorer] = useState<Scorer | null>(null);
    const [showUpdatePlayersGoalsCountModal, setShowUpdatePlayersGoalsCountModal] = useState(false);

    useEffect(() => {
        setFirstTeamScorers([]);

        const fetchFirstTeamPlayers = async () => {
            try {
                if (firstTeamId) {
                    let receivedPlayers: Player[] = [];

                    const response = await axios.get(
                        `${environment.apiPath}footballPlayers`,
                        {
                            params: {
                                teamId: firstTeamId,
                            },
                            ...environment.params
                        }
                    );

                    for (const item of response.data.items) {
                        const player: Player = { ...item.player };
                        player.signedPhotoUrl = item.signedPhotoUrl;
                        receivedPlayers.push(player);
                    }

                    setFirstTeamPlayers(receivedPlayers);
                }
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        toast.error(`Error fetching players: ${error.response.data?.error || error.response.statusText}`);
                    } else if (error.request) {
                        toast.error('No response received from the server when trying to fetch players.');
                    } else {
                        toast.error(`Error setting up request when trying to fetch players.: ${error.message}`);
                    }
                } else {
                    toast.error(`An unexpected error occurred when trying to fetch players.: ${error}`);
                }
            }
        };

        fetchFirstTeamPlayers();
    }, [firstTeamId]);

    useEffect(() => {
        setSecondTeamScorers([]);

        const fetchSecondTeamPlayers = async () => {
            try {
                if (secondTeamId) {
                    let receivedPlayers: Player[] = [];

                    const response = await axios.get(
                        `${environment.apiPath}footballPlayers`,
                        {
                            params: {
                                teamId: secondTeamId,
                            },
                            ...environment.params
                        }
                    );

                    for (const item of response.data.items) {
                        const player: Player = { ...item.player };
                        player.signedPhotoUrl = item.signedPhotoUrl;
                        receivedPlayers.push(player);
                    }

                    setSecondTeamPlayers(receivedPlayers);
                }
            } catch (error) {
                if (axios.isAxiosError(error)) {
                    if (error.response) {
                        toast.error(`Error fetching players: ${error.response.data?.error || error.response.statusText}`);
                    } else if (error.request) {
                        toast.error('No response received from the server when trying to fetch players.');
                    } else {
                        toast.error(`Error setting up request when trying to fetch players.: ${error.message}`);
                    }
                } else {
                    toast.error(`An unexpected error occurred when trying to fetch players.: ${error}`);
                }
            }
        };

        fetchSecondTeamPlayers();
    }, [secondTeamId]);

    useEffect(() => {
        if (selectedPlayer) {
          const selectedScorer =
            firstTeamScorers.find(scorer => scorer.player.id === selectedPlayer.id) ||
            secondTeamScorers.find(scorer => scorer.player.id === selectedPlayer.id);

          if (selectedScorer) {
            setSelectedScorer(selectedScorer)
          }
          else {
            setSelectedScorer(null);
          }
        }

        let totalGoals = firstTeamScorers.reduce((sum, scorer) => sum + scorer.minutes.length, 0);
        setFirstTeamScore(totalGoals);

        totalGoals = secondTeamScorers.reduce((sum, scorer) => sum + scorer.minutes.length, 0);
        setSecondTeamScore(totalGoals);
      }, [firstTeamScorers, secondTeamScorers, selectedPlayer]);


    const handleSubmit = () => {
        if (firstTeamId !== null && secondTeamId !== null && gameDateAndTime !== "") {
            const scorers: ScorerOutput[] = [
                ...firstTeamScorers.map((scorer) => ({
                  playerId: scorer.player.id,
                  teamId: scorer.player.teamId,
                  minutes: scorer.minutes,
                })),
                ...secondTeamScorers.map((scorer) => ({
                  playerId: scorer.player.id,
                  teamId: scorer.player.teamId,
                  minutes: scorer.minutes,
                })),
            ];

            const newGame: Game = {
                firstTeamId,
                secondTeamId,
                firstTeamScore,
                secondTeamScore,
                gameDateAndTime,
                scorers,
            };
            resetStates();
            onCreate(newGame);
        }
    };

    const resetStates = () => {
        setFirstTeamId(null);
        setSecondTeamId(null);
        setGameDateAndTime("");
        setFirstTeam(null);
        setSecondTeam(null);
        setFirstTeamPlayers([]);
        setSecondTeamPlayers([]);
    }

    const getTeamOptions = (isFirstTeam: boolean) => {
        return teams.map(team =>
        <option key={team.id} value={team.id} disabled={isFirstTeam ? secondTeamId === team.id : firstTeamId === team.id}>
            {team.teamName}
        </option>);
    };

    const handlePlayerClick = (player: Player) => {
        setShowUpdatePlayersGoalsCountModal(true);
        setSelectedPlayer(player);

        const selectedScorer =
            firstTeamScorers.find(scorer => scorer.player.id === player.id) ||
            secondTeamScorers.find(scorer => scorer.player.id === player.id);

        if (selectedScorer) {
            setSelectedScorer(selectedScorer);
        }
    };


    const onClosePlayerGoals = () => {
        setShowUpdatePlayersGoalsCountModal(false);
        setSelectedPlayer(null);
        setSelectedScorer(null);
    }

    const addGoal = (minute: number, setFunction: React.Dispatch<React.SetStateAction<Scorer[]>>) => {
        if (selectedPlayer) {
            setFunction(prevScorers => {
                const scorerIndex = prevScorers.findIndex(scorer => scorer.player.id === selectedPlayer.id);

                if (scorerIndex !== -1) {
                    // Player has scored before, so update the minutes array
                    const updatedScorers = [...prevScorers];
                    updatedScorers[scorerIndex] = {
                        player: updatedScorers[scorerIndex].player,
                        minutes: [...updatedScorers[scorerIndex].minutes, minute],
                    };
                    return updatedScorers;
                } else {
                    // Player hasn't scored before, so add a new scorer object
                    return [...prevScorers, { player: selectedPlayer, minutes: [minute] }];
                }
            });
        }
        else {
            console.warn('No player selected.');
        }
    }

    const removeGoal = (minuteToRemove: number, setFunction: React.Dispatch<React.SetStateAction<Scorer[]>>) => {
        if (selectedPlayer) {
            setFunction(prevScorers => {
                const scorerIndex = prevScorers.findIndex(scorer => scorer.player.id === selectedPlayer.id);

                if (scorerIndex !== -1) {
                    const updatedScorers = [...prevScorers];
                    const updatedMinutes = [...updatedScorers[scorerIndex].minutes];

                    const minuteIndex = updatedMinutes.indexOf(minuteToRemove);

                    if (minuteIndex !== -1) {
                        updatedMinutes.splice(minuteIndex, 1);

                        if (updatedMinutes.length > 0) {
                            updatedScorers[scorerIndex] = {
                                player: updatedScorers[scorerIndex].player,
                                minutes: updatedMinutes,
                            };
                        } else {
                            updatedScorers.splice(scorerIndex, 1);
                        }

                        return updatedScorers;
                    }
                }

                return prevScorers;
            });
        }
    };

    if (!show) {
        return null;
    }

    const currentDateTime = new Date().toLocaleString('sv-SE', {
        timeZone: 'Europe/Bucharest',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    }).replace(' ', 'T');

    const handleDateTimeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedDateTime = e.target.value;

        if (selectedDateTime > currentDateTime) {
            alert("You cannot select a future date or time.");
            return;
        }

        setGameDateAndTime(selectedDateTime);
    };

    const firstTeamScorerIds = new Set(firstTeamScorers.map(scorer => scorer.player.id));
    const secondTeamScorerIds = new Set(secondTeamScorers.map(scorer => scorer.player.id));

    const nonScorerFirstTeamPlayers = firstTeamPlayers.filter(player => !firstTeamScorerIds.has(player.id));
    const nonScorerSecondTeamPlayers = secondTeamPlayers.filter(player => !secondTeamScorerIds.has(player.id));

    const isCreateButtonDisabled = firstTeamId === null || secondTeamId === null || gameDateAndTime === "";

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modal}>
                <h1 className={styles.header}>Create Game</h1>
                <div className={styles.teamsContainer}>
                    <div className={styles.team}>
                        {!firstTeam ?
                            <img src={"/assets/no-badge.png"} alt="First Team Badge" className={styles.teamBadge} /> :
                            <img src={firstTeam.signedPhotoUrl} alt="First Team Badge" className={styles.teamBadge} />}
                        <select
                            value={firstTeamId ?? ''}
                            onChange={(e) => {
                                const selectedTeamId = Number(e.target.value);
                                setFirstTeamId(selectedTeamId);

                                const selectedTeam = teams.find(team => team.id === selectedTeamId);
                                if (selectedTeam) {
                                    setFirstTeam(selectedTeam);
                                }
                            }}
                            className={styles.teamSelect}
                        >
                            <option value="" disabled>Select a team</option>
                            {getTeamOptions(true)}
                        </select>
                        <div className={styles.teamScore}>
                            {firstTeamScore}
                        </div>
                    </div>
                    <span className={styles.scoreSeparator}>-</span>
                    <div className={styles.team}>
                        <div className={styles.teamScore}>
                            {secondTeamScore}
                        </div>
                        <select
                            value={secondTeamId ?? ''}
                            onChange={(e) => {
                                const selectedTeamId = Number(e.target.value);
                                setSecondTeamId(selectedTeamId);

                                const selectedTeam = teams.find(team => team.id === selectedTeamId);
                                if (selectedTeam) {
                                    setSecondTeam(selectedTeam);
                                }
                            }}
                            className={styles.teamSelect}
                        >
                            <option value="" disabled>Select a team</option>
                            {getTeamOptions(false)}
                        </select>
                        {!secondTeam ?
                            <img src={"/assets/no-badge.png"} alt="First Team Badge" className={styles.teamBadge} /> :
                            <img src={secondTeam.signedPhotoUrl} alt="First Team Badge" className={styles.teamBadge} />}
                    </div>
                </div>
                <div className={styles.formGroup}>
                    <h2>Game Date and Time</h2>
                    <input
                        type="datetime-local"
                        value={gameDateAndTime}
                        onChange={handleDateTimeChange}
                        max={currentDateTime}
                        className={styles.dateTimeInput}
                    />
                </div>
                <div className={styles.playersContainer}>
                    <div className={styles.playersList}>
                        {firstTeam && <h2>Who scored for {firstTeam.teamName}?</h2>}
                        {firstTeam && <h4>(Click on a player to add or remove a goal)</h4>}

                        <ul className={styles.playerList}>
                            {firstTeamScorers.map(scorer => (
                                <li key={scorer.player.id} onClick={() => handlePlayerClick(scorer.player)} >
                                    <div className={styles.scorerContainer}>
                                        <div className={styles.positionAndName}>
                                            <PositionComponent fieldPosition={scorer.player.fieldPosition}></PositionComponent>
                                            <span>{scorer.player.fullName}</span>
                                        </div>
                                        <div className={styles.scoreContainer}>
                                            <span>
                                                {scorer.minutes.length}
                                                <SportsSoccerIcon fontSize='inherit'  style={{ marginLeft: '2px' }} />
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                            {nonScorerFirstTeamPlayers.map(player => (
                                <li key={player.id} onClick={() => handlePlayerClick(player)} >
                                    <div className={styles.playerContainer}>
                                        <div className={styles.positionAndName}>
                                            <PositionComponent fieldPosition={player.fieldPosition}></PositionComponent>
                                            <span>{player.fullName}</span>
                                        </div>
                                        <div className={styles.scoreContainer}>
                                            <span>
                                                0
                                                <SportsSoccerIcon fontSize='inherit'  style={{ marginLeft: '2px' }} />
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className={styles.playersList}>
                        {secondTeam && <h2>Who scored for {secondTeam.teamName}?</h2>}
                        {secondTeam && <h4>(Click on a player to add or remove a goal)</h4>}

                        <ul className={styles.playerList}>
                            {secondTeamScorers.map(scorer => (
                                <li key={scorer.player.id} onClick={() => handlePlayerClick(scorer.player)} >
                                    <div className={styles.scorerContainer}>
                                        <div className={styles.positionAndName}>
                                            <PositionComponent fieldPosition={scorer.player.fieldPosition}></PositionComponent>
                                            <span>{scorer.player.fullName}</span>
                                        </div>
                                        <div className={styles.scoreContainer}>
                                            <span>
                                                {scorer.minutes.length}
                                                <SportsSoccerIcon fontSize='inherit'  style={{ marginLeft: '2px' }} />
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                            {nonScorerSecondTeamPlayers.map(player => (
                                <li key={player.id} onClick={() => handlePlayerClick(player)} >
                                    <div className={styles.playerContainer}>
                                        <div className={styles.positionAndName}>
                                            <PositionComponent fieldPosition={player.fieldPosition}></PositionComponent>
                                            <span>{player.fullName}</span>
                                        </div>
                                        <div className={styles.scoreContainer}>
                                            <span>
                                                0
                                                <SportsSoccerIcon fontSize='inherit'  style={{ marginLeft: '2px' }} />
                                            </span>
                                        </div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className={styles.buttons}>
                    <button
                        className={styles.confirmButton}
                        onClick={handleSubmit}
                        disabled={isCreateButtonDisabled}
                        title={isCreateButtonDisabled ? "We need both teams and the date set" : ""}
                    >
                        Create
                    </button>
                    <button
                        className={styles.cancelButton}
                        onClick={() => {
                            onClose();
                            resetStates();
                        }}
                    >
                        Cancel
                    </button>
                </div>
            </div>
            {showUpdatePlayersGoalsCountModal &&
                <div className={styles.modalOverlay}>
                    <div className={styles.playerGoalsModal}>
                        <h2>How many goals did {selectedPlayer?.fullName} score?</h2>
                        <div className={styles.playerPhotoAndGoals}>
                            <img src={selectedPlayer?.signedPhotoUrl} alt={`player: ${selectedPlayer?.fullName}`} className={styles.playerPhoto} />
                            <div className={styles.playerGoals}>
                                <div className={styles.scoreContainer}>
                                    <span>Goals scored: {selectedScorer?.minutes ? selectedScorer?.minutes.length : 0} </span>
                                </div>
                                <div className={styles.minutesContainer}>
                                    {selectedScorer?.minutes.map((minute, index) => (
                                        <button
                                            key={index}
                                            className={styles.minuteButton}
                                            onClick={() => removeGoal(minute, selectedPlayer?.teamId === firstTeamId ? setFirstTeamScorers : setSecondTeamScorers)}
                                        >
                                            <div key={index} className={styles.minuteItem}>
                                                '{minute}
                                                <DeleteForeverIcon/>
                                            </div>
                                        </button>
                                    ))}
                                </div>
                                <AddGoalForm onAddGoal={addGoal} setFunction={ selectedPlayer?.teamId === firstTeamId ? setFirstTeamScorers : setSecondTeamScorers}/>

                            </div>
                        </div>
                        <div className={styles.playerGoalsButtons}>
                            {/* <button className={styles.confirmButton} onClick={handleConfirmPlayerGoals}>Confirm</button> */}
                            <button className={styles.cancelButton} onClick={onClosePlayerGoals}>Close</button>
                        </div>
                    </div>
                </div>
            }
        </div>
    );
};

export default CreateGameModal;
