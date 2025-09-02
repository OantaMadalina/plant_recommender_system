import React, { useEffect, useState } from "react";
import GameItem from "./GameItem";
import styles from "./GameList.module.css";
import CreateGameModal from "./CreateGameModal";
import axios from "axios";
import environment from "../environment";
import { Game, Team } from "../models/interfaces";
import { toast } from "react-toastify";
import { BallTriangle } from "react-loader-spinner";

const GameList: React.FC = () => {
    const [games, setGames] = useState<Game[]>([]);
    const [teams, setTeams] = useState<Team[]>([]);
    const [showCreateModal, setShowCreateModal] = useState(false);

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
        const fetchGames = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballGames`,
                    {
                        ...environment.params,
                    }
                );
                console.log(response.data);
                setGames(response.data.items);
            } catch (error) {
                handleError(error, "Error fetching games");
            }
        };

        const fetchTeams = async () => {
            try {
                const response = await axios.get(
                    `${environment.apiPath}footballTeams`,
                    {
                        ...environment.params,
                    }
                );
                let receivedTeams: Team[] = [];

                for (const item of response.data.items) {
                    const team: Team = { ...item.team };
                    team.signedPhotoUrl = item.signedPhotoUrl;
                    receivedTeams.push(team);
                }

                setTeams(receivedTeams);
            } catch (error) {
                handleError(error, "Error fetching teams");
            }
        };

        fetchGames();
        fetchTeams();
    }, []);

    const handleEdit = async (editedGame: Game) => {
        console.log("Edit game:", editedGame);

        let responseStatus = await editGame(editedGame);

        if (responseStatus) {
            setGames((prevGames) =>
                prevGames.map((game) =>
                    game.id === editedGame.id ? editedGame : game
                )
            );
        }
    };

    const editGame = async (game: Game): Promise<number | void> => {
        try {
            const response = await axios.put(
                `${environment.apiPath}footballGames/${game.id}`,
                game,
                {
                    ...environment.params,
                }
            );

            toast.success("Game updated successfully!");
            return response.status;
        } catch (error) {
            handleError(error, "Error updating game");
        }
    };

    const deleteGame = async (gameId: number): Promise<void> => {
        try {
            const response = await axios.delete(
                `${environment.apiPath}footballGames/${gameId}horse`,
                {
                    ...environment.params,
                }
            );

            toast.success("Game deleted successfully!");
        } catch (error) {
            handleError(error, "Error deleting game");
        }
    };

    const createGame = async (game: Game): Promise<number | void> => {
        try {
            const response = await axios.post(
                `${environment.apiPath}footballGame`,
                game,
                {
                    ...environment.params,
                }
            );

            toast.success("Game created successfully!");
            return response.data.id;
        } catch (error) {
            handleError(error, "Error deleting game");
        }
    };

    const handleDelete = (game: Game) => {
        setGames(games.filter((g) => g !== game));

        deleteGame(game.id!);
    };

    const handleCreate = () => {
        setShowCreateModal(true);
    };

    const handleSubmitCreate = async (newGame: Game) => {
        setShowCreateModal(false);
        let newGameId = await createGame(newGame);
        if (newGameId) {
            newGame.id = newGameId;
            setGames((prevGames) => [...prevGames, newGame]);
        }
    };

    return (
        <div className={styles.gameList}>
            <button className={styles.createButton} onClick={handleCreate}>
                Create Game
            </button>
            {games.length !== 0 ? (
                <>
                    {games.map((game, index) => (
                        <GameItem
                            key={index}
                            game={game}
                            onEdit={handleEdit}
                            onDelete={handleDelete}
                            games={games}
                            setGames={setGames}
                            teams={teams}
                        />
                    ))}
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
            <CreateGameModal
                show={showCreateModal}
                onClose={() => setShowCreateModal(false)}
                onCreate={handleSubmitCreate}
                games={games}
                teams={teams}
            />
        </div>
    );
};

export default GameList;
