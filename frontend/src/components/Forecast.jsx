import React from "react";
import { useState } from "react";

const Forecast = () => {

  const [forecastLocation, setForecastLocation] = useState("");
  const [days, setDays] = useState(1);

  const handleGetForecast = (event) => {
    event.preventDefault();
    setForecastLocation(event.target.value);
  }

  const handleGetForecastDays = (event) => {
    event.preventDefault();
    setDays(event.target.value);
  }

  return (
    <div className="forecast-weather">
      <form action="get-forecast" method="post">
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
    </div>
  );
};

export default Forecast;
