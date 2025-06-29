import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

const Navbar = () => {
  return (
    <div>
      <div className="navbar">
        <nav>
          <ul className="nav-items">
            <div className="logo">
              <li>
                <Link id="link" to="/">
                  LOGO
                </Link>
              </li>
            </div>
            <div className="router-elements">
              <li>
                <Link id="link" to="/">
                  Home
                </Link>
              </li>
              <li>
                <Link id="link">About</Link>
              </li>
              <li>
                <Link id="link">Help</Link>
              </li>
            </div>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default Navbar;
