import { ChangeEvent, FormEvent, useState } from "react";

import {
  Dictionary,
  SongItemProps,
  TextInputDataModel,
  UpsertSongModalProps,
} from "../interfaces";

import Button from "../shared/Button";
import Header from "../shared/Header";
import ModalContainer from "../shared/ModalContainer";
import { songFormFields } from "../constants";

import TextInput from "./TextInput";

const setDefaultFormState = (defaultValues: SongItemProps) => {
  return songFormFields.reduce(
    (fieldsDict: Dictionary, currentField: TextInputDataModel) => {
      fieldsDict[currentField.fieldName] =
        defaultValues[currentField.fieldName as keyof SongItemProps] ?? "";
      return fieldsDict;
    },
    { songId: defaultValues["songId"] }
  );
};

const UpsertSongModal = ({
  defaultValues,
  closeModal,
  submitForm,
}: UpsertSongModalProps) => {
  const [formValues, setFormValues] = useState(
    setDefaultFormState(defaultValues)
  );

  const setFormValue = (event: ChangeEvent) => {
    const fieldName = event.target.id;
    const fieldValue = (event.target as HTMLInputElement).value;
    setFormValues((prevState) => ({ ...prevState, [fieldName]: fieldValue }));
  };

  const handleAddSongSubmit = (e: FormEvent) => {
    e.preventDefault();
    submitForm && submitForm(formValues);
    closeModal && closeModal();
  };

  return (
    <ModalContainer>
      <Header
        className="text-lime-700"
        title={defaultValues.songName ? "Edit Song" : "Add Song"}
        level={3}
      />
      <form className="space-y-8" onSubmit={handleAddSongSubmit}>
        <div className="space-y-3">
          {songFormFields.map((field) => (
            <TextInput
              key={field.fieldName}
              fieldName={field.fieldName}
              label={field.label}
              placeholder={field.placeholder}
              value={formValues[field.fieldName]}
              setFormValue={setFormValue}
            />
          ))}
        </div>
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

export default UpsertSongModal;
