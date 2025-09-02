import React, {useEffect, useState} from 'react';
import styles from './GameItem.module.css';
import EditIcon from '@mui/icons-material/Edit';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import ConfirmModal from './ConfirmModal';
import UpdateGameModal from './UpdateGameModal';
import { Link, useNavigate } from 'react-router-dom';
import { Game, Team } from '../models/interfaces';


interface GameItemProps {
    game: Game;
    onEdit: (game: Game) => void;
    onDelete: (game: Game) => void;
    games: Game[];
    setGames: React.Dispatch<React.SetStateAction<Game[]>>;
    teams: Team[];
}

const GameItem: React.FC<GameItemProps> = ({ game, onEdit, onDelete, games, setGames, teams }) => {
    const [showModal, setShowModal] = useState(false);
    const [showUpdateModal, setShowUpdateModal] = useState(false);
    const [firstTeam, setFirstTeam] = useState<Team>();
    const [secondTeam, setSecondTeam] = useState<Team>();

    useEffect(() => {
        setFirstTeam(teams.find(team => team.id === game.firstTeamId))
        setSecondTeam(teams.find(team => team.id === game.secondTeamId))
    }, [game, teams]);

    const handleDelete = () => {
        setShowModal(true);
    };

    const handleConfirmDelete = () => {
        setShowModal(false);
        onDelete(game);
    };

    const handleCloseModal = () => {
        setShowModal(false);
    };

    const handleEdit = () => {
        setShowUpdateModal(true);
    };

    const handleConfirmUpdate = (updatedGame: Game) => {
        setShowUpdateModal(false);
        onEdit(updatedGame);
    };

    const handleCloseUpdateModal = () => {
        setShowUpdateModal(false);
    };

    const navigate = useNavigate();

    const handleGameClick = (game: Game) => {
        navigate(`/games/${game.id}`);
    };


    return (
        <div className={styles.gameItem}>
            <Link to={`/games/${game.id}`} className={styles.gameInfoContainer}>
                <div className={styles.gameInfo}>
                    <img src={firstTeam?.signedPhotoUrl} alt={`ID ${game.firstTeamId}`} className={styles.teamBadge} />
                    <p className={styles.teamName}>{`${firstTeam?.code}`}</p>
                    <p className={styles.score}>{`${game.firstTeamScore ?? 0} - ${game.secondTeamScore ?? 0}`}</p>
                    <p className={styles.teamName}>{`${secondTeam?.code}`}</p>
                    <img src={secondTeam?.signedPhotoUrl} alt={`ID ${game.secondTeamId}`} className={styles.teamBadge} />
                    <div>
                        <p className={styles.dateTime}><span className={styles.dateTimeLabel}>Date: </span>{game.gameDateAndTime.split('T')[0]}</p>
                        <p className={styles.dateTime}><span className={styles.dateTimeLabel}>Time: </span>{game.gameDateAndTime.split('T')[1]}</p>
                    </div>
                </div>
            </Link>
            <div className={styles.buttons}>
                <button className={styles.editButton} onClick={handleEdit}><EditIcon/></button>
                <button className={styles.deleteButton} onClick={handleDelete}><DeleteForeverIcon/></button>
            </div>
            <ConfirmModal
                show={showModal}
                onClose={handleCloseModal}
                onConfirm={handleConfirmDelete}
                message="Are you sure you want to delete this game?"
            />
            <UpdateGameModal
                show={showUpdateModal}
                onClose={handleCloseUpdateModal}
                onUpdate={handleConfirmUpdate}
                game={game}
                games={games}
                teams={teams}
            />
        </div>
    );
};

export default GameItem;
