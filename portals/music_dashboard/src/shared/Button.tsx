import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { ButtonProps } from "../interfaces";

const Button = ({ icon, label, className, onClick }: ButtonProps) => {
  return (
    <button
      className={`space-x-2 items-center rounded-full px-3 py-1 ${className}`}
      onClick={onClick}
    >
      {icon && <FontAwesomeIcon icon={icon} />}
      {label && <span>{label}</span>}
    </button>
  );
};

export default Button;
