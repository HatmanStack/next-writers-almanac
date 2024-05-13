'use client'
import React, { useEffect, useState }   from 'react'; 

import Link from 'next/link';

type SidebarProps = {
    currentAuthor: string;
    currentPoem: string;
  };

const Sidebar: React.FC<SidebarProps> = ({currentAuthor, currentPoem}) => {
    const [currentDay, setCurrentDay] = useState('');
    
    
    useEffect(() => {
        const date = new Date();
        const formattedDate = `2013${(date.getMonth() + 1).toString().padStart(2, '0')}${(date.getDate()).toString().padStart(2, '0')}`;
        setCurrentDay(formattedDate);
        
    }, []);
    console.log('currentDay:', currentDay);
    console.log('currentAuthor:', currentAuthor);
    console.log('currentPoem:', currentPoem);
    return (
        <div className="Sidebar">
            <Link href={`/day/${currentDay}`}>
                <button onClick={() => {}}> Day </button>
            </Link>
            <Link href={`/author/${currentAuthor}`}>
                <button onClick={() => {}}> Author </button>
            </Link>
            <Link href={`/poem/${currentPoem}`}>
                <button onClick={() => {}}> Poem </button>
            </Link>
        </div>
    );
};

export default Sidebar;