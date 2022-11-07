import React, { useEffect } from 'react'
import NavyGameCard from '../components/NavyGameCard'
import NavyTitle from '../components/NavyTitle'
import NavyGameService from '../services/NavyGameService'

const NavyGames = () => {

  useEffect(() => {
    console.log("use effect")
  }, [])
  
  return (
    <div style={{flexGrow: "1"}} className="container-fluid bg-navy">
      <div className='row'>
        <div className='col-12 text-center'>
          <NavyTitle text={"Games"} size={4} />
        </div>
      </div>
      <div className='row'>
        <NavyGameCard />
      </div>
    </div>
  )
}

export default NavyGames