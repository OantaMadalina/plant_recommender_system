import { faList, faMap } from "@fortawesome/free-solid-svg-icons";
import {
  Action,
  LoginFormState,
  SongItemProps,
  TextInputDataModel,
} from "./interfaces";

export const emptySongFormState: SongItemProps = {
  songId: "",
  songName: "",
  artist: "",
  album: "",
  YTURL: "",
  locations: [],
};

export const songItemActions: Action[] = [
  {
    id: "edit",
    label: "Edit",
  },
  {
    id: "remove",
    label: "Remove",
  },
];

export const locationItemActions: Action[] = [
  { id: "remove", label: "Remove" },
];
export const emptyLoginFormState: LoginFormState = {
  username: "",
  password: "",
};
export const loginFormFields: TextInputDataModel[] = [
  {
    fieldName: "username",
    label: "Username",
  },
  {
    fieldName: "password",
    label: "Password",
    type: "password",
  },
];

export const supportedImageExtensions = new Set(["jpeg", "jpg", "png", "gif"]);

export const songFormFields: TextInputDataModel[] = [
  {
    fieldName: "songName",
    label: "Title",
    placeholder: "Type in the song title",
  },
  {
    fieldName: "artist",
    label: "Artist",
    placeholder: "Type in the artist",
  },
  {
    fieldName: "album",
    label: "Album (Optional)",
    placeholder: "Type in the album",
  },
  {
    fieldName: "YTURL",
    label: "YouTube URL",
    placeholder: "Type in the Youtube URL",
  },
];

export const pillsItems = [
  { id: "list", label: "Show list", icon: faList },
  { id: "map", label: "Show map", icon: faMap },
];
