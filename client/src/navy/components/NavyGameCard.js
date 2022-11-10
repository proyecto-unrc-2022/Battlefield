import React from 'react'
import wings from "./../assets/wings.svg"
import NavyButton from './NavyButton'
import NavyUserCard from './NavyUserCard'

const NavyGameCard = () => {
  return (
    <div className='navy-card-container d-flex flex-column align-items-center border border-dark'>
      <div className=''>
        <img src={wings} alt="Wings"/>
      </div>
      <div className='d-flex'>
        <NavyUserCard />
        <p className='navy-text'>VS.</p>
        <NavyUserCard />
      </div>
      <div className='text-center'> 
        <NavyButton text={"join"} size={"small"}/>
      </div>
    </div>
  )
}

export default NavyGameCard