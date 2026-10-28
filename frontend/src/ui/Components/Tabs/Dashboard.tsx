import DashboardHeader from "../DashboardHeader";
import Icons from "../../Utilities/Icons";
import { useState, useEffect, useRef } from "react";
import ArmIndicatorCard from "../ArmIndicatorCard";
import "./Dashboard.css";

const Dashboard = () => {
  const [cameraFeed, setCameraFeed] = useState<boolean>(false);
  const cameraFeedRef = useRef<HTMLImageElement | null>(null);
  const cameraFeedBlobURLRef = useRef<string | null>(null);
  const unsubscribeRef = useRef<(() => void) | null>(null);

  useEffect(() => {
    return closeCameraWS;
  }, []);

  function connectCameraWS() {
    unsubscribeRef.current = window.electron.connectCameraWS((imageBlob) => {
      const imageBlobURL = URL.createObjectURL(imageBlob);
      if (cameraFeedRef.current) cameraFeedRef.current.src = imageBlobURL;
      if (cameraFeedBlobURLRef.current)
        URL.revokeObjectURL(cameraFeedBlobURLRef.current);
      cameraFeedBlobURLRef.current = imageBlobURL;
    });
    setCameraFeed(true);
  }

  function closeCameraWS() {
    if (unsubscribeRef.current) {
      unsubscribeRef.current();
      window.electron.closeCameraWS();
    }
    setCameraFeed(false);
  }

  return (
    <main className="dashboard-main-container">
      <DashboardHeader title="Dashboard" deviceState={true} />
      <section className="dashboard-content-section scrollable">
        <h2>Welcome, Juan Dela Cruz!</h2>
        <article className="dashboard-indicator-container">
          <div className="device-indicator-card">
            <section className="device-indicator-title-icon">
              <p>Device Status</p>
              <Icons.DeviceIndicator className="device-indicator-card-icon" />
            </section>
            <h3>ONLINE</h3>
            <button>Disconnect Device</button>
          </div>
          <ArmIndicatorCard
            data={[
              {title: 'Base', angle: 0, color: '#4F78F6'},
              {title: 'Lower Arm', angle: 0, color: '#10b67f'},
              {title: 'Upper Arm', angle: 0, color: '#ae4ff6'},
              {title: 'Fore Arm', angle: 0, color: '#f6e34f'},
              {title: 'Claw', angle: 0, color: '#b6108c'},
            ]}
          />
        </article>
        <article className="camera-content-container">
          <div>
            <section className="camera-content-header"></section>
            <section className="camera-content">
              {cameraFeed ? (
                <img
                  className="camera-feed"
                  alt="RPi Cam Feed"
                  ref={cameraFeedRef}
                />
              ) : (
                <div className="camera-no-feed">
                  <div className="camera-icon-circle">
                    <Icons.Camera className="camera-icon" />
                  </div>
                  <p>No Camera Feed Available.</p>
                  <button
                    className="camera-connect-btn"
                    onClick={connectCameraWS}
                  >
                    Connect
                  </button>
                </div>
              )}
            </section>
          </div>
        </article>
      </section>
    </main>
  );
};

export default Dashboard;
