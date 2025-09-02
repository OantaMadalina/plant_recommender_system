import { FormEvent, useState } from "react";
import type { DragEvent, ChangeEvent } from "react";
import axios from "axios";
import { LeafletMouseEvent } from "leaflet";

import Header from "../shared/Header";
import ModalContainer from "../shared/ModalContainer";
import Button from "../shared/Button";
import TextInput from "../libraryPage/TextInput";
import { supportedImageExtensions } from "../constants";
import { addErrorToast, addSuccessToast } from "../utils";
import environment from "../environment";
import { AddLocationPropsHandlers } from "../interfaces";
import ImageUploader from "./ImageUploader";
import MapInput from "./MapInput";

const AddLocationModal = ({
  songId,
  closeModal,
  submitForm,
}: AddLocationPropsHandlers) => {
  const [files, setFiles] = useState<File[]>([]);
  const [validationError, setValidationError] = useState("");
  const [formValues, setFormValues] = useState({
    description: "",
    imagePath: "",
    latitude: "",
    longitude: "",
  });
  const [isImageUploadLoading, setIsImageUploadLoading] = useState(false);

  const getBase64 = async (file: File) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
    });

  const uploadImage = async (file: File) => {
    const filename = `${file.name}-${songId}-${Date.now()}`
    const apiPath = `${environment.apiUrl}/song-locations/upload/${filename}`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    const encodedFile = await getBase64(file);
    try {
      const response = await axios.put(apiPath, encodedFile, {
        ...apiParams,
        headers: {
          ...apiParams.headers,
          Accept: "text/plain",
        },
      });
      addSuccessToast("The image was uploaded successfully");
      const responseData = response.data;
      return responseData;
    } catch (err) {
      addErrorToast(`The image could not be uploaded: ${err}`);
    } finally {
      setIsImageUploadLoading((prevState) => !prevState);
    }
  };

  const handleUpload = async (e: DragEvent | ChangeEvent) => {
    if (
      e.type === "drop" &&
      !(e as DragEvent).dataTransfer &&
      !(e as DragEvent).dataTransfer?.files
    )
      return;
    if (
      e.type === "change" &&
      !e.target &&
      !((e as ChangeEvent).target as HTMLInputElement).files
    )
      return;

    const fileList: FileList | null =
      e.type === "drop" && (e as DragEvent).dataTransfer?.files
        ? (e as DragEvent).dataTransfer.files
        : (e.target as HTMLInputElement).files;

    if (
      fileList &&
      !supportedImageExtensions.has(fileList[0].type.split("/")[1])
    ) {
      setFiles([]);
      setValidationError(
        "Invalid file extension. Supported extensions are: .jpeg, .jpg, .png, .gif"
      );
      return;
    }
    setValidationError("");
    const files = fileList ? Array.from(fileList) : [];
    setFiles(files);

    setIsImageUploadLoading((prevState) => !prevState);
    const imagePath = await uploadImage(files[0]);
    setFormValues((prevState) => ({ ...prevState, imagePath: imagePath }));
  };

  const closeModalHandler = () => {
    setFormValues({
      description: "",
      imagePath: "",
      latitude: "",
      longitude: "",
    });
    setValidationError("");
    setFiles([]);
    closeModal();
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      closeModalHandler();
      submitForm(formValues);
    } catch (err: any) {
      const errorMessage = "The image could not be converted to base64";
      addErrorToast(errorMessage);
    }
  };

  const setCoordinates = (e: LeafletMouseEvent) => {
    setFormValues((prevState) => ({
      ...prevState,
      latitude: e.latlng.lat.toString(),
      longitude: e.latlng.lng.toString(),
    }));
  };

  return (
    <ModalContainer>
      <Header className="text-lime-700" title="Add your spot" level={6} />
      <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
        <TextInput
          label="Description"
          placeholder="Add the spot's description"
          value={formValues.description}
          fieldName="Description"
          setFormValue={(e) =>
            setFormValues((prevState) => ({
              ...prevState,
              description: (e.target as HTMLInputElement).value,
            }))
          }
        />
        <MapInput
          center={[45.9121312, 22.3813854]}
          zoom={3}
          item={formValues}
          onClick={setCoordinates}
        />
        <div className="flex space-x-4">
          <TextInput
            label="Latitude"
            fieldName="latitude"
            value={formValues.latitude}
            readOnly
          />
          <TextInput
            label="Longitude"
            fieldName="longitude"
            value={formValues.longitude}
            readOnly
          />
        </div>
        <ImageUploader
          files={files}
          validationError={validationError}
          isImageUploadLoading={isImageUploadLoading}
          handleUpload={handleUpload}
        />
        <div className="flex justify-end space-x-2">
          <Button
            className="ring-1 ring-lime-600 text-lime-700 hover:bg-slate-50"
            label="Close"
            onClick={closeModalHandler}
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

export default AddLocationModal;
