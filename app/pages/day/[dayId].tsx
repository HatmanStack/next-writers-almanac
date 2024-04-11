import React from 'react'; 
import Layout from '../../layout'; 
import Poem from '../../components/poem';
import Note from '../../components/note';
import dayIds from '../../../public/Days_sorted.js';
import axios from 'axios';
import { GetStaticPropsContext, GetStaticPathsResult } from 'next'; 

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
      <div className="main-content">
        {/* Render day-specific data here */}
        <h1>{date}</h1>
        <h3>{dayOfWeek}</h3> 
        {/* ...Other Day components for transcript, etc. */}

        {/* TRANSCRIPT BUTTON */}
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
  const year = dayId?.substring(0, 4);
  const month = dayId?.substring(4, 6);
  const day = dayId?.substring(6, 8);

  // Fetch data based on 'dayId' from the CDN
  try {
    const response = await axios.get(`https://d3vq6af2mo7fcy.cloudfront.net/public/${year}/${month}/${day}.json`);
    const data = response.data;

      return {
        props: {
          dayofweek: data.dayofweek,
          date: data.date,
          transcript: data.transcript,
          poemtitle: data.poemtitle,
          poembyline: data.poembyline,
          author: data.author,
          poem: data.poem,
          notes: data.notes
        },
        revalidate: 60 * 60, // Example: Revalidate every hour (adjust as needed)
      };
  } catch (error) {
    console.log("DayId")
  }
}

export async function getStaticPaths(): Promise<GetStaticPathsResult> {
      const paths = dayIds.map(day => ({
        params: { dayId: day } 
    }));

    return {
      paths,
      fallback: false,
    };
  }

export default DayPage;
