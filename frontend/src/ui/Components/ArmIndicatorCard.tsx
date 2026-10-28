import Icons from "../Utilities/Icons"
import { type CSSProperties } from "react"
import './ArmIndicatorCard.css'

interface ArmIndicatorCardProps {
    data: ArmIndicatorData[]
}

interface ArmIndicatorData {
    title: string,
    angle: number,
    color: string,
}

const ArmIndicatorCard = ({ data }: ArmIndicatorCardProps) => {
    const armIndicatorData = data.map(item => 
        <ArmIndicatorItem
            title={item.title}
            angle={item.angle}
            color={item.color}
            key={item.title}
        />
    )
    return (
        <div className="arm-indicator-container">
            <section className="arm-indicator-title-icon">
                <Icons.ArrowDirection className="arm-indicator-icon" />
                <p>Arm Status</p>
            </section>
            <section className="arm-indicator-angle">
                {armIndicatorData}
            </section>
        </div>
    )
}

const ArmIndicatorItem = ({ title, angle, color }: ArmIndicatorData) => {

    const colorStyle = { "--custom-slider-color": color } as CSSProperties;

    return (
        <div style={colorStyle}>
            <span>{title}:</span>
            <div className="angle-indicator">
                <div className="angle-bg"style={colorStyle}></div>
                <p className="angle-text" style={colorStyle}>
                    {angle}&deg;
                </p>
            </div>
        </div>
    )
}

export default ArmIndicatorCard
