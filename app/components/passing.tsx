'use client'
 
import { useState, useEffect} from 'react'
import Sidebar from './sidebar';
 
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

  return (
    <>
      <Sidebar currentAuthor={currentAuthor} currentPoem={currentPoem} />
      {children}
    </>
  )

}

