import React from "react";
import "../App.css";

const Navbar = () => {
  return (
    <div>
      <div className="navbar">
        <nav>
          <ul className="nav-items">
            <div className="logo">
              <li>LOGO</li>
            </div>
            <div className="router-elements">
              <li>Home</li>
              <li>About</li>
              <li>Help</li>
            </div>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Navbar;
