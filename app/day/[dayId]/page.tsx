import Poem from '../../components/poem';
import Note from '../../components/note';

export async function generateStaticParams() {
  return [{ params: { id: '01' } }, { params: { id: '02' } }];
}

async function getData(params: { id: string }) {
  const res = await fetch(
    `https://d3vq6af2mo7fcy.cloudfront.net/public/2017/01/${params.id}.json`
  );
  const data = await res.json();
  return data;
}

export default async function Page({ params }: { params: { id: string } }) {
  const data = await getData(params);

  return (
    <div className="main-content">
      <h1>{data.date}</h1>
      <h3>{data.dayOfWeek}</h3>
      <Poem
        poemTitle={data.poemTitle}
        poem={data.poem}
        poemByline={data.poemByline}
        author={data.author}
      />
      <Note note={data.notes} />
    </div>
  );
}