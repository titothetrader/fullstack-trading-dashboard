import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { useGetStrategyDetailsQuery } from '../../services/strategiesAPI'

const StrategyDetails = () => {
    const { strategyCode } = useParams()
  const [strategyDetails, setStrategyDetails] = useState()

//   REDUX TOOLKIT CALL
  const {data, isFetching } = useGetStrategyDetailsQuery(strategyCode)
  console.log(data)
  

  useEffect(() => {
    setStrategyDetails(data[0])
  },[isFetching])

  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        Exchange Details: {strategyDetails?.coingecko_id} {'>>'} {strategyDetails?.name}
      </h1>
      <div className='my-8'>
        {strategyDetails && Object.keys(strategyDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {strategyDetails[key]}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default StrategyDetails