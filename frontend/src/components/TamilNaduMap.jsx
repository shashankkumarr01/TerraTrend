
import { useEffect, useState } from "react";
import L from "leaflet";
import {
  MapContainer,
  TileLayer,
  GeoJSON,
  useMap,
} from "react-leaflet";
import "./TamilNaduMap.css";

function FitMap({ data }) {
  const map = useMap();

  useEffect(() => {
    if (data) {
      const layer = L.geoJSON(data);
      const bounds = layer.getBounds();

      if (bounds.isValid()) {
        map.fitBounds(bounds, { padding: [20, 20] });
      }
    }
  }, [data, map]);

  return null;
}

export default function TamilNaduMap({
  selectedDistrict,
  onDistrictSelect,
}) {
  const [geoData, setGeoData] = useState(null);

  const [error, setError] = useState("");

  useEffect(() => {
    fetch("/data/tamil_nadu_districts.geojson")
      .then((response) => {
        if (!response.ok) {
          throw new Error("GeoJSON file could not be loaded");
        }
        return response.json();
      })
      .then((data) => setGeoData(data))
      .catch((err) => setError(err.message));
  }, []);

  const districtStyle = (feature) => ({
    color:
      feature.properties.NAME_2 === selectedDistrict
        ? "#ff6600"
        : "#2563eb",
    weight:
      feature.properties.NAME_2 === selectedDistrict ? 3 : 1.5,
    fillColor:
      feature.properties.NAME_2 === selectedDistrict
        ? "#facc15"
        : "#60a5fa",
    fillOpacity: 0.45,
  });

  const onEachDistrict = (feature, layer) => {
    const districtName = feature.properties.NAME_2;
    layer.bindTooltip(districtName);

   layer.on("click", () => {
  onDistrictSelect(districtName);
});
  };

  if (error) return <p>Map Error: {error}</p>;
  if (!geoData) return <p>Loading Tamil Nadu map...</p>;

  return (
    <div className="tamil-map-wrapper">
      <h2>Tamil Nadu District Map</h2>

      <MapContainer
        center={[10.8, 78.7]}
        zoom={7}
        scrollWheelZoom={true}
        className="tamil-map"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <FitMap data={geoData} />

        <GeoJSON
          key={selectedDistrict}
          data={geoData}
          style={districtStyle}
          onEachFeature={onEachDistrict}
        />
      </MapContainer>

      <p className="selected-district">
        Selected District: {selectedDistrict || "Click a district on the map"}
      </p>
    </div>
  );
}