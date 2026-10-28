import electron from "electron";
import { ipcRenderer } from "electron";

electron.contextBridge.exposeInMainWorld("electron", {
  serverStartListener: (callback) =>
    ipcOn("serverStart", (event, data) => {
      callback(data);
    }),
  setServoAngle: (angle, servo_channel) =>
    ipcSend("setServoAngle", { angle, servo_channel }),
  getCurrentAngles: () => ipcInvoke("getCurrentAngles"),
  closeApplication: () => ipcInvoke("closeApplication"),
  connectServoWS: () => ipcInvoke("connectServoWS"),
  closeServoWS: () => ipcInvoke("closeServoWS"),
  connectCameraWS: (callback) => {
    ipcInvoke("connectCameraWS");
    return ipcOn("receiveCameraWSData", (event, data: ArrayBuffer) => {
      const imageBlob = new Blob([data], { type: "text/plain" });
      callback(imageBlob);
    });
  },
  closeCameraWS: () => ipcInvoke("closeCameraWS"),
} satisfies Window["electron"]);

function ipcInvoke<Key extends keyof EventPayloadMapping>(
  key: Key,
  payload?: EventPayloadMapping[Key],
) {
  return ipcRenderer.invoke(key, payload);
}

function ipcOn<Key extends keyof EventPayloadMapping>(
  key: Key,
  handler: (
    event: Electron.IpcRendererEvent,
    payload: EventPayloadMapping[Key],
  ) => void,
) {
  ipcRenderer.on(key, handler);
  return () => ipcRenderer.off(key, handler);
}

function ipcSend<Key extends keyof EventPayloadMapping>(
  key: Key,
  payload: EventPayloadMapping[Key],
) {
  ipcRenderer.send(key, payload);
}
