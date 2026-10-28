import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Icons from "../Utilities/Icons";
import "./LoadingScreen.css";

const LoadingScreen = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const unsubscribe = window.electron.serverStartListener((connected) => {
      setLoading(connected);
      console.log(`Server Connected: ${connected}`);

      if (connected) {
        navigate("/dashboard");
      }
    });
    return unsubscribe;
  }, []);

  return loading ? (
    <main className="loading-container">
      <Icons.Loading className="loading-circle" />
      <p>Connecting to Server...</p>
    </main>
  ) : (
    <main className="failed-dialog-container">
      <div>
        <h2>Failed to Open</h2>
        <p>
          The backend server has failed to load. Please try to open the app
          again.
        </p>
        <button onClick={window.electron.closeApplication}>Close App</button>
      </div>
    </main>
  );
};

export default LoadingScreen;
