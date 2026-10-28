import DashboardHeader from "../DashboardHeader";
import ValueSlider from "../ValueSlider";
import { useEffect, useState } from "react";
import Icons from "../../Utilities/Icons";
import "./Controller.css";

const Controller = () => {
  const [servoAngles, setServoAngles] = useState<
    CurrentServoAngles | undefined
  >(undefined);

  useEffect(() => {
    async function connectWebSocket() {
      const connected = await window.electron.connectServoWS();
      console.log("Connected:", connected);
    }
    connectWebSocket();
    return window.electron.closeServoWS;
  }, []);

  useEffect(() => {
    async function getCurrentAngles() {
      const servoData = await window.electron.getCurrentAngles();
      if (!servoData) {
        setServoAngles({
          channel_0: 90,
          channel_1: 25,
          channel_2: 0,
          channel_3: 80,
          channel_4: 90,
        });
        return;
      }
      setServoAngles(servoData);
    }
    getCurrentAngles();
  }, []);

  function setServoAngle(angle: number, servo_channel: number) {
    window.electron.setServoAngle(angle, servo_channel);
  }

  return servoAngles !== undefined ? (
    <main className="controller-main-container">
      <DashboardHeader title="Arm Controller Panel" deviceState={true} />
      <section className="controller-panel-section scrollable">
        <h2>Adjust individual joint positions.</h2>
        <ValueSlider
          onChange={setServoAngle}
          channel={0}
          title="Base"
          color="#4F78F6"
          startValue={servoAngles.channel_0}
        />
        <ValueSlider
          onChange={setServoAngle}
          channel={1}
          title="Lower Arm"
          color="#10b67f"
          startValue={servoAngles.channel_1}
        />
        <ValueSlider
          onChange={setServoAngle}
          channel={2}
          title="Upper Arm"
          color="#ae4ff6"
          startValue={servoAngles.channel_2}
        />
        <ValueSlider
          onChange={setServoAngle}
          channel={3}
          title="Fore Arm"
          color="#f6e34f"
          startValue={servoAngles.channel_3}
        />
        <ValueSlider
          onChange={setServoAngle}
          channel={4}
          title="Claw"
          color="#b6108c"
          startValue={servoAngles.channel_4}
        />
      </section>
    </main>
  ) : (
    <main className="controller-main-loading">
      <section className="loading-container">
        <Icons.Loading className="loading-circle" />
        <p>Loading...</p>
      </section>
    </main>
  );
};

export default Controller;
