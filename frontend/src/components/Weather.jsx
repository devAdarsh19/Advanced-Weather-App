import React, { useState } from "react";
import axios from "axios";

const Weather = () => {
  const [locationData, setLocationData] = useState("");
  const [weatherData, setWeatherData] = useState(null);

  const handleGetWeather = (event) => {
    setLocationData(event.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    alert("Form submitted");
    const response = await axios.get(
      `http://localhost:8000/v1/weather?location=${locationData}`
    );

    // const data = await response.json()
    setWeatherData(response.data);
    console.log(response.data);
  };

  return (
    <>
      <div className="current-weather">
        <form onSubmit={handleSubmit}>
          <label htmlFor="location">Location</label>
          <input
            type="text"
            name="location"
            id=""
            placeholder="Ex: New York, London, etc"
            value={locationData}
            onChange={handleGetWeather}
          />
          <span>{locationData}</span>
          <button type="submit">Get current weather</button>
        </form>
      </div>

      {weatherData && (
        <div>
            <h2>{weatherData.location_name}</h2>
        </div>
      )}
    </>
  );
};

export default Weather;
