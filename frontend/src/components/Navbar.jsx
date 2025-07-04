import React from "react";
import { Link } from "react-router-dom";
import "../App.css";

const Navbar = () => {
  return (
    <div>
      {/* <div className="navbar">
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
      </div> */}
      <nav class="sticky top-0 my-5 mx-auto flex items-center justify-between bg-purple-700 p-4 rounded-b-md shadow-md">
        <div>
          <Link to="/">
            <h1 class="text-white text-2xl font-bold">Weather App</h1>
          </Link>
        </div>
        <div class="flex gap-x-6">
          <Link to="/">
            <h3 class="text-purple-100 hover:text-white text-lg font-medium transition-colors duration-200">
              Home
            </h3>
          </Link>
          <Link to="/">
            <h3 class="text-purple-100 hover:text-white text-lg font-medium transition-colors duration-200">
              About
            </h3>
          </Link>
          <Link to="/">
            <h3 class="text-purple-100 hover:text-white text-lg font-medium transition-colors duration-200">
              Help
            </h3>
          </Link>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;
