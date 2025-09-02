import { useContext, useState } from "react";

import { faTrash } from "@fortawesome/free-solid-svg-icons";

import IconicButton from "../shared/IconicButton";

import { LocationItemProps } from "../interfaces";
import { locationItemActions } from "../constants";
import { isClubThemeContext, userRoleContext } from "../App";

const LocationItem = (props: LocationItemProps) => {
  const { userRole } = useContext(userRoleContext);
  const { imagePath, description, createdAt, handleLocationActionTriggered } =
    props;
  const [displayActions, setDisplayActions] = useState(false);
  const { isClubTheme } = useContext(isClubThemeContext);

  return (
    <figure
      className={`relative ring-1 ring-lime-800/25 px-2 pt-2 pb-4 rounded-sm ${
        isClubTheme ? "bg-slate-50" : ""
      }`}
      onMouseOut={() => setDisplayActions(false)}
      onMouseOver={() => setDisplayActions(true)}
    >
      {displayActions && userRole === "admin" && (
        <IconicButton
          className="absolute px-2 py-1 left-[calc(100%-38px)] bg-white text-lime-800"
          icon={faTrash}
          onClick={() =>
            handleLocationActionTriggered &&
            handleLocationActionTriggered(locationItemActions[0], props)
          }
        />
      )}
      <img
        className="rounded-sm min-w-full"
        src={imagePath}
        alt={description}
      />
      <figcaption className="flex justify-between space-x-8 mt-2">
        <span className="max-w-lg text-lime-800">
          On spotter's mind: <i className="text-amber-700">"{description}"</i>
        </span>
        <span className="text-lime-800">
          <i>{new Date(createdAt).toLocaleDateString()}</i>
        </span>
      </figcaption>
    </figure>
  );
};

export default LocationItem;
