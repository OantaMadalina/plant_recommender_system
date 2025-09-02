import { useEffect, useState, useMemo, useCallback, useContext } from "react";
import { createPortal } from "react-dom";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { ToastContainer } from "react-toastify";

import ConfirmModal from "../shared/ConfirmModal";
import Button from "../shared/Button";
import Loader from "../shared/Loader";
import SearchInput from "../shared/SearchInput";
import SearchDropdown from "../shared/SearchDropdown";
import Header from "../shared/Header";

import {
  Action,
  Dictionary,
  LocationItemProps,
  SongItemProps,
} from "../interfaces";
import { emptySongFormState, pillsItems } from "../constants";
import environment from "../environment";
import { addErrorToast, addSuccessToast } from "../utils";
import { isClubThemeContext } from "../App";

import LocationItemsList from "./LocationItemsList";
import AddLocationModal from "./AddLocationModal";
import Pills from "./Pills";
import MapComponent from "./MapComponent";

const SongPage = () => {
  const pathParams = useParams();
  const songId = useMemo(() => pathParams["songId"], [pathParams]);

  const navigate = useNavigate();

  const [visibleModal, setVisibleModal] = useState("");
  const [selectedLocation, setSelectedLocation] =
    useState<LocationItemProps | null>();

  const [song, setSong] = useState<SongItemProps>(emptySongFormState);
  const [searchContent, setSearchContent] = useState<string | undefined>("");
  const [songs, setSongs] = useState<SongItemProps[]>([]);
  const [showLoader, setShowLoader] = useState(true);
  const [showDropdown, setShowDropdown] = useState(false);
  const [view, setView] = useState(pillsItems[0].id);
  const { isClubTheme } = useContext(isClubThemeContext);

  const getSong = useCallback(async () => {
    const apiPath = `${environment.apiUrl}/song-locations/${songId}`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    try {
      const response = await axios.get(apiPath, apiParams);
      const songData: SongItemProps = response.data;
      songData.locations = songData.locations?.sort(
        (a: LocationItemProps, b: LocationItemProps) =>
          new Date(b.createdAt).valueOf() - new Date(a.createdAt).valueOf()
      );
      setSong(songData);
      setShowLoader(false);
    } catch (err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage);
      navigate("404");
    }
  }, [songId, navigate]);

  const removeLocation = useCallback(
    async (locationId: string | undefined) => {
      if (!locationId) return;

      const apiPath = `${environment.apiUrl}/song-locations/${songId}/${locationId}`;
      const apiParams = environment.params;

      if (!apiPath || !apiParams) return;

      try {
        const response = await axios.delete(apiPath, apiParams);
        const responseData = response.data;
        addSuccessToast(responseData.message);
        return responseData;
      } catch (err: any) {
        const errorMessage = `Request failed: ${err.response.data.error}`;
        addErrorToast(errorMessage);
      }
    },
    [songId]
  );

  const insertLocation = useCallback(async (payload: Dictionary) => {
    const apiPath = `${environment.apiUrl}/song-locations`;
    const apiParams = environment.params;

    if (!apiPath || !apiParams) return;

    try {
      const response = await axios.post(apiPath, payload, apiParams);
      const responseData = response.data;
      setSong((prevState) => ({
        ...prevState,
        locations: [responseData["location"], ...(prevState.locations || [])],
      }));
      addSuccessToast(responseData.message);
      return responseData;
    } catch (err: any) {
      const errorMessage = `Request failed: ${err.response.data.error}`;
      addErrorToast(errorMessage);
    }
  }, []);

  useEffect(() => {
    getSong();
  }, [getSong]);

  const handleLocationActionTriggered = (
    action: Action,
    location: LocationItemProps
  ) => {
    setVisibleModal(action.id);
    setSelectedLocation(location);
  };

  const confirmAction = async () => {
    setVisibleModal("");

    const response = await removeLocation(selectedLocation?.locationId);
    if (!response) return;

    setSong((prevState) => ({
      ...prevState,
      locations: prevState.locations?.filter(
        (location) => location.locationId !== selectedLocation?.locationId
      ),
    }));
  };

  const submitForm = async (formValues: Dictionary) => {
    insertLocation({
      ...formValues,
      songId: songId,
    });
  };

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
    }
  }, []);

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

  useEffect(() => {
    getSongs();
  }, [getSongs]);

  if (showLoader) {
    return <Loader />;
  }

  return (
    <>
      <div className="flex flex-col items-center space-y-12 max-w-screen-lg">
        <SearchInput
          className="relative w-full"
          searchHandler={searchHandler}
          onFocus={() => setShowDropdown((prevState) => !prevState)}
          onBlur={() =>
            setTimeout(() => setShowDropdown((prevState) => !prevState), 200)
          }
        >
          {searchContent && showDropdown && (
            <SearchDropdown
              className="absolute bg-white w-full py-2 border top-9 rounded-lg divide-y border ring-1 ring-lime-600"
              songs={filteredSongs}
            />
          )}
        </SearchInput>

        <iframe
          id="song"
          key={song.YTURL}
          className="w-full rounded-lg aspect-video"
          height="480"
          src={song.YTURL}
          title="YouTube video player"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerPolicy="strict-origin-when-cross-origin"
          allowFullScreen
          onLoad={() => setShowLoader(false)}
        />
        {song.locations && song.locations.length > 0 && (
          <div className="self-start flex w-full justify-between items-center">
            <Header
              className={`"text-2xl ${
                isClubTheme ? "text-amber-500" : "text-amber-700/75"
              }`}
              level={6}
              title="Other spotters listened to this song here"
            />
            <Pills
              className={`ring-lime-500  ${
                isClubTheme ? "text-lime-400" : "text-lime-800"
              }`}
              items={pillsItems}
              onClick={setView}
            />
          </div>
        )}
        {view === "list" && (
          <>
            <LocationItemsList
              locations={song.locations ?? []}
              handleLocationActionTriggered={handleLocationActionTriggered}
            />
            <Button
              className={`fixed bottom-[5%] right-[20%] ${
                isClubTheme ? "bg-amber-500" : "bg-amber-700"
              } text-slate-50 hover:bg-amber-600`}
              icon={faPlus}
              label="Add Your Spot"
              onClick={() => setVisibleModal("add")}
            />
          </>
        )}

        {view === "map" && (
          <MapComponent
            center={[45.9121312, 22.3813854]}
            zoom={3}
            items={song.locations ?? []}
          />
        )}

        {visibleModal === "add" &&
          createPortal(
            <AddLocationModal
              songId={songId}
              closeModal={() => setVisibleModal("")}
              submitForm={submitForm}
            />,
            document.body
          )}
        {visibleModal === "remove" &&
          createPortal(
            <ConfirmModal
              headerTitle="Remove Location"
              headerLevel={3}
              confirmationMessage="Are you sure you want to remove this location?"
              closeModal={() => setVisibleModal("")}
              confirmAction={confirmAction}
            />,
            document.body
          )}
      </div>
      <ToastContainer />
    </>
  );
};

export default SongPage;
