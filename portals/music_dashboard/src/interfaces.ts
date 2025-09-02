import { IconProp } from "@fortawesome/fontawesome-svg-core";
import { LatLngExpression, LeafletMouseEvent } from "leaflet";
import { ChangeEvent } from "react";

export interface LayoutProps {
  children?: React.ReactNode;
}
export interface CustomizableStyling {
  className?: string;
}
export interface HeaderProps extends CustomizableStyling {
  title: string;
  level: number;
}
export interface SongItemProps extends CustomizableStyling {
  songId: string;
  songName: string;
  album?: string;
  artist: string;
  YTURL: string;
  locations?: LocationItemProps[];
  showActions?: boolean;
  handleActionTriggered?: (action: Action, song: SongItemProps) => void;
}

export interface LocationItemProps extends CustomizableStyling {
  locationId: string;
  imagePath: string;
  description: string;
  latitude: string;
  longitude: string;
  createdAt: string;
  handleLocationActionTriggered?: (
    action: Action,
    location: LocationItemProps
  ) => void;
}

export interface LocationItemListProps {
  locations: LocationItemProps[];
  handleLocationActionTriggered?: (
    action: Action,
    location: LocationItemProps
  ) => void;
}

export interface SongItemsListProps extends CustomizableStyling {
  songs: SongItemProps[];
  handleSongActionTriggered?: (action: Action, song: SongItemProps) => void;
}

export interface ButtonProps extends CustomizableStyling {
  icon?: IconProp;
  label?: string;
  onClick?: () => void;
}

export interface SearchInputProps extends CustomizableStyling, LayoutProps {
  onFocus?: () => void;
  onBlur?: () => void;
  searchHandler: (searchContent?: string) => void;
}

export interface TextInputDataModel {
  label: string;
  fieldName: string;
  type?: string;
  placeholder?: string;
}

export interface TextInputProps extends CustomizableStyling, TextInputDataModel {
  value: string;
  disabled?: boolean;
  readOnly?: boolean;
  setFormValue?: (event: ChangeEvent) => void;
}

export interface Dictionary {
  [key: string]: any;
}

export interface UpsertSongModalProps {
  defaultValues: SongItemProps;
  submitForm?: (payload: Dictionary) => void;
  closeModal?: () => void;
}

export interface ConfirmModalProps {
  headerTitle: string;
  headerLevel: number;
  confirmationMessage: string;
  confirmAction?: () => void;
  closeModal?: () => void;
}

export interface Action {
  id: string;
  label: string;
}
export interface IconicDropdownProps extends CustomizableStyling {
  icon?: IconProp;
  actions: Action[];
  handleActionTriggered?: (action: Action) => void;
}

export interface ImageUploaderProps extends CustomizableStyling {
  files: File[];
  validationError: string;
  isImageUploadLoading: boolean;
  handleUpload?: (event: any) => void;
}

export interface AddLocationPropsHandlers {
  songId?: string;
  closeModal: () => void;
  submitForm: (event: Dictionary) => void;
}

export interface UpsertSongResponse {
  songId: string;
  message: string;
}

export interface IconicButtonProps extends LayoutProps, CustomizableStyling {
  icon: IconProp;
  onClick: () => void;
}

export interface LoginFormState {
  username: string;
  password: string;
}

export interface PillsProps extends CustomizableStyling {
  items: {
    id: string;
    label: string;
    icon?: IconProp;
  }[];
  onClick?: (item: string) => void;
}

export interface MapComponentProps extends CustomizableStyling {
  center: LatLngExpression;
  zoom: number;
  items: LocationItemProps[];
}

export interface MapInputProps extends CustomizableStyling {
  center: LatLngExpression;
  zoom: number;
  item?: { latitude: string; longitude: string };
  onClick?: (e: LeafletMouseEvent) => void
}
