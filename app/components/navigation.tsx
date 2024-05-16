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
    <div >
      <Link href={cleanPrevLink}>
      <button className="Card-Navigation-Button" id="left-button" onClick={() => {}}> &lt;</button>
      </Link>
      <div className="Card-Wrapper">
      {children}
      </div>
      <Link href={cleanNextLink}>
      <button className="Card-Navigation-Button" id="right-button" onClick={() => {}}> &gt;</button>
      </Link>
    </div>
  );
};

export default Navigation;