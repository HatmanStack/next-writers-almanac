import React, { useState, useEffect } from 'react';
import Sidebar from './sidebar'; 
import Head from 'next/head'; 
import  sortedAuthors from '../../public/Authors_sorted.js';
import  sortedPoems from '../../public/Poems_sorted.js';
import dayIds from '../../public/Days_sorted.js';

// ... your other imports 

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isShowingContentByDate, setIsShowingContentByDate] = useState(true);

  // Fetch data only once on component mount
  useEffect(() => {
    // Since 'sortedAuthors' and 'sortedPoems' are static you 
    // don't need to fetch them from an external source.
  }, []);

   // ... rest of your Layout component logic
 
  return (
    
      <div className="App"> 
      <Head>
        <title>Your Project Title</title> {/* Set your project's title */}
        <meta name="description" content="Project Description" /> {/* Meta description */}
        {/* Add other SEO meta tags as needed */}
      </Head>

      <Sidebar 
        isShowingContentByDate={isShowingContentByDate}
        setIsShowingContentByDate={setIsShowingContentByDate} 
        sortedAuthors={sortedAuthors}  
        sortedPoems={sortedPoems} 
        dayIds={dayIds} 
      /> 
      <div className="Main-Content">
        {children} 
      </div>
    </div>
  );
};

export default Layout; 
