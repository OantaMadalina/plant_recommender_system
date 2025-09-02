import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { PillsProps } from "../interfaces";

const Pills = ({ items, className, onClick }: PillsProps) => {
  return (
    <div
      className={`flex divide-x-2 ring-1 ring-emerald-800/25 rounded-lg items-center ${className}`}
    >
      {items.map((item) => (
        <div
          className="px-3 py-2 cursor-pointer hover:bg-emerald-100/25"
          onClick={() => onClick && onClick(item.id)}
        >
          {item.icon ? (
            <FontAwesomeIcon icon={item.icon} />
          ) : (
            <span>{item.label}</span>
          )}
        </div>
      ))}
    </div>
  );
};

export default Pills;
