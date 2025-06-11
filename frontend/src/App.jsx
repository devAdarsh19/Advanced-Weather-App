import { React } from "react";
import Navbar from "./components/Navbar";
import Weather from "./components/Weather";
import Forecast from "./components/Forecast";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {

  return (
    <>
      {/* Navbar */}
      <Navbar />

      {/* Get current weather */}
      {/* <Weather /> */}

      {/* Get forecast */}
      <Forecast />
    </>
  );
}

export default App;
