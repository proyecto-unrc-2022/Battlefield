import React from 'react'
import { useNavigate } from 'react-router-dom'
import NavyButton from './NavyButton'

const AccessDenied = ({text, buttonText, redirectTo}) => {

  const navigate = useNavigate()

  return (
    <>  
      <div className="row justify-content-center mt-5">
        <div className="col-12 text-center">
          <p className='navy-text'>{text}</p>
        </div>
        <div className="col-2 text-center">
          <NavyButton size={"small"} text={buttonText} action={() => navigate(redirectTo)}/>
        </div>
      </div>
    </>
  )
}

export default AccessDenied