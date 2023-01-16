import { useEffect, useState } from 'react'

import { useGetAllStrategiesQuery } from '../../../services/strategiesAPI'

const StrategyFilter = () => {
    const [strategies, setStrategies] = useState()
    const [labelStrategy, setLabelStrategy] = useState()
  
    // REDUX TOOLKIT CALL
    const {data, isFetching } = useGetAllStrategiesQuery()
    // console.log(data)
    
  
    useEffect(() => {
      setStrategies(data)
      setLabelStrategy(data?.[0])
    },[isFetching])

  return (
    <div>StrategyFilter
        {console.log(strategies)}
    </div>
  )
}

export default StrategyFilter