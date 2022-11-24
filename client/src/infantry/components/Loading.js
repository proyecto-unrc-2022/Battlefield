import React from 'react'

function Loading() {
    
    return ( 
        <div className='container'>

            <div className='row'>
                <div className='col'>
                    <div className="d-flex justify-content-center">
                        <div className="spinner-border" role="status">
                            <span className="sr-only "></span>
                        </div>
                    </div>
                </div>
            </div>
        
            
            <div className='row mt-3'>
                <div className='col'>
                    <h1>Waiting for player to join</h1>
                </div>
            </div>


        </div>

        
     );
}

export default Loading;