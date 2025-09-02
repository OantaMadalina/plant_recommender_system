import { MapContainer, Marker, TileLayer, useMapEvents } from "react-leaflet";
import L from "leaflet";
import icon from "leaflet/dist/images/marker-icon.png";
import iconShadow from "leaflet/dist/images/marker-shadow.png";
import { MapInputProps } from "../interfaces";

let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
});

L.Marker.prototype.options.icon = DefaultIcon;

const MapInput = (props: MapInputProps) => {
  const { center, zoom, item, onClick } = props;
  const MapEventHandler = () => {
    useMapEvents({
      click(e) {
        onClick && onClick(e);
      },
    });
    return null;
  };
  return (
    <MapContainer
      className="flex w-full h-[300px] rounded-lg"
      center={center}
      zoom={zoom}
      scrollWheelZoom
    >
      <TileLayer
        className="rounded-lg"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapEventHandler />

      {item && item.latitude && item.longitude && (
        <Marker
          key={item.longitude + item.longitude}
          position={[parseFloat(item.latitude), parseFloat(item.longitude)]}
        />
      )}
    </MapContainer>
  );
};

export default MapInput;
