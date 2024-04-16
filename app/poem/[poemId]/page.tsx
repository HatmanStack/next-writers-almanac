import PoemDetails from '../../components/poemdetails'; 
import sortedPoems from '../../../public/Poems_sorted.js';

  export async function generateStaticParams() {
    const paths = sortedPoems.map(poem => ({ id: poem }));
    return paths;
  }

  async function getData(params) {
    const res = await fetch(`https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.id}.json`)
    const data = await res.text()
   
    return data
  }

  export default async function Page({ params }) {
    const data = await getData(params)
   
    return (
        <div className="main-content">
            <PoemDetails 
              poemTitle={data.poemTitle}
              authorName={data.authorName}
              poem={data.poem}
              analysis={data.analysis}
            /> 
          </div>
    ); 
  }