import React, { ReactNode } from 'react'
import Navbar from './Navbar'
import Footer from './Footer'

interface LayoutProps {
    children?: ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className='Layout'>
        <Navbar/>
        {/* <Content/> */}
        {children}
        <Footer/>
    </div>
  )
}

export default Layout