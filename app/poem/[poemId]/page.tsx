import PoemDetails from '../../components/poemdetails';
import sortedPoems from '../../../public/Poems_sorted.js';

export async function generateStaticParams() {
  const paths = sortedPoems.map((poem) => ({ params: { id: poem } }));
  return paths;
}

async function getData(params: { id: string }) {
  const res = await fetch(`https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.id}.json`);
  const data = await res.json();
  return data;
}

export default async function Page({ params }: { params: { id: string } }) {
  const data = await getData(params);
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