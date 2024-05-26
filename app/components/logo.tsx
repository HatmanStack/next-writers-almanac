import React from 'react';
import Image from 'next/image';
import logo from '../logo_writersalmanac.png';

const Logo: React.FC = () => {
  return (
    
      <Image className="LogoImage" src={logo} alt="LOGO" />
    
)};

export default Logo;