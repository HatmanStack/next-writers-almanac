import React from 'react'; 
import Layout from '../../components/layout'; 
import PoemDetails from '../../components/poemdetails'; 
import { GetStaticProps, GetStaticPaths } from 'next';
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
          <div className="sidebar"> 
            {/* Sidebar with Day/Author/Poem navigation will go here */}
          </div>
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
    const response = await axios.get(`/poems/${poemId}.json`); 
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
    // ... error handling 
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
