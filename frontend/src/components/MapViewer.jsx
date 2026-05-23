import { MapContainer, TileLayer, GeoJSON, useMap } from "react-leaflet";
import { useEffect } from "react";
import L from "leaflet";

function GeoJSONLayer({ geojson }) {
  const map = useMap();

  useEffect(() => {
    if (!geojson) return;

    const layer = L.geoJSON(geojson).addTo(map);
    map.fitBounds(layer.getBounds(), { padding: [20, 20] });

    return () => {
      map.removeLayer(layer);
    };
  }, [geojson, map]);

  return null;
}

export default function MapViewer({ geojson }) {
  return (
    <MapContainer
      style={{ height: "100%", width: "100%" }}
      center={[0, 0]}
      zoom={2}
      scrollWheelZoom={true}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {geojson && <GeoJSONLayer geojson={geojson} />}
    </MapContainer>
  );
}
