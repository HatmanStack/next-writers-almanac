'use client'
 
import { useState, useEffect} from 'react'
import Sidebar from './sidebar';
import Image from 'next/image';
import logo from '../logo_writersalmanac.png'; 

export default function Passing({
  children,
}: {
  children: React.ReactNode
}) {

type ServerData = {
  author: string[];
  poemid: string[];
};
  
const [currentAuthor, setCurrentAuthor] = useState('');
const [currentPoem, setCurrentPoem] = useState('');
const [serverData, setServerData] = useState<ServerData | null>(null);;

useEffect(() => {
  const observer = new MutationObserver((mutationsList, observer) => {
    const serverDataElement = document.getElementById('server-data');
    if (serverDataElement && serverDataElement.textContent) {
      setServerData(JSON.parse(serverDataElement.textContent));
      observer.disconnect();
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });

  return () => observer.disconnect();
}, []);

  useEffect(() => {
    console.log('Checking serverData')
    if (serverData) {
      setCurrentAuthor(serverData.author[0]);
      setCurrentPoem(serverData.poemid[0]);
    }
  }, [serverData]);

  useEffect(() => {
    function handleScroll() {
        const header = document.querySelector('body > header');
        const scrollPosition = window.pageYOffset || document.documentElement.scrollTop;
    
        if (header) {
            if (scrollPosition > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
    }

    window.addEventListener('scroll', handleScroll);

    // Cleanup on unmount
    return () => {
        window.removeEventListener('scroll', handleScroll);
    };
}, []); 

  return (
    <div className="container">
    <div className="header">
      <Image className="LogoImage" src={logo} alt="LOGO" />
    </div>
    <div className="container-row">
    <div className="side"/>
      <Sidebar currentAuthor={currentAuthor} currentPoem={currentPoem} />
      
      {children}
      <div className="side"/>
      </div>
    </div>
  )

}

