'use client'
import React, { useEffect, useState, useRef }   from 'react'; 

import Link from 'next/link';

type SidebarProps = {
    currentAuthor: string;
    currentPoem: string;
  };

const Sidebar: React.FC<SidebarProps> = ({currentAuthor, currentPoem}) => {
    const [currentDay, setCurrentDay] = useState('');
    const dayButtonRef = useRef<HTMLButtonElement>(null); 
    const [isCollapsed, setIsCollapsed] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setIsCollapsed(true);
        }, 3000);

        return () => clearTimeout(timer);
    }, []);
    
    useEffect(() => {
        const date = new Date();
        const formattedDate = `2013${(date.getMonth() + 1).toString().padStart(2, '0')}${(date.getDate()).toString().padStart(2, '0')}`;
        setCurrentDay(formattedDate);
        
    }, []);

    useEffect(() => {
        if (dayButtonRef.current) {
            dayButtonRef.current.click(); // Click the Day button programmatically
        }
    }, [currentDay]); 

    console.log('currentDay:', currentDay);
    console.log('currentAuthor:', currentAuthor);
    console.log('currentPoem:', currentPoem);
    return (
        <div className={`Sidebar ${isCollapsed ? 'collapsed' : ''}`}>
        <div className="Sidebar">
            <Link href={`/day/${currentDay}`}>
                <button className="Sidebar-Button" ref={dayButtonRef} onClick={() => {}}>Today</button>
            </Link>
            <Link href={`/author/${currentAuthor}`}>
                <button className="Sidebar-Button" onClick={() => {}}>Author</button>
            </Link>
            <Link href={`/poem/${currentPoem}`}>
                <button className="Sidebar-Button" onClick={() => {}}>Poem</button>
            </Link>
        </div>
        </div>
    );
};

export default Sidebar;