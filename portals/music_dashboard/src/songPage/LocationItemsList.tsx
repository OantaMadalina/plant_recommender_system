import { LocationItemListProps } from "../interfaces";
import LocationItem from "./LocationItem";

const LocationItemsList = ({ locations, handleLocationActionTriggered }: LocationItemListProps) => {
  return (
    <div className="flex flex-col items-center space-y-8">
      {locations.map((location) => (
        <LocationItem {...location} handleLocationActionTriggered={handleLocationActionTriggered} />
      ))}
    </div>
  );
};

export default LocationItemsList;
