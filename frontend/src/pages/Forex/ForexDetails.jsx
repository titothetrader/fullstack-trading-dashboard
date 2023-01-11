import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetForexDetailsQuery } from '../../services/forexAPI'

const ForexDetails = () => {
  const { forexPair } = useParams()

  const [forexPairDetails, setForexPairDetails] = useState()

  const { data, isFetching } = useGetForexDetailsQuery(forexPair)

  
  useEffect(() => {
    // console.log(data)
    setForexPairDetails(data?.[0])
  }, [isFetching])
  
  return (
    <div className='mt-6'>
      <h1 className='text-2xl h-16 underline bold'>
        FX Details: {forexPairDetails?.forex_pair} {'>>'} {forexPairDetails?.currency_a} / {forexPairDetails?.currency_b}
      </h1>
      <div className='my-8'>
        {forexPairDetails && Object.keys(forexPairDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {forexPairDetails[key]}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ForexDetails