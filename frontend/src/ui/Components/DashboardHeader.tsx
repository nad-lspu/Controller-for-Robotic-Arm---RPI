import Icons from '../Utilities/Icons'
import './DashbaordHeader.css'
import clsx from 'clsx'

interface DashboardHeaderProps {
    title: string,
    deviceState: boolean,
}

const DashboardHeader = ({ title, deviceState }: DashboardHeaderProps) => {
  return (
    <section className='dashboard-header-container'>
        <h1>{title}</h1>
        <div className={clsx('device-indicator-container', !deviceState && 'offline')}>
            <Icons.DeviceIndicator className='device-indicator-icon' />
            {deviceState ? 'Connected' : 'Not Connected'}
        </div>
    </section>
  )
}

export default DashboardHeader