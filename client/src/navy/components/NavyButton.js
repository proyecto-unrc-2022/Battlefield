import React from 'react'
import "./NavyButton.css"
import "./../index.css"

const NavyButton = ({text}) => {
  return (
    <div className='navy-button rounded w-100 border border-dark text-uppercase navy-text my-1'>{text}</div>
  )
}

export default NavyButton