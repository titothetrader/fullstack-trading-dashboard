import { useEffect, useState } from 'react'
import { skipToken } from '@reduxjs/toolkit/dist/query'

import { useApplyStrategyMutation, useGetAllStrategiesQuery } from '../../../services/strategiesAPI'
import { useNavigate } from 'react-router-dom'

const ApplyStrategy = (props) => {
    const [strategies, setStrategies] = useState()
    const [strategyId, setStrategyId] = useState()
    const navigate = useNavigate()
  
    // REDUX TOOLKIT CALL
    const {data, isFetching } = useGetAllStrategiesQuery(props.isParentSuccess ? props.parentData : skipToken)
    const [applyStrategy, {isLoading: isUpdating}] = useApplyStrategyMutation()
  
    useEffect(() => {
      setStrategies(data)
      // setLabelStrategy(data?.[0])
      // console.log(data)
      // console.log(data && Object.keys(data?.[0]))
    },[isFetching])

    const submitStrategy = (event) => {
      event.preventDefault()
      console.log(event.target.strategy_id.value, event.target.strategy_symbol.value)
      let asset_type = "stocks"
      let strategy_id = event.target.strategy_id.value
      let symbol = event.target.strategy_symbol.value
      applyStrategy({asset_type, strategy_id, symbol}).then(() => {
        let strat_code = ''
        strategies.map(strategy => {
          if (strategy["id"] == strategy_id) {
            strat_code = strategy["strategy_code"]
          }
          })
        // console.log(strat_code)
        navigate(`/strategies/${strat_code}`)
      })
    }

    const selectStrategyId = (event) => {
      setStrategyId(event.target.value)
      console.log(event.target.value)
    }

  return (
    <div>
      <div>
        <h2>Strategy Filter</h2>
      </div>
      <div>
        <form onSubmit={submitStrategy}>
          <select name="strategy_id" title="select strategy" onChange={selectStrategyId}>
            <option>Select Strategy</option>
            {strategies && strategies.map((strategy) => (
              <option key={strategy.id} value={strategy.id}>{strategy.name}
                {/* {console.log(strategy)} */}
              </option>
          ))}
          </select>
          <input type='text' name="strategy_symbol" defaultValue={props.parentSymbol} className='hidden'/>
          <button type="submit" className='block mx-auto'>Apply Strategy</button>
        </form>
      </div>
    </div>
  )
}

export default ApplyStrategy