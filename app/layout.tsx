'use client'
import React, { useState } from 'react';
import Sidebar from './components/sidebar'; 
import logo from './logo_writersalmanac.png'; 
import classNames from 'classnames';
import DayComponent from './pages/DayComponent'; // Fix the import path here
import Head from 'next/head'; 
import Image from 'next/image';
import './ui/global.css'
import { useRouter } from 'next/router';


interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
    const [isShowingContentByDate, setIsShowingContentByDate] = useState(true);
    const router = useRouter();

    let content;
    switch (router.pathname) {
        case '/day':
            content = <DayComponent />;
            break;
        case '/author':
            content = <AuthorComponent />;
            break;
        case '/poem':
            content = <PoemComponent />;
            break;
        default:
            content = children;
    }

    return (
        <div>
        <Head>
            <title>The Writer's Almanac</title> 
            <meta name="description" content="Project Description" /> {/* Meta description */}
            {/* Add other SEO meta tags as needed */}
        </Head>
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
                    {/* Transcript Component Might Go here */}
                     {content}
                </div>
            </div>
        </div>
        
        
        
    );
};

export default Layout; 
