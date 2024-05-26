'use client';
import React, { useEffect }  from 'react';
import Logo from './logo';
import Search from './search';
import DateDisplay from './datedisplay';
import '../ui/header.css';


// Add the missing import statement for the './logo' module

namespace Heading {
    export interface Props {
        date: Date;
    }
}

const Heading: React.FC<Heading.Props> = ({ date }) => {

  
  useEffect(() => {
    const headerContainer = document.querySelector('.HeaderContainer') as HTMLElement;

    window.addEventListener('scroll', function() {
      if (window.scrollY > 0) {
        headerContainer.style.height = '5vh';
      } else {
        headerContainer.style.height = '15vh';
      }
    });

    headerContainer.addEventListener('mouseover', function() {
      headerContainer.style.height = '15vh';
    });

    headerContainer.addEventListener('mouseout', function() {
      if (window.scrollY > 0) {
        headerContainer.style.height = '5vh';
      }
    });
  }, []);

  return (
    <header>
      <div className="HeaderContainer">
      <Logo />
      <Search />
      <DateDisplay onDateChange={date => console.log(date)}/>
      </div>
    </header>
  );
};

export default Heading;