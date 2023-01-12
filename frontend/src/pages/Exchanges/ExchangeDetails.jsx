import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetCryptoExchangeDetailsQuery } from '../../services/cryptoAPI'

const ExchangeDetails = () => {
  const { exchangeId } = useParams()

  const [exchangeDetails, setExchangeDetails] = useState()

  const { data, isFetching } = useGetCryptoExchangeDetailsQuery(exchangeId)

  const detailLabels = []
  
  useEffect(() => {
    // console.log(data)
    setExchangeDetails(data?.[0])
  }, [isFetching])

  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        Exchange Details: {exchangeDetails?.coingecko_id} {'>>'} {exchangeDetails?.name}
      </h1>
      <div className='my-8'>
        {exchangeDetails && Object.keys(exchangeDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {exchangeDetails[key]}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ExchangeDetails