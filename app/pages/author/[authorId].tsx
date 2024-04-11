import React from 'react'; 
import Layout from '../../layout'; 
import AuthorDetails from '../../components/authordetails'; 
import { GetStaticPropsContext, GetStaticPathsResult } from 'next'; 
import sortedAuthors from '../../../public/Authors_sorted.js';
import axios from 'axios'; 

interface AuthorPageProps {
  authorName: string;
  biography: string; 
  photos: string[]; 
  poems: { [poemName: string]: string };
}

const AuthorPage: React.FC<AuthorPageProps> = ({ authorName, biography, photos, poems }) => {
    return (
        <Layout> {/* Wrap with your Layout component */}
          
          <div className="main-content">
            <AuthorDetails 
              authorName={authorName}
              biography={biography}
              photos={photos}
              poems={poems}
            /> 
          </div>
        </Layout>  
      );
};

export async function getStaticProps({ params }: GetStaticPropsContext<{ authorId: string }>) {
  const authorId = params?.authorId;

  try {
    const response = await axios.get(`https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${authorId}.json`); 
    const data = response.data;

    return {
      props: {
        authorName: authorId,
        biography: data.biography,
        photos: data.photos,
        poems: data.poems
      },
      revalidate: 60 * 60,
    };
  } catch (error) {
    console.log("AuthorID")
  }
}

export async function getStaticPaths(): Promise<GetStaticPathsResult> {
  // Assuming 'sorted_Authors.js' has the format:
  // const sortedAuthors = ['Dante Gabriel Rossetti', 'Emily Dickinson', ...]

  const paths = sortedAuthors.map(author => ({
      params: { authorId: author } 
  }));

  return {
    paths,
    fallback: false,
  };
}

export default AuthorPage;
