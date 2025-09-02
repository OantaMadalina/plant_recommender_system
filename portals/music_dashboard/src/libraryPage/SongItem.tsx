import { useContext } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay } from "@fortawesome/free-solid-svg-icons";

import IconicDropdown from "../shared/IconicDropdown";

import { Action, SongItemProps } from "../interfaces";
import { songItemActions } from "../constants";
import { userRoleContext } from "../App";

const SongItem = (props: SongItemProps) => {
  const { userRole } = useContext(userRoleContext);
  const { songId, songName, album, artist, className, showActions, handleActionTriggered } =
    props;
  const handleSongActionTriggered = (action: Action) => {
    handleActionTriggered && handleActionTriggered(action, props);
  };
  return (
    <div className={className}>
      <Link
        className="flex space-x-4 items-center w-full"
        to={`/song/${songId}`}
      >
        <FontAwesomeIcon className="text-amber-800/75" icon={faPlay} />
        <div className="grid grid-cols-3 w-full space-x-8">
          <div className="flex flex-col">
            <span className="text-xs text-amber-700/75">Name</span>
            <span className="break-words text-lime-800">{songName}</span>
          </div>
          <div className="flex flex-col">
            <span className="text-xs text-amber-700/75">Artist</span>
            <span className="break-words text-lime-800">{artist}</span>
          </div>
          {album && (
            <div className="flex flex-col">
              <span className="text-xs text-amber-700/75">Album</span>
              <span className="break-words text-lime-800">{album}</span>
            </div>
          )}
        </div>
      </Link>
      {userRole === "admin" && showActions && (
        <IconicDropdown
          key={songId}
          className="text-amber-800/75 px-2"
          actions={songItemActions}
          handleActionTriggered={handleSongActionTriggered}
        />
      )}
    </div>
  );
};

export default SongItem;
