import { useState, useRef } from "react";
import { faEllipsisVertical } from "@fortawesome/free-solid-svg-icons";
import { IconicDropdownProps } from "../interfaces";
import IconicButton from "./IconicButton";

const IconicDropdown = ({
  className,
  icon,
  actions,
  handleActionTriggered,
}: IconicDropdownProps) => {
  const [toggleDropdown, setToggleDropdown] = useState(false);
  const dropdownButtonRef = useRef(null);

  const triggerAction = (event: React.MouseEvent) => {
    handleActionTriggered &&
      handleActionTriggered(
        actions.filter((op) => op.id === (event.target as HTMLElement).id)[0]
      );
  };

  document.addEventListener("click", (ev: MouseEvent) => {
    const evElem = ev.target as HTMLElement;
    if (!dropdownButtonRef || !dropdownButtonRef.current) return;
    const elem = dropdownButtonRef.current as HTMLElement;

    if (evElem.id !== elem.id && toggleDropdown) setToggleDropdown(false);
  });

  return (
    <IconicButton
      ref={dropdownButtonRef}
      icon={icon ?? faEllipsisVertical}
      className={`relative ${className}`}
      onClick={() => setToggleDropdown((prevState) => !prevState)}
    >
      {toggleDropdown && (
        <div
          id="dropdown"
          className="absolute -left-14 ring-1 ring-amber-800/75 rounded-lg bg-white py-1 px-2 items-start divide-y divide-solid z-10"
        >
          {actions.map((action) => (
            <p
              className="text-lime-800 hover:text-lime-600"
              key={action.id}
              id={action.id}
              onClick={triggerAction}
            >
              {action.label}
            </p>
          ))}
        </div>
      )}
    </IconicButton>
  );
};

export default IconicDropdown;
