import DashboardHeader from "../DashboardHeader";
import './Vision.css';

const Vision = () => {
  return (
    <main className="vision-main-container">
        <DashboardHeader title="Vision" deviceState={true} />
        <section className="vision-content-container scrollable">
            <article className="vision-feed-container">
                <header>
                    <button className="vision-start-btn">Start Detection</button>
                    <button className="vision-stop-btn">Stop Detection</button>
                </header>
                <section className="vision-camera-feed">
                    Camera Feed
                </section>
            </article>
            <section className="vision-select-container">
                <label htmlFor="detection-model">Detection Model</label>
                <select name="detection-model" id="detection-model">
                    <optgroup label="Select a Model">
                        <option value="color">Color Detection</option>
                        <option value="shape">Shape Detection</option>
                        <option value="custom">Custom Model</option>
                    </optgroup>
                </select>
            </section>
        </section>
    </main>
  )
}

export default Vision