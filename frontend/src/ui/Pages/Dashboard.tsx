import Icons from "../Utilities/Icons";
import { NavDrawerMenu } from "../Components/NavDrawer";
import { useState, useRef, useReducer, type JSX } from "react";
import useOutsideAlerter from "../Utilities/OutsideAlerter";
import Controller from "../Components/Tabs/Controller";
import Settings from "../Components/Tabs/Settings";
import Vision from "../Components/Tabs/Vision";
import DashboardTab from "../Components/Tabs/Dashboard";
import "./Dashboard.css";
import clsx from "clsx";

interface LogOutState {
  showLogOutButton: boolean;
  showLogOutPrompt: boolean;
}

interface LogOutAction {
  button?: boolean | undefined;
  prompt?: boolean | undefined;
}

function logOutReducer(state: LogOutState, action: LogOutAction) {
  const { button, prompt } = action;
  return {
    showLogOutButton: button !== undefined ? button : state.showLogOutButton,
    showLogOutPrompt: prompt !== undefined ? prompt : state.showLogOutPrompt,
  };
}

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState<JSX.Element>(<DashboardTab />);
  const [logOut, setLogOut] = useReducer(logOutReducer, {
    showLogOutButton: false,
    showLogOutPrompt: false,
  });
  const logOutButtonRef = useRef<HTMLButtonElement | null>(null);

  useOutsideAlerter(logOutButtonRef, () => {
    if (logOut.showLogOutButton && !logOut.showLogOutPrompt) {
      console.log("Outside Alerter Triggered!");
      setLogOut({ button: false });
    }
  });

  return (
    <main className="dashboard-container">
      <section className="nav-drawer">
        <div>
          <header>
            <Icons.AppLogo className="app-logo" />
            <h1>Trixie</h1>
          </header>
          <section className="search-box-container">
            <Icons.Search className="search-icon" />
            <input type="text" placeholder="Search" />
          </section>
          <NavDrawerMenu
            items={[
              {
                icon: Icons.Dashboard,
                title: "Dashboard",
                element: DashboardTab,
              },
              {
                icon: Icons.Controller,
                title: "Controller",
                element: Controller,
              },
              { icon: Icons.CameraOutline, title: "Vision", element: Vision },
              { icon: Icons.Settings, title: "Settings", element: Settings },
            ]}
            onClick={(selectedElement) => setActiveTab(selectedElement)}
          />
        </div>
        <section className="user-info-container">
          <img
            src="src/assets/default_user.png"
            alt="User Profile Picture"
            width={35}
            height={35}
          />
          <div>
            <h3>Juan Dela Cruz</h3>
            <p>XXXX-XXXX</p>
          </div>
          <div className="user-more-container">
            <Icons.TripleDot
              className="user-more"
              onClick={() => setLogOut({ button: true })}
            />
            <button
              className={clsx(
                "log-out-button",
                !logOut.showLogOutButton && "hide",
              )}
              onClick={() => setLogOut({ button: false, prompt: true })}
              ref={logOutButtonRef}
            >
              <Icons.LogOut className="log-out-button-icon" /> Log Out
            </button>
            {logOut.showLogOutPrompt && (
              <section className="log-out-prompt-bg">
                <div className="log-out-prompt-container">
                  <h2>Log Out</h2>
                  <p>Are you sure you want to leave?</p>
                  <div>
                    <button
                      className="yes-button"
                      onClick={() => console.log("ShutDown")}
                    >
                      Yes
                    </button>
                    <button
                      className="no-button"
                      onClick={() => setLogOut({ prompt: false })}
                    >
                      No
                    </button>
                  </div>
                </div>
              </section>
            )}
          </div>
        </section>
      </section>
      <section className="content-window">{activeTab}</section>
    </main>
  );
};

export default Dashboard;
