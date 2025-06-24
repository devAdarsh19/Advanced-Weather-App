import React, { useEffect, useState } from "react";
import Navbar from "./Navbar";
import { Link } from "react-router-dom";
import axios from "axios";

const Home = () => {
  const [homeWeather, setHomeWeather] = useState([]);
  const [abroadWeather, setAbroadWeather] = useState([]);

  const fetch_home_weather = async () => {
    const response = await axios.get(`/api/home`).catch((error) => {
      console.log(error);
    });

    setHomeWeather(response.data.home_weather);
    setAbroadWeather(response.data["abroad_weather"]);
    console.log(response.data);
    // console.log(`abroad_weather: ${response.data}`);
  };

  useEffect(() => {
    fetch_home_weather();
  }, []);

  return (
    <>
      <Navbar />
      <div>
        <h1>Weather App</h1>
        <p>Get weather information for any place in the world</p>
        <span>
          Powered by <i>Free Weather API</i>
        </span>
      </div>

      <div>
        <h2>Get Weather Information</h2>
        <Link to="/weather">
          <button>Weather</button>
        </Link>
      </div>

      <div>
        <h2>Get Forecast Information</h2>
        <Link to="/forecast">
          <button>Forecast</button>
        </Link>
      </div>

      <h2>Popular cities in your area</h2>
      <div className="homepage-weather">
        {homeWeather &&
          homeWeather.map((homeLocation, index) => {
            <div key={index}>
              <p>Location: {homeLocation.location_name}</p>
              <p>Condition: {homeLocation.condition}</p>
              <p>
                Temperature: {homeLocation.temperature_c} /{" "}
                {homeLocation.temperature_f}
              </p>
            </div>;
          })}
      </div>

      <h2>Popular cities around the world</h2>
      <div className="homepage-weather">
        {abroadWeather &&
          abroadWeather.map((abroadLocation, index) => {
            <div key={index}>
              <p>Location: {abroadLocation.location_name}</p>
              <p>Condition: {abroadLocation.condition}</p>
              <p>
                Temperature: {abroadLocation.temperature_c} /{" "}
                {abroadLocation.temperature_f}
              </p>
            </div>;
          })}
      </div>
    </>
  );
};

export default Home;
