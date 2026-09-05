import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

const cityCenter = [12.9716, 79.1597];


// 🚑 Ambulance icon
const ambulanceIcon = new L.DivIcon({
  className: "custom-marker",
  html: "🚑",
  iconSize: [32, 32],
  iconAnchor: [16, 16],
});


// 🏥 Hospital icon
const hospitalIcon = new L.DivIcon({
  className: "custom-marker",
  html: "🏥",
  iconSize: [32, 32],
  iconAnchor: [16, 16],
});


// 🚨 Emergency icon
const emergencyIcon = new L.DivIcon({
  className: "custom-marker emergency-marker",
  html: "🚨",
  iconSize: [40, 40],
  iconAnchor: [20, 20],
});


function App() {
  const [ambulances, setAmbulances] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [dispatchResult, setDispatchResult] = useState(null);
  const [loading, setLoading] = useState(false);


  useEffect(() => {
    fetchData();
  }, []);


  async function fetchData() {
    try {
      const ambulanceResponse = await fetch(
        `${API_URL}/ambulances`
      );

      const hospitalResponse = await fetch(
        `${API_URL}/hospitals`
      );

      const ambulanceData =
        await ambulanceResponse.json();

      const hospitalData =
        await hospitalResponse.json();

      setAmbulances(
        ambulanceData.ambulances
      );

      setHospitals(
        hospitalData.hospitals
      );
    } catch (error) {
      console.error(
        "Failed to load city data:",
        error
      );
    }
  }


  async function dispatchEmergency() {
    setLoading(true);

    try {
      const response = await fetch(
        `${API_URL}/dispatch`,
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/json",
          },
          body: JSON.stringify({
            latitude: cityCenter[0],
            longitude: cityCenter[1],
            severity: "CRITICAL",
          }),
        }
      );

      const data = await response.json();

      setDispatchResult(data);

      await fetchData();
    } catch (error) {
      console.error(
        "Dispatch failed:",
        error
      );
    } finally {
      setLoading(false);
    }
  }


  function routeToLatLng(route) {
    if (!route?.geometry?.coordinates) {
      return [];
    }

    return route.geometry.coordinates.map(
      ([longitude, latitude]) => [
        latitude,
        longitude,
      ]
    );
  }


  const ambulanceRoute =
    routeToLatLng(
      dispatchResult?.ambulance?.route
    );

  const hospitalRoute =
    routeToLatLng(
      dispatchResult?.hospital?.route
    );


  return (
    <div className="app">

      <header className="header">

        <div>
          <h1>
            🚨 Emergency Response
            Intelligence System
          </h1>

          <p>
            Emergency Response Command Center
          </p>
        </div>


        <button
          onClick={dispatchEmergency}
          disabled={loading}
        >
          {loading
            ? "DISPATCHING..."
            : "🚑 DISPATCH EMERGENCY"}
        </button>

      </header>


      <main className="dashboard">

        <section className="map-section">

          <MapContainer
            center={cityCenter}
            zoom={12}
            className="map"
          >

            <TileLayer
              attribution="&copy; OpenStreetMap contributors"
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />


            {/* 🚑 Ambulances */}

            {ambulances.map(
              (ambulance) => (

                <Marker
                  key={ambulance.id}
                  position={[
                    ambulance.latitude,
                    ambulance.longitude,
                  ]}
                  icon={ambulanceIcon}
                >

                  <Popup>

                    <strong>
                      🚑 {ambulance.id}
                    </strong>

                    <br />

                    Status:{" "}
                    {ambulance.status}

                  </Popup>

                </Marker>

              )
            )}


            {/* 🏥 Hospitals */}

            {hospitals.map(
              (hospital) => (

                <Marker
                  key={hospital.id}
                  position={[
                    hospital.latitude,
                    hospital.longitude,
                  ]}
                  icon={hospitalIcon}
                >

                  <Popup>

                    <strong>
                      🏥 {hospital.name}
                    </strong>

                    <br />

                    Beds:{" "}
                    {hospital.available_beds}

                    <br />

                    ICU:{" "}
                    {hospital.icu_available}

                  </Popup>

                </Marker>

              )
            )}


            {/* 🚨 Emergency */}

            {dispatchResult && (

              <Marker
                position={[
                  dispatchResult.emergency.latitude,
                  dispatchResult.emergency.longitude,
                ]}
                icon={emergencyIcon}
              >

                <Popup>

                  <strong>
                    🚨 Emergency
                  </strong>

                  <br />

                  Severity:{" "}
                  {
                    dispatchResult
                      .emergency
                      .severity
                  }

                </Popup>

              </Marker>

            )}


            {/* 🚑 Ambulance → Emergency route */}

            {ambulanceRoute.length > 0 && (

              <Polyline
                positions={ambulanceRoute}
                weight={6}
              />

            )}


            {/* 🚨 Emergency → Hospital route */}

            {hospitalRoute.length > 0 && (

              <Polyline
                positions={hospitalRoute}
                weight={6}
              />

            )}

          </MapContainer>

        </section>


        <aside className="sidebar">

          <div className="panel">

            <h2>
              🚑 Ambulances
            </h2>

            <h3>
              {ambulances.length}
            </h3>

            <p>
              Simulated units
            </p>

          </div>


          <div className="panel">

            <h2>
              🏥 Hospitals
            </h2>

            <h3>
              {hospitals.length}
            </h3>

            <p>
              Available facilities
            </p>

          </div>


          {dispatchResult && (

            <div className="panel dispatch-panel">

              <h2>
                🚨 Latest Dispatch
              </h2>


              <p>
                <strong>
                  Emergency:
                </strong>{" "}
                {
                  dispatchResult
                    .emergency.id
                }
              </p>


              <p>
                <strong>
                  Severity:
                </strong>{" "}
                {
                  dispatchResult
                    .emergency.severity
                }
              </p>


              {dispatchResult.ambulance && (

                <>
                  <hr />

                  <h3>
                    🚑 Ambulance
                  </h3>

                  <p>
                    {
                      dispatchResult
                        .ambulance.id
                    }
                  </p>

                  <p>
                    ETA:{" "}
                    {
                      dispatchResult
                        .ambulance
                        .eta_minutes
                    }{" "}
                    min
                  </p>

                  <p>
                    Distance:{" "}
                    {
                      dispatchResult
                        .ambulance
                        .distance_km
                    }{" "}
                    km
                  </p>

                </>

              )}


              {dispatchResult.hospital && (

                <>
                  <hr />

                  <h3>
                    🏥 Hospital
                  </h3>

                  <p>
                    {
                      dispatchResult
                        .hospital
                        .name
                    }
                  </p>

                  <p>
                    ETA:{" "}
                    {
                      dispatchResult
                        .hospital
                        .eta_minutes
                    }{" "}
                    min
                  </p>

                  <p>
                    Beds:{" "}
                    {
                      dispatchResult
                        .hospital
                        .available_beds
                    }
                  </p>

                  <p>
                    ICU:{" "}
                    {
                      dispatchResult
                        .hospital
                        .icu_available
                    }
                  </p>

                </>

              )}

            </div>

          )}

        </aside>

      </main>

    </div>
  );
}


export default App;