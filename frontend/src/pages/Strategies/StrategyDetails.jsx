import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useParams } from 'react-router-dom'

import { useGetStrategyDetailsQuery } from '../../services/strategiesAPI'

const StrategyDetails = () => {
    const { strategyCode } = useParams()
  const [strategyDetails, setStrategyDetails] = useState()
  const [strategyApplied, setStrategyApplied] = useState()

//   REDUX TOOLKIT CALL
  const {data, isFetching } = useGetStrategyDetailsQuery(strategyCode)
  // console.log(data)
  

  useEffect(() => {
    setStrategyDetails(data?.details[0])
    setStrategyApplied(data?.applied)
  },[isFetching])

  useEffect(() => {
    setStrategyDetails(data?.details[0])
    setStrategyApplied(data?.applied)
  },[])

  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        Strategy Details: {strategyDetails?.coingecko_id} {'>>'} {strategyDetails?.name}
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
      <div>
        <h3>Strategy applied to:</h3>
        <table className='mx-auto'>
          <thead>
            <tr>
              <th>Asset Type</th>
              <th>Symbol</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            {strategyApplied?.map((strat) => (
              <tr key={strat.id}>
                <td>{strat.asset_type}</td>
                <td>{strat.symbol}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default StrategyDetails