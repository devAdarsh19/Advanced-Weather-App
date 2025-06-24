import React from "react";
import { useState } from "react";
import axios from "axios";
import Navbar from "./Navbar";

const Forecast = () => {
  const [forecastLocation, setForecastLocation] = useState("");
  const [days, setDays] = useState(1);
  const [forecastData, setForecastData] = useState(null);

  const handleGetForecast = (event) => {
    event.preventDefault();
    setForecastLocation(event.target.value);
  };

  const handleGetForecastDays = (event) => {
    event.preventDefault();
    setDays(event.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form Submitted");
    const response = await axios
      .get(
        `http://localhost:8000/api/forecast?location=${forecastLocation}&days=${days}`
        // `/api/forecast?location=${forecastLocation}&days=${days}`
      )
      .catch((error) => {
        console.log(`Error: ${error}`);
        alert("[ERROR] Error while fetching forecast data.");
      });

    // const data = await response.json()
    console.log(response.data);
    setForecastData(response.data);
  };

  return (
    <>
      <Navbar />
      <h2>Get Forecast Information for upto 5 days</h2>
      <br />
      
      <div className="forecast-weather">
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="">Location</label>
            <input
              type="text"
              name="location"
              id=""
              placeholder="Ex: New York, London, etc"
              onChange={handleGetForecast}
            />
            <span>{forecastLocation}</span>
          </div>
          <div>
            <label htmlFor="">Days</label>
            <input
              type="text"
              name="location"
              id=""
              placeholder="0 < days < 5"
              onChange={handleGetForecastDays}
            />
            <span>{days}</span>
          </div>
          <button type="submit">Get weather forecast</button>
        </form>

        {forecastData && (
          <div>
            <h2>
              <strong>Location : {forecastData.location_name}</strong>
            </h2>
            <h3>Local Time : {forecastData.localtime}</h3>
            <h3>Condition : {forecastData.condition}</h3>
            <h3>
              Temperature: {forecastData.temp_c}℃ / {forecastData.temp_f}℉
            </h3>
            {forecastData.forecast_days.map((days, index) => (
              <div key={index}>
                <br />
                <h3>
                  <strong>Date: {days.date}</strong>
                </h3>
                <h4>Condition: {days.condition}</h4>
                {/* <h4>Avg Temperature: { days.temp_c }℃ / { days.temp_f }℉</h4> */}
                <h4>
                  Max Temperature: {days.maxtemp_c}℃ / {days.maxtemp_f}℉
                </h4>
                <h4>
                  Min Temperature: {days.mintemp_c}℃ / {days.mintemp_f}℉
                </h4>
                {days.hours.map((hour, hourIndex) => (
                  <div key={hourIndex} style={{ marginLeft: "20px" }}>
                    <br />
                    <h3>
                      <strong>Date & Time: {hour.time}</strong>
                    </h3>
                    <h4>Condition: {hour.condition}</h4>
                    <h4>
                      Temperature: {hour.temp_c}℃ / {hour.temp_f}℉
                    </h4>
                  </div>
                ))}
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default Forecast;
