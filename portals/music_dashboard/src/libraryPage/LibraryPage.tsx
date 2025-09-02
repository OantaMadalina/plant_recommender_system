import { useState, useMemo, useEffect, useCallback, useContext } from "react";
import { ToastContainer } from "react-toastify";
import { createPortal } from "react-dom";
import axios from "axios";

import { faPlus } from "@fortawesome/free-solid-svg-icons";

import Button from "../shared/Button";
import ConfirmModal from "../shared/ConfirmModal";
import Loader from "../shared/Loader";
import SearchInput from "../shared/SearchInput";
import { Action, Dictionary, SongItemProps } from "../interfaces";
import { emptySongFormState } from "../constants";
import environment from "../environment";
import { isClubThemeContext } from "../App";
import { addErrorToast, addSuccessToast } from "../utils";

import SongItemsList from "./SongItemsList";
import UpsertSongModal from "./UpsertSongModal";

const LibraryPage = () => {
  const [songs, setSongs] = useState<SongItemProps[]>([]);
  const [searchContent, setSearchContent] = useState<string | undefined>("");
  const [visibleModal, setVisibleModal] = useState("");
  const [defaultFormValues, setDefaultFormValues] =
    useState(emptySongFormState);
  const [showLoader, setShowLoader] = useState(true);
  const { isClubTheme } = useContext(isClubThemeContext);

  const getSongs = useCallback(async () => {
    const apiPath = `${environment.apiUrl}/songs`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    try {
      const response = await axios.get(apiPath, apiParams);
      setSongs(response.data);
    } catch (err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage);
    } finally {
      setShowLoader(false);
    }
  }, []);

  const upsertSong = useCallback(async (payload: Dictionary) => {
    const apiPath = `${environment.apiUrl}/songs`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    const data = {
      songId: payload.songId ?? null,
      songName: payload.songName,
      artist: payload.artist,
      album: payload.album,
      YTURL: payload.YTURL,
      locations: payload.locations
    };

    try {
      const response = await axios.post(apiPath, data, apiParams);
      const responseData = response.data;
      addSuccessToast(responseData.message);
      return responseData.songId;
    } catch (err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage);
    }
  }, []);

  const removeSong = useCallback(async (songId: string) => {
    const apiPath = `${environment.apiUrl}/songs/${songId}`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    try {
      const response = await axios.delete(apiPath, apiParams);
      const responseData = response.data;
      addSuccessToast(responseData);
      return responseData;
    } catch (err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage);
    }
  }, []);

  useEffect(() => {
    getSongs();
  }, [getSongs]);

  const filteredSongs = useMemo(
    () =>
      songs.filter(
        (song) =>
          song.songName
            .toLocaleLowerCase()
            .includes(searchContent?.toLocaleLowerCase() ?? "") ||
          (song.album &&
            song.album
              .toLocaleLowerCase()
              .includes(searchContent?.toLocaleLowerCase() ?? "")) ||
          song.artist
            .toLocaleLowerCase()
            .includes(searchContent?.toLocaleLowerCase() ?? "")
      ),
    [searchContent, songs]
  );

  const searchHandler = (searchContent?: string | undefined) => {
    setSearchContent(searchContent);
  };

  const closeModal = () => {
    setVisibleModal("");
    setDefaultFormValues(emptySongFormState);
  };

  const removeSongHandler = async () => {
    const songToRemove = defaultFormValues.songId;
    closeModal();

    try {
      const responseData = await removeSong(songToRemove);
      addSuccessToast(responseData.message)
      setSongs((prevState) =>
        prevState.filter((song) => song.songId !== defaultFormValues.songId)
      );
    } catch(err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage)
    }

  };

  const handleSongActionTriggered = (action: Action, song: SongItemProps) => {
    setVisibleModal(action.id);
    setDefaultFormValues(song);
  };

  const submitForm = async (payload: Dictionary) => {
    const songAlreadyExists = songs.find(
      (song) => song.songId === payload.songId
    );
    let updatedSongs = [];
    const upsertedSongId = await upsertSong({...payload, locations: songAlreadyExists?.locations || []});
    if (!upsertedSongId) return;

    if (songAlreadyExists) {
      updatedSongs = songs.map((song) =>
        song.songId === payload.songId
          ? {
              ...song,
              ...payload
            }
          : song
      );
    } else {
      updatedSongs = [
        ...songs,
        {
          ...payload,
          songId: upsertedSongId,
        },
      ];
    }
    setSongs(updatedSongs as SongItemProps[]);
  };
  return (
    <>
      {showLoader ? (
        <Loader />
      ) : (
        <div className="space-y-4 w-full h-screen">
          <div className="flex w-full space-x-4">
            <SearchInput className="flex-auto" searchHandler={searchHandler} />
            <Button
              className={`flex-none ${
                isClubTheme ? "bg-lime-500 text-slate-100" : "bg-lime-700"
              } text-slate-50 hover:bg-lime-600`}
              icon={faPlus}
              onClick={() => setVisibleModal("add")}
            />
          </div>
          <SongItemsList
            songs={filteredSongs}
            handleSongActionTriggered={handleSongActionTriggered}
          />
          {(visibleModal === "add" || visibleModal === "edit") &&
            createPortal(
              <UpsertSongModal
                defaultValues={defaultFormValues}
                closeModal={closeModal}
                submitForm={submitForm}
              />,
              document.body
            )}
          {visibleModal === "remove" &&
            createPortal(
              <ConfirmModal
                headerTitle="Remove Song"
                headerLevel={3}
                confirmationMessage={`Are you sure you wan to remove song ${defaultFormValues.songName} by ${defaultFormValues.artist}?`}
                closeModal={closeModal}
                confirmAction={removeSongHandler}
              />,
              document.body
            )}
        </div>
      )}
      <ToastContainer />
    </>
  );
};

export default LibraryPage;
