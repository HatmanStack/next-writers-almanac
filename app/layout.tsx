'use client'
import React, { useState } from 'react';
import Sidebar from './components/sidebar'; 
import logo from './logo_writersalmanac.png'; 
import classNames from 'classnames';
import Head from 'next/head'; 
import Image from 'next/image';
import './ui/global.css'
import { PoemProvider } from './context/poemcontext';
import { AuthorProvider } from './context/authorcontext';


interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const [isShowingContentByDate, setIsShowingContentByDate] = useState(true);
    

    return (
        <html lang="en">
        <Head>
            <title>The Writer's Almanac</title> 
            <meta name="description" content="Project Description" /> {/* Meta description */}
            {/* Add other SEO meta tags as needed */}
        </Head>
        <body>
        <AuthorProvider>
        <PoemProvider>
        <div className="AppHeader">
            <Image className="LogoImage" src={logo} alt="LOGO" />
            <div className="FormattingContainer" />
            {/* Search component will go here */}
        </div>
        
        <div className={classNames({ ColumnContainer: !isShowingContentByDate })}>
            <Sidebar 
                    isShowingContentByDate={isShowingContentByDate}
                    setIsShowingContentByDate={setIsShowingContentByDate} 
                /> 
                <div className="MainContent">
                    
                    {children}
                </div>
            </div>
            </PoemProvider>
        </AuthorProvider>
            </body>
        </html>   
    );
};

export default Layout; 
