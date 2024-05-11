'use client';
import Link from 'next/link';

interface NavigationProps {
    prevLink: string;
    nextLink: string;
    children: React.ReactNode; 
}

const Navigation: React.FC<NavigationProps> = ({ prevLink, nextLink, children }) => {
  return (
    <div>
      <Link href={prevLink}>
      <button onClick={() => {}}> Previous </button>
      </Link>
      {children}
      <Link href={nextLink}>
      <button onClick={() => {}}> Next </button>
      </Link>
    </div>
  );
};

export default Navigation;