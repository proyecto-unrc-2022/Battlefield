import React from 'react'
import user from "../assets/user-icon.svg"

const NavyUserCard = ({username, rol}) => {
  return (
    <div className='border border-dark p-1'>
      <div className='border border-dark rounded p-2'>
        <img src={user} alt="User"/>
      </div>
      <div>
        
      </div>
    </div>
  )
}

export default NavyUserCard