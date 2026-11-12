import { BrowserWindow, app } from "electron";
import path from "path";
import {
  isDev,
  getPreloadPath,
  ipcMainHandle,
  ipcWebcontentsSend,
  ipcMainOn,
} from "./UtilityModules.js";
import { getCurrentAngles } from "./DataFetching.js";
import {
  startBackendServer,
  waitServerStart,
  stopBackendServer,
} from "./FastAPIStarter.js";

const BACKEND_CONNECTION_RETRIES = 10;
const BACKEND_CONNECTION_INTERVAL_MS = 5000;
let wsServo: WebSocket | null = null;
let wsCamera: WebSocket | null = null;

app.on("ready", async () => {
  const mainWindow = new BrowserWindow({
    webPreferences: {
      preload: getPreloadPath(),
    },
    height: 600,
    width: 1024,
    autoHideMenuBar: true,
    backgroundColor: "#505050",
  });

  if (isDev()) mainWindow.loadURL("http://localhost:5123");
  else
    mainWindow.loadFile(path.join(app.getAppPath(), "dist-react/index.html"));

  ipcMainHandle("closeApplication", () => app.quit());

  ipcMainHandle("connectServoWS", () => {
    wsServo?.close();
    wsServo = new WebSocket("ws://localhost:8000/gpio/ws-servo");
    wsServo.onopen = () => console.log("Servo Websocket Connected!");
    wsServo.onclose = () => console.log("Servo Websocket Disconnected!");
    return !!wsServo;
  });

  ipcMainHandle("getCurrentAngles", () => {
    return getCurrentAngles();
  });

  ipcMainOn("setServoAngle", (_, data) => {
    wsServo?.send(JSON.stringify(data));
  });

  ipcMainHandle("closeServoWS", () => {
    wsServo?.close();
    wsServo = null;
  });

  ipcMainHandle("connectCameraWS", () => {
    // Never leave a previous socket open; it would keep the camera busy.
    wsCamera?.close();
    wsCamera = new WebSocket("ws://localhost:8000/gpio/cam");
    wsCamera.onopen = () => console.log("Camera WebSocket Connected!");
    wsCamera.onclose = () => console.log("Camera WebSocket Disconnected!");
    wsCamera.onerror = (error) =>
      console.log("Error on Camera Websocket:", error);
    wsCamera.onmessage = async (event) => {
      const imageBlob = event.data as Blob;
      const imageArrayBuffer = await imageBlob.arrayBuffer();
      ipcWebcontentsSend(
        "receiveCameraWSData",
        imageArrayBuffer,
        mainWindow.webContents,
      );
    };
  });

  ipcMainHandle("closeCameraWS", () => {
    wsCamera?.close();
    wsCamera = null;
  });

  startBackendServer();
  const connected = await waitServerStart(
    BACKEND_CONNECTION_RETRIES,
    BACKEND_CONNECTION_INTERVAL_MS,
  );

  if (connected) {
    ipcWebcontentsSend("serverStart", true, mainWindow.webContents);
  } else {
    ipcWebcontentsSend("serverStart", false, mainWindow.webContents);
  }
});

app.on("quit", () => {
  stopBackendServer();
});
