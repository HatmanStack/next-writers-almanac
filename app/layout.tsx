'use client';
import Passing from './components/passing'; 
import React from 'react';

import classNames from 'classnames';
import Head from 'next/head'; 

import './ui/global.css'


interface LayoutProps {
    children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {

    
    
    return (
        <html lang="en">
            <Head>
                <title>The Writer's Almanac</title> 
                <meta name="description" content="Project Description" /> {/* Meta description */}
                {/* Add other SEO meta tags as needed */}
            </Head>
            <body>
                
                
                <div className={classNames({})}>
                    <Passing>                    
                        {children}
                    </Passing>
                </div>         
            </body>
        </html>   
    );
};

export default Layout; 
