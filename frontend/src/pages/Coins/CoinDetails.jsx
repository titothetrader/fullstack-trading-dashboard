import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetCryptoCoinQuery } from '../../services/cryptoAPI'


const CoinDetails = () => {
    const { coinSymbol } = useParams()

    const [coinDetails, setCoinDetails] = useState()
  
    const { data, isFetching } = useGetCryptoCoinQuery(coinSymbol)
  
    const detailLabels = []
    
    useEffect(() => {
      // console.log(data)
      setCoinDetails(data?.[0])
    }, [isFetching])

    return (
        <div className='mt-6'>
          <h1 className='text-lg h-16 underline bold'>
            Coin Details: {coinDetails?.coingecko_id} {'>>'} {coinDetails?.name}
          </h1>
          <div className='my-8'>
            {coinDetails && Object.keys(coinDetails).map((key, i) => (
              <div key={i}>
                <div>
                  
                </div>
                <p>{key}: {coinDetails[key]}</p>
              </div>
            ))}
          </div>
        </div>
      )
}

export default CoinDetails