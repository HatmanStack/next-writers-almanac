'use client'
import React, { useEffect, useState, useRef }   from 'react'; 
import '../ui/sidebar.css';
import Link from 'next/link';

type SidebarProps = {
    currentAuthor: string;
    currentPoem: string;
  };

const Sidebar: React.FC<SidebarProps> = ({currentAuthor, currentPoem}) => {
    const [currentDay, setCurrentDay] = useState('');

    useEffect(() => {
        const SidebarContainer = document.querySelector('.SidebarContainer') as HTMLElement;
        window.addEventListener('scroll', function() {
            if (window.scrollY > 0) {
                SidebarContainer.style.width = '100px';
                
            }else {
                SidebarContainer.style.width = '40px';
            }
          });
        SidebarContainer.addEventListener('mouseover', function() {
            SidebarContainer.style.width = '100px';
        });
    
        SidebarContainer.addEventListener('mouseout', function() {
          if (window.scrollY > 0) {
            SidebarContainer.style.width = '50px';
          }
        });

      }, []);
    
    useEffect(() => {
        const date = new Date();
        const formattedDate = `2013${(date.getMonth() + 1).toString().padStart(2, '0')}${(date.getDate()).toString().padStart(2, '0')}`;
        setCurrentDay(formattedDate);
        
    }, []);

    console.log('currentDay:', currentDay);
    console.log('currentAuthor:', currentAuthor);
    console.log('currentPoem:', currentPoem);
    return (
        
        <div className="SidebarContainer">
            <Link href={`/day/${currentDay}`}>
                <button className="Sidebar-Button" onClick={() => {}}>Today</button>
            </Link>
            <Link href={`/author/${currentAuthor}`}>
                <button className="Sidebar-Button" onClick={() => {}}>Author</button>
            </Link>
            <Link href={`/poem/${currentPoem}`}>
                <button className="Sidebar-Button" onClick={() => {}}>Poem</button>
            </Link>
        </div>
        
    );
};

export default Sidebar;