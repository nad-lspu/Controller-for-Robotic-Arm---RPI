type ToggleLED = void;
type ServerStart = boolean;
type CloseApplication = void;
type ServoAngle = {
  angle: number | undefined;
  servo_channel: number | undefined;
};
type ServoWebSocketResult = boolean;
type CurrentServoAngles = {
  channel_0: number;
  channel_1: number;
  channel_2: number;
  channel_3: number;
  channel_4: number;
};
type CameraWebSocketResult = ArrayBuffer;

type EventPayloadMapping = {
  toggleLED: ToggleLED;
  serverStart: ServerStart;
  setServoAngle: ServoAngle;
  getCurrentAngles: CurrentServoAngles | null;
  closeApplication: CloseApplication;
  connectServoWS: ServoWebSocketResult;
  closeServoWS: void;
  connectCameraWS: CameraWebSocketResult;
  receiveCameraWSData: ArrayBuffer;
  closeCameraWS: void;
};

interface Window {
  electron: {
    serverStartListener: (callback: (connected: boolean) => void) => void;
    setServoAngle: (
      angle: number | undefined,
      servo_channel: number | undefined,
    ) => void;
    getCurrentAngles: () => Promise<CurrentServoAngles | null>;
    closeApplication: () => void;
    connectServoWS: () => Promise<ServoWebSocketResult>;
    closeServoWS: () => void;
    connectCameraWS: (callback: (imageBuffer: Blob) => void) => () => void;
    closeCameraWS: () => void;
  };
}
