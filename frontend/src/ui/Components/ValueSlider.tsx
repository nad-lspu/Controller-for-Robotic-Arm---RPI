import Icons from "../Utilities/Icons";
import { useState, type ChangeEvent, type CSSProperties } from "react";
import "./ValueSlider.css";

interface ValueSliderProps {
  onChange: (angle: number, servo_channel: number) => void;
  channel: number;
  title: string;
  color?: string | undefined;
  startValue: number;
}

const ValueSlider = ({
  onChange,
  channel,
  title,
  color,
  startValue,
}: ValueSliderProps) => {
  const [angle, setAngle] = useState<number>(startValue);
  const colorStyle = { "--custom-slider-color": color } as CSSProperties;

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const angle: number = Number(event.target.value);
    setAngle(angle);
    onChange(angle, channel);
  }

  return (
    <section className="value-slider-container">
      <section className="reload-angle-section">
        <div className="reload-title-container">
          <div>
            <button style={colorStyle}></button>
            <Icons.Reload className="reload-button-icon" style={colorStyle} />
          </div>
          <p>{title}</p>
        </div>
        <div className="angle-indicator">
          <div className="angle-bg" style={colorStyle}></div>
          <p className="angle-text" style={colorStyle}>
            {angle}&deg;
          </p>
        </div>
      </section>
      <input
        type="range"
        className="range-slider"
        min={0}
        max={180}
        onChange={handleChange}
        style={colorStyle}
        value={angle}
      />
      <div className="range-slider-label">
        <p>0&deg;</p>
        <p>180&deg;</p>
      </div>
    </section>
  );
};

export default ValueSlider;
