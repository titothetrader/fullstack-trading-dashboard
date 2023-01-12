import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useGetAllStrategiesQuery } from '../../services/strategiesAPI'


const Strategies = () => {
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
    <div className='responsive-container rounded-2xl'>
      <h1 className="text-3xl underlie">Strategies</h1>
      <table className="text-lg rounded-2xl mx-auto">
        <thead>
            <tr>
                {labelStrategy && Object.keys(labelStrategy).map((key, i) => (
                    <th key={i}>{key}</th>
                ))}
            </tr>
        </thead>
        <tbody>
      {strategies?.map((strategy) => (
        <tr key={Math.random()} className="even:bg-slate-900 odd:bg-slate-800 hover:bg-sky-900">
            {Object.keys(strategy).map((key) => 
                (   
                    <td key={Math.random()}>
                        {(key === 'name') && 
                            <Link className='link' to={`/strategies/${strategy.strategy_code}`}>
                                {strategy[key]}
                            </Link>
                        }
                        {(key !== 'name') && 
                            strategy[key]
                        }
                    </td>
                )
            )}
        </tr>
      ))}
      </tbody>
      </table>
    </div>
  )
}

export default Strategies