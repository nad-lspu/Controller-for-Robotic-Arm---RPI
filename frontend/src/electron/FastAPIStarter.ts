import { ChildProcessWithoutNullStreams, spawn, exec } from "child_process";
import { getBackendPath } from "./UtilityModules.js";
import path from "path";

let uvicornProcess: ChildProcessWithoutNullStreams;

export function startBackendServer() {

    const venvBinPath = process.platform === 'win32' ? 'Scripts' : 'bin';
    const uvicornBinPath = process.platform === 'win32' ? 'uvicorn.exe' : 'uvicorn';
    const command = path.join('.venv', venvBinPath, uvicornBinPath);
    
    uvicornProcess = spawn(command, ['api.main:app'], { cwd: getBackendPath() });

    uvicornProcess.stdout.on('data', (data) => {
        console.log(`Uvicorn: ${data}`);
    })

    uvicornProcess.stderr.on('data', (data) => {
        console.log(`Uvicorn: ${data}`);
    });

    uvicornProcess.on('close', (code) => {
        console.log(`Uvicorn Process exited with code ${code}`);
    })
}

export async function waitServerStart(retries: number, interval: number): Promise<boolean> {
    for(let i = 1; i <= retries; i++) {
        try{
            const response = await fetch('http://localhost:8000');
            if (response.ok) {
                console.log('FastAPI successfully started!');
                return new Promise(resolve => resolve(true));
            }
        }
        catch {
            console.log(`Can't connect to FastAPI server. Retrying again. Attempts: ${i}`); 
        }
        await new Promise(resolve => setTimeout(resolve, interval));
    }

    return new Promise(resolve => resolve(false));
}

export function stopBackendServer() {
    try {
        uvicornProcess.kill();
    }
    catch {
        console.log('No Process to Kill');
    }
}



