import React from 'react'; 
import Layout from '../../layout'; 
import PoemDetails from '../../components/poemdetails'; 
import sortedPoems from '../../../public/Poems_sorted.js';
import { GetStaticPropsContext, GetStaticPathsResult } from 'next';
import axios from 'axios'; 

interface PoemPageProps {
  poemTitle: string; 
  poem: string; 
  authorName: string;
  analysis?: string; 
}

const PoemPage: React.FC<PoemPageProps> = ({ poemTitle, poem, authorName, analysis }) => {
    return (
        <Layout>
          <div className="main-content">
            <PoemDetails 
              poemTitle={poemTitle}
              authorName={authorName}
              poem={poem}
              analysis={analysis}
            /> 
          </div>
        </Layout>  
      );
};

export async function getStaticProps({ params }: GetStaticPropsContext<{ poemId: string }>) {
  const poemId = params?.poemId;

  try {
    const response = await axios.get(`https://d3vq6af2mo7fcy.cloudfront.net/public/poems/${poemId}.json`); 
    const data = response.data;

    return {
      props: {
        poemTitle: data.poemTitle,
        poem: data.poem,
        authorName: data.author,
        analysis: data.analysis
      },
      revalidate: 60 * 60,
    };
  } catch (error) {
    console.log("poemId")
  }
}

export async function getStaticPaths(): Promise<GetStaticPathsResult> {
  // Assuming 'sorted_Poems.js' has the format:
  // const sortedPoems = ['A. A. Milne', 'A. D. Hope', ...]

  const paths = sortedPoems.map(poem => ({
      params: { poemId: poem } 
  }));

  return {
    paths,
    fallback: false,
  };
}

export default PoemPage;
