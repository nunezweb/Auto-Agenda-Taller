//import react into the bundle
import React from "react";
import { createRoot } from "react-dom/client";

//include your index.scss file into the bundle
// import "../styles/index.css";
import 'bootstrap/dist/css/bootstrap.min.css';

//import your own components
import Layout from "./layout";

// Get the DOM element where the React app will be rendered
const container = document.querySelector("#app");

// Create a root and render the application
const root = createRoot(container);
root.render(<Layout />);


// //import react into the bundle
// import React from "react";
// import ReactDOM from "react-dom";

// //include your index.scss file into the bundle
// // import "../styles/index.css";
// import 'bootstrap/dist/css/bootstrap.min.css';

// //import your own components
// import Layout from "./layout";

// //render your react application
// ReactDOM.render(<Layout />, document.querySelector("#app"));
