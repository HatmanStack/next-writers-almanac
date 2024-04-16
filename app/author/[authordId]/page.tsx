import AuthorDetails from '../../components/authordetails'; 
import sortedAuthors from '../../../public/Authors_sorted.js';

  export async function generateStaticParams() {
    const paths = sortedAuthors.map(author => ({ id: author }));
    return paths;
  }

  async function getData({ params }: { params: { slug: string } }) {
    const res = await fetch(`https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.id}.json`)
    const data = await res.text()
   
    return data
  }

  export default async function Page({ params }) {
    const data = await getData(params)
   
    return (
        <div className="main-content">
        <AuthorDetails 
          authorName={data.authorName}
          biography={data.biography}
          photos={data.photos}
          poems={data.poems}
        /> 
      </div>
    ); 
  }