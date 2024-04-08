import React from 'react'; 
import Layout from '../../components/layout'; 
import Poem from '../../components/Poem';
import Note from '../../components/Note';
import axios from 'axios';
import { GetStaticProps, GetStaticPaths } from 'next'; 

interface DayPageProps {
  dayOfWeek: string;
  date: string;
  transcript: string;
  poemTitle: string[]; 
  poemByline: string;
  author: string[]; 
  poem: string[]; 
  notes: string[]; 
}

const DayPage: React.FC<DayPageProps> = ({
  dayOfWeek,
  date,
  transcript,
  poemTitle,
  poemByline,
  author,
  poem,
  notes,
}) => {
  return (
    <Layout>
      <div className="sidebar">
        {/* Sidebar with Day/Author/Poem navigation will go here */}
      </div>
      <div className="main-content">
        {/* Render day-specific data here */}
        <h1>{date}</h1>
        <h3>{dayOfWeek}</h3> 
        {/* ...Other Day components for transcript, etc. */}

        <Poem 
          poemTitle={poemTitle}
          poem={poem}
          poemByline={poemByline}
          author={author}
        />
        <Note note={notes} />
      </div>
    </Layout>
  );
};

export async function getStaticProps({ params }: GetStaticPropsContext<{ dayId: string }>) {
  // Implement Data Fetching Logic Here...
  const dayId = params?.dayId;

  // Fetch data based on 'dayId' from the CDN
  const response = await axios.get(`https://d3vq6af2mo7fcy.cloudfront.net/public/${dayId}.json`);
  const data = response.data;

  return {
    props: {
      dayOfWeek: data.dayofweek,
      date: data.date,
      // ...etc, map the rest of your data 
    },
    revalidate: 60 * 60, // Example: Revalidate every hour (adjust as needed)
  };
}

export async function getStaticPaths(): Promise<GetStaticPathsResult> {
    const startDate = new Date(1993, 0, 1); // January 1st, 1993
    const endDate = new Date(2017, 10, 29); // November 29th, 2017
  
    const paths = [];
    let currentDate = startDate;
  
    while (currentDate <= endDate) {
      const dayId = currentDate.toISOString().slice(0, 10).replaceAll('-', ''); // Format as YYYYMMDD
      paths.push({ params: { dayId } });
  
      currentDate.setDate(currentDate.getDate() + 1); // Move to the next day
    }
  
    return {
      paths,
      fallback: false, // All valid paths are generated
    };
  }

export default DayPage;
