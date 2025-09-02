// src/components/ConfirmModal.tsx
import React from 'react';
import styles from './ConfirmModal.module.css';

interface ConfirmModalProps {
    show: boolean;
    onClose: () => void;
    onConfirm: () => void;
    message: string;
}

const ConfirmModal: React.FC<ConfirmModalProps> = ({ show, onClose, onConfirm, message }) => {
    if (!show) {
        return null;
    }

    return (
        <div className={styles.modalOverlay}>
            <div className={styles.modal}>
                <p>{message}</p>
                <div className={styles.buttons}>
                    <button className={styles.confirmButton} onClick={onConfirm}>Yes</button>
                    <button className={styles.cancelButton} onClick={onClose}>No</button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmModal;
