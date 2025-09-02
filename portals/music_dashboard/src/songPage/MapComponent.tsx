import { useMemo } from "react";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import { MapComponentProps } from "../interfaces";
import LocationItem from "./LocationItem";

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapComponent = (props: MapComponentProps) => {
  const { center, zoom, items } = props;
  const mapSpots = useMemo(
    () => items.filter((item) => item.longitude && item.latitude),
    [items]
  );
  return (
    <MapContainer
      className="flex w-full h-[500px] rounded-lg"
      center={center}
      zoom={zoom}
      scrollWheelZoom
    >
      <TileLayer
        className="rounded-lg"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {mapSpots.map((item) => (
        <Marker
          key={item.locationId}
          position={[parseFloat(item.latitude), parseFloat(item.longitude)]}
        >
          <Popup>
            <LocationItem {...item} handleLocationActionTriggered={() => {}} />
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;
