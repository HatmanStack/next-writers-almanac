import React, { useState } from 'react';
import Sidebar from './components/sidebar'; // We'll create this soon
import classNames from 'classnames'; 
import logo from './logo_writersalmanac.png'
import  sortedAuthors from '../public/Authors_sorted.js';
import  sortedPoems from '../public/Poems_sorted.js';

import '../css/App.css'; // Import your existing styles (adjust path if needed)

interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const [isShowingContentByDate, setIsShowingContentByDate] = useState(true);

    return (
        <div className="App"> 
            {/* Assuming width logic is handled via CSS for now, might need JavaScript if complex */}
           {/*  <ParticlesComponent /> */} 
            <div className="AppHeader">
                <img className="LogoImage" src={logo} alt="LOGO" />
                <div className="FormattingContainer" />
                {/* Search component will go here */}
            </div> 
            {/* Content Area */}
            <div className={classNames({ ColumnContainer: !isShowingContentByDate })}>
                <Sidebar 
                    isShowingContentByDate={isShowingContentByDate}
                    setIsShowingContentByDate={setIsShowingContentByDate} 
                /> 
                <div className="MainContent">
                    {/* Transcript Component Might Go here */}
                     {children} 
                </div>
            </div>
        </div>
    );
};

export default Layout; 
