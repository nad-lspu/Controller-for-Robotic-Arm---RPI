# Raspberry Pi Robotic Arm Controller Application

This Application is a system that is responsible for interacting with Raspberry Pi to control the Robotic Arm. This Application will also contain college level laboratory activities to aid in teaching microcontroller interfacing. This is powered by Electron.js, Node.js, and Python in Raspberry Pi.

## How to Set Up this System

_Note that you can only set this up if you are a collaborator on this repository._

### 1. Clone this repository on your code editor

To do this, you can run the following code.

```
git clone https://github.com/Mizuto911/rpi-robotic-arm-app.git
```

### 2. Open the Frontend Project Directory

Change your directory to the frontend project directory with the following command:

```
cd frontend
```

### 3. Download required dependencies of the Frontend System

Open the project folder in your code editor. Run the following code in your terminal:

```
npm install
```

### 4. Open the Backend Project Directory

Change your directory to the frontend project directory with the following command _(Starting from the Frontend Directory)_:

```
cd ../backend
```

### 5. Set Up your Python Virtual Environment

Set up a virtual environment and activate it with the commands below:

_If you are in Windows,_

```
py -3 -m venv .venv
.venv/Scripts/activate
```

_and if you are in RPi OS or Linux_

```
python3 -m venv .venv
source .venv/bin/activate
```

### 6. Download required dependencies of the Backend System

Open the project folder in your code editor. Run the following code in your terminal:

```
pip install fastapi[all]
```

### 7. Run the Application

Go to the Frontend Project Directory with this command _(Starting from the Backend Directory)_:

```
cd ../frontend
```

**There is two ways to run this application.**

1. To run the application in development mode, run the following code:

```
npm run dev
```

2. To export the application, run the following code:

```
npm run dist:<your_platform>
```

Currently there are **3 platforms** supported for this application to export:

- Windows (win)
- Mac (mac)
- Linux (linux)

So if you want to export this application as a **Windows** app, run the following:

```
npm run dist:win
```

_After the application finishes exporting, you can go to the dist folder of your project folder and locate the exported application and open it to launch the application._

## Making a Github Branch

You may edit the code as you wish, but remember to make your own branch and push the code there first. If the code passes inspection, then we will merge it with main.

You can run the following code to make your own branch:

```
git switch -c <your-branch-name>
...
<Commit and Push code>
```

### Enjoy!

Feel free to explore and code, just remember to **not edit the main branch directly.**
