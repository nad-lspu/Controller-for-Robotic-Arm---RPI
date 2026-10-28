import { HashRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./Pages/Dashboard";
import LoadingScreen from "./Pages/LoadingScreen";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<LoadingScreen />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </HashRouter>
  );
}

export default App;
