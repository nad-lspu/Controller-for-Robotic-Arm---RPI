import path from "path";
import { app, ipcMain, WebContents } from 'electron';
import { pathToFileURL } from "url";

export function isDev() {
    return process.env.NODE_RUN_MODE === 'development';
}

export function getPreloadPath() {
    return path.join(
        app.getAppPath(),
        isDev() ? '.' : '..',
        'dist-electron/preload.cjs'
    )
}

export function getBackendPath() {
    return path.join(
        app.getAppPath(),
        isDev() ? '..' : '../..',
        'backend'
    );
}

export function getUIPath() {
    return path.join(
        app.getAppPath(),
        isDev() ? '..' : '../..',
        'dist-react/index.html'
    );
}

export function ipcMainHandle<Key extends keyof EventPayloadMapping>(
    key: Key,
    handler: (data?: EventPayloadMapping[Key]) => any
) {
    ipcMain.handle(key, (event, data) => {
        validateSenderFrame(event.senderFrame);
        return handler(data);
    });
}

export function ipcWebcontentsSend<Key extends keyof EventPayloadMapping>(
    key: Key,
    payload: EventPayloadMapping[Key],
    webcontents: WebContents
) {
    webcontents.send(key, payload);
}

export function ipcMainOn<Key extends keyof EventPayloadMapping>(
    key: Key,
    handler: (event:Electron.IpcMainEvent, payload: EventPayloadMapping[Key]) => void
) {
    ipcMain.on(key, (event, payload) => {
        validateSenderFrame(event.senderFrame);
        return handler(event, payload);
    });
}

function validateSenderFrame(senderFrame: Electron.WebFrameMain | null) {
    if (!senderFrame) {
        throw new Error('Access Denied. No Sender Frame Detected');
    }
    if (isDev() && new URL(senderFrame.url).host === 'localhost:5123') {
        return
    }
    if (senderFrame.url !== pathToFileURL(getUIPath()).toString()) {
        throw new Error('Malicious Event');
    }
}