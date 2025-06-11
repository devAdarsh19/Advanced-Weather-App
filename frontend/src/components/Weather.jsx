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
    console.log("Form submitted");
    const response = await axios.get(
      `http://localhost:8000/api/weather?location_q=${locationData}`
    )
    .catch((error) => {
      console.log(error);
      alert("[ERROR] Error fetching weather data.");
    });

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
          <button type="submit">Get current weather</button>
        </form>
      </div>

      {weatherData && (
        <div>
            <h2>Location: {weatherData.location_name}</h2>
            <h3>Condition: {weatherData.condition}</h3>
            <h3>Localtime: {weatherData.localtime}</h3>
            <h3>Temperature (℃): {weatherData.temp_c}</h3>
            <h3>Temperature (℉): {weatherData.temp_f}</h3>
        </div>
      )}
    </>
  );
};

export default Weather;
