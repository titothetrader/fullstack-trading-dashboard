import React from 'react'

const LoadingSpinner = () => {
  return (
    <div className='w-full text-center'>
    <img 
        className="w-1/12 mx-auto"  
        src={require("../../../assets/images/Tensai-logo-symbol-anim.gif")}  
    />
</div>
  )
}

export default LoadingSpinner