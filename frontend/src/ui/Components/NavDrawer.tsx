import { useState, type JSX } from 'react'
import { type IconType } from 'react-icons'
import clsx from 'clsx'
import './NavDrawer.css'

interface NavDrawerMenuProps {
  items: ItemData[],
  onClick: (selectedElement: JSX.Element) => void
}

type ItemData = {
  icon: IconType,
  title: string,
  element: () => JSX.Element,
}

interface NavDrawerItemProps {
  Icon: IconType
  title: string
  active?: boolean,
  onClick: () => void
}

export const NavDrawerMenu = ({ items, onClick }: NavDrawerMenuProps) => {
  const [activeIndex, setActiveIndex] = useState(0);
  const menus = items.map((item, index) => 
    <NavDrawerItem
      key={item.title}
      Icon={item.icon} 
      title={item.title} 
      active={activeIndex === index}
      onClick={
        () => {
          if (activeIndex === index) return;
          onClick(<item.element />);
          setActiveIndex(index);
        }
      }
    />)
  return (
    <section className='nav-drawer-menu'>
      {menus}
    </section>
  )
}

export const NavDrawerItem = ({ Icon, title, active, onClick }: NavDrawerItemProps) => {
    return (
        <div 
          className={clsx('nav-drawer-item', active ? 'nav-active' : '')}
          onClick={onClick}
        >
          <Icon className='nav-drawer-item-icon' /> {title}
        </div>
    )
}