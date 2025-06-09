import { React } from "react";
import Navbar from "./components/Navbar";
import Weather from "./components/Weather";
import Forecast from "./components/Forecast";

function App() {

  return (
    <>
      {/* Navbar */}
      <Navbar />

      {/* Get current weather */}
      <Weather />
      

      {/* Get forecast */}
      
    </>
  );
}

export default App;
