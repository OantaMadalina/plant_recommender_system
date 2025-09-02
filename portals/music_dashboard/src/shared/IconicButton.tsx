import { forwardRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { IconicButtonProps } from "../interfaces";

const IconicButton = forwardRef<HTMLButtonElement, IconicButtonProps>(
  ({ children, icon, className, onClick }, ref) => {
    return (
      <button
        id={`ops${Date.now()}`}
        ref={ref}
        className={className}
        onClick={onClick}
      >
        <FontAwesomeIcon className="pointer-events-none" icon={icon} />
        {children}
      </button>
    );
  }
);

export default IconicButton;
