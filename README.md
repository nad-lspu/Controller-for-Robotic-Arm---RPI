# TRACE — Raspberry Pi Robotic Arm Controller

> **EXPERIMENTAL SOFTWARE — DEVELOPMENT AND TESTING ONLY**
>
> This project is under active development. Its current version has not been validated for safe operation on a physical Raspberry Pi robotic arm.
>
> **Do not connect powered motors or servos to this experimental version until hardware initialization, movement limits, emergency-stop functionality, and safety procedures have been tested.**

## 1. Project Overview

The TRACE Raspberry Pi Robotic Arm Controller is a software application designed to support robotic arm control, Python programming, and educational laboratory activities involving microcontroller interfacing.

The project includes:

- A Python FastAPI backend for controller operations and API communication.
- An Electron, React, and TypeScript frontend.
- Raspberry Pi GPIO and servo-control integration.
- Mock GPIO and servo implementations for Windows development.
- Experimental Python code validation and execution features.

This repository is one component of the larger **TRACE robotic arm development system**.

## 2. TRACE System Architecture

TRACE currently consists of two separate repositories.

| Repository | Purpose |
|---|---|
| [TRACE Controller](https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI) | Raspberry Pi-oriented controller application, including backend and frontend |
| TRACE Laboratory | Separate desktop programming and laboratory application; repository link to be added after publication |

The intended architecture is:

```text
TRACE Laboratory
(Desktop Application — Windows Development)
          |
          | HTTP API
          v
TRACE Controller
(FastAPI Backend)
          |
          v
GPIO / Servo Controller
          |
          v
Robotic Arm Hardware
```

The Controller repository also contains its own Electron frontend.

The intended deployment uses the Controller on a Raspberry Pi and the Laboratory on a separate computer. This networked arrangement has not yet been fully verified.

## 3. Technology Stack

**Backend**
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- OpenCV
- Raspberry Pi GPIO
- Adafruit ServoKit

**Frontend**
- Electron
- React
- TypeScript
- Vite
- Node.js

## 4. Current Development Status

The following functionality has been implemented or tested during development.

| Feature | Status |
|---|---|
| FastAPI backend startup on Windows | Verified |
| HTTP health-check endpoint | Verified |
| Windows mock GPIO support | Available; backend startup verified |
| Python code validation API | Implemented and tested for supported examples |
| Python demo execution API | Implemented and tested for supported examples |
| Fixed test-program execution | Implemented and tested |
| Test-program termination | Implemented and tested |
| Live test-program output API | Implemented and tested |
| Physical Raspberry Pi servo operation | Not validated in the current version |
| Full execution of editor-written Python programs | Not implemented |
| Complete computer vision workflow | Not fully verified |

### Python execution limitations

The current implementation distinguishes between demo execution and test-program execution.

**Demo execution** supports a restricted subset of Python consisting of simple `print()` statements with literal arguments. The validator limits input size and statement count and rejects imports.

This validation is **not a secure Python sandbox**.

**Run** currently executes the fixed backend script `backend/test_execution.py`, not arbitrary Python code written in the Laboratory editor.

**Stop** terminates the running test subprocess.

The backend provides a program-output endpoint that returns captured subprocess output, retaining up to 200 lines.

## 5. Project Structure

```text
rpi-robotic-arm-controller/
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   └── mRPi/
│   ├── execution_manager.py
│   ├── test_execution.py
│   ├── trace_controller.py
│   ├── requirements.txt
│   └── rpi-requirements.txt
├── frontend/
│   └── package.json
├── .gitignore
└── README.md
```

## 6. Windows Development Setup

The following setup is intended for development on Windows using mock GPIO hardware.

### Prerequisites

- Python 3.12 (verified with Python 3.12.10)
- Node.js and npm
- Git
- Windows development computer

### Clone the repository

```powershell
git clone https://github.com/nad-lspu/Controller-for-Robotic-Arm---RPI.git
cd Controller-for-Robotic-Arm---RPI
```

### Create a Python virtual environment

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install backend dependencies

```powershell
python -m pip install -r requirements.txt
```

The general dependency file contains packages for the FastAPI backend, authentication, database access, and computer vision.

The separate `rpi-requirements.txt` contains Raspberry Pi-specific GPIO and servo packages and should not be installed for ordinary Windows mock-hardware development.

### Start the backend

From the `backend` directory with the virtual environment activated:

```powershell
python -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

The backend startup and health check were verified on Windows using Python 3.12.10 and Uvicorn 0.54.0.

To test the health-check endpoint:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/
```

Expected message:

```text
Health Check Complete
```

Stop the backend using `Ctrl+C`.

### Start the Controller frontend

In a separate terminal, navigate to the `frontend` directory:

```powershell
cd frontend
npm install
npm run dev
```

The frontend's `package.json` also defines packaging scripts:

```text
npm run dist:win
npm run dist:linux
npm run dist:mac
```

These commands are configured in the project, but successful packaging and operation on every target platform have not been verified.

## 7. Raspberry Pi Development Considerations

The backend contains operating-system-specific hardware imports.

- Windows and macOS use local mock GPIO and ServoKit implementations.
- Linux currently imports Raspberry Pi GPIO and Adafruit ServoKit libraries.

The Raspberry Pi-specific dependency file is:

```text
backend/rpi-requirements.txt
```

**Hardware safety warning:** The controller's GPIO module currently initializes servo channels during Python module import. This can command physical servos to move when the backend starts.

The power-button shutdown callback is currently commented out. GPIO cleanup alone is not an emergency-stop mechanism.

Do not deploy this version to powered robotic arm hardware without reviewing and validating the startup sequence and independent safety controls.

## 8. Controller API

The backend defines a FastAPI application in:

```text
backend/api/main.py
```

The following routes have been implemented as part of the current TRACE development work:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Backend health check |
| POST | `/gpio/validate_code` | Validate supported demo Python statements |
| POST | `/gpio/execute_demo_code` | Execute supported demo print statements |
| POST | `/gpio/run_code` | Start the fixed test program |
| POST | `/gpio/terminate_code` | Stop the fixed test program |
| GET | `/gpio/program_output` | Retrieve captured test-program output |

Other API routes may be present in the existing application.

## 9. Known Issues and Limitations

The following issues have been observed or identified during TRACE development:

1. **Camera navigation issue:** Camera streaming works when the application first opens but may stop after navigating to another page and returning. The root cause has not been established.
2. **Activities page:** An `Unauthorized` message has been observed in the terminal, with a gray or blank application screen. The cause remains under investigation.
3. **Python editor execution:** The Run button currently launches a fixed test script instead of executing the editor's Python source.
4. **Python validation:** Demo validation accepts only a limited subset of Python. It is not a security boundary for arbitrary code execution.
5. **Hardware startup:** Servo initialization occurs during module import and may cause unexpected physical movement on Raspberry Pi hardware.
6. **Emergency stop:** A verified hardware emergency-stop system is not currently established.
7. **Network configuration:** Some development connections use hardcoded localhost addresses. Separate-computer operation requires additional configuration and testing.
8. **Computer vision:** Model-upload and complete computer vision workflows require further implementation or verification.
9. **Platform compatibility:** Full Raspberry Pi deployment and cross-platform desktop packaging have not been validated.

Some camera, Activities, and programming-editor issues are observed through the connected TRACE Laboratory application rather than solely within this Controller repository.

## 10. Planned Development

Future work includes:

- Configurable Controller IP address and API port.
- Reliable communication between the Raspberry Pi and Laboratory desktop.
- Safe execution of user-authored Python programs.
- Improved execution status and output handling.
- Camera reconnection and stream lifecycle fixes.
- Activities authentication and navigation fixes.
- Computer vision integration and testing.
- Physical robotic arm calibration and movement constraints.
- Verified hardware emergency-stop procedures.
- Raspberry Pi deployment testing.
- Cross-platform compatibility testing.

These are development goals, not completed features.

## 11. Attribution

This project is based on the original Raspberry Pi robotic arm controller work by **Mizuto911**.

Original repository:

https://github.com/Mizuto911/rpi-robotic-arm-controller

The TRACE development work includes modifications and experimental features involving Python code validation, demo execution, subprocess management, and live output retrieval.

Original authorship and commit history should be preserved.

**Licensing notice:** No license has been identified in the original repository. Attribution does not itself grant permission to redistribute or relicense the original source code. Public redistribution should be undertaken only after the appropriate permissions have been established.

## 12. Project Disclaimer

TRACE is currently an experimental educational and research development project.

The software is provided for development and evaluation, not as a certified or production-ready robotic arm control system.

Physical hardware testing must be conducted only after the relevant mechanical, electrical, software, and emergency-stop safeguards have been independently verified.