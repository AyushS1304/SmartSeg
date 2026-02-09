import React from "react";
import { Routes, Route } from "react-router-dom";

import Upload from "./components/Upload";
import Result from "./components/Result";


function App() {
  return (
    
      // <Navbar />
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/result" element={<Result />} />
      </Routes>
   
  );
}

export default App;
