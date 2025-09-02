import React from 'react'
import styles from './CreateGameModal.module.css';

interface PositionComponentProps {
    fieldPosition: string | undefined;
}

const PositionComponent: React.FC<PositionComponentProps> = ({ fieldPosition }) => {
    switch (fieldPosition) {
        case "Goalkeeper":
            return (
                <div className={styles.fieldPositionContainer} style={{ backgroundColor: '#a8a899' }}>
                    Gk.
                </div>
            );
        case "Defender":
            return (
                <div className={styles.fieldPositionContainer} style={{ backgroundColor: '#ff8400' }}>
                    {fieldPosition.substring(0, 3)}.
                </div>
            );
        case "Midfielder":
            return (
                <div className={styles.fieldPositionContainer} style={{ backgroundColor: '#196b00' }}>
                    {fieldPosition.substring(0, 3)}.
                </div>
            );
        case "Attacker":
            return (
                <div className={styles.fieldPositionContainer} style={{ backgroundColor: '#011059' }}>
                    {fieldPosition.substring(0, 3)}.
                </div>
            );
        default:
            return (
                <div className={styles.fieldPositionContainer}>
                    Pos.
                </div>
            );
    }
}

export default PositionComponent
