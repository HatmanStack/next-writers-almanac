'use client';
import Link from 'next/link';


interface NavigationProps {
  prevLink: string;
  nextLink: string;
  children: React.ReactNode; 
}

const Navigation: React.FC<NavigationProps> = ({ prevLink, nextLink, children }) => {
  const cleanPrevLink = prevLink.replace('.json', '');
  const cleanNextLink = nextLink.replace('.json', '');
  
  return (
    <div className="Card-Wrapper">
      <Link href={cleanPrevLink}>
      <button onClick={() => {}}> Previous </button>
      </Link>
      {children}
      <Link href={cleanNextLink}>
      <button onClick={() => {}}> Next </button>
      </Link>
    </div>
  );
};

export default Navigation;