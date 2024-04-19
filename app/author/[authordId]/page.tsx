import AuthorDetails from '../../components/authordetails';
import sortedAuthors from '../../../public/Authors_sorted.js';

export async function generateStaticParams() {
  const paths = sortedAuthors.map((author) => ({ params: { id: author } }));
  return paths;
}

async function getData(params: { id: string }) {
  const res = await fetch(
    `https://d3vq6af2mo7fcy.cloudfront.net/public/authors/${params.id}.json`
  );
  const data = await res.json();
  return data;
}



export default async function Page({ params }: { params: { id: string } }) {
  const data = await getData(params);

  return (
    <main className="main-content">
      <AuthorDetails
        authorName={data.authorName}
        biography={data.biography}
        photos={data.photos}
        poems={data.poems}
      />
    </main>
  );
}