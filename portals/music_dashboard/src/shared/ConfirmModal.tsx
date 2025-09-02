import { ConfirmModalProps } from "../interfaces";
import Button from "./Button";
import Header from "./Header";
import ModalContainer from "./ModalContainer";

const ConfirmModal = ({
  headerTitle,
  headerLevel,
  confirmationMessage,
  closeModal,
  confirmAction,
}: ConfirmModalProps) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    confirmAction && confirmAction();
  };
  return (
    <ModalContainer>
      <Header
        className="text-lime-700"
        title={headerTitle}
        level={headerLevel}
      />
      <form className="space-y-8" onSubmit={handleSubmit}>
        <p>{confirmationMessage}</p>
        <div className="flex justify-end space-x-2">
          <Button
            className="ring-1 ring-lime-600 text-lime-700 hover:bg-slate-50"
            label="Close"
            onClick={closeModal}
          />
          <Button
            className="bg-lime-700 text-slate-50 hover:bg-lime-600"
            label="Submit"
          />
        </div>
      </form>
    </ModalContainer>
  );
};

export default ConfirmModal;
