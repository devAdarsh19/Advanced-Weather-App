import { React } from "react";
import Navbar from "./components/Navbar";
import Weather from "./components/Weather";
import Forecast from "./components/Forecast";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/forecast" element={<Forecast />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
