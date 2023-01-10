import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetCryptoDetailsQuery } from '../../services/cryptoAPI'

import { StockBarChart } from '../../components'

const CryptoDetails = () => {
  const { cryptoSymbol } = useParams()

  const [cryptoDetails, setCryptoDetails] = useState()
  const [cryptoPrices, setCryptoPrices] = useState()

  const { data, isFetching } = useGetCryptoDetailsQuery(cryptoSymbol)

  const detailLabels = []
  
  useEffect(() => {
    setCryptoDetails(data?.details?.[0])
    setCryptoPrices(data?.prices)
  }, [isFetching])

  // useEffect(() => {
  //   setBars(barsData?.[`0`])
  //   console.log(barsData)
  // }, [isFetchingBars])


  return (
    <div className='mt-6'>
      <h1 className='text-2xl h-16 underline bold'>
        Stock Details: {cryptoDetails?.exchange} {'>>'} {cryptoDetails?.symbol} {'>>'} {cryptoDetails?.name}
      </h1>
      <div className='my-8'>
        {cryptoDetails && Object.keys(cryptoDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {cryptoDetails[key]}</p>
          </div>
        ))}
      </div>
        {!isFetching && cryptoPrices &&
          <StockBarChart prices={cryptoPrices} />
        }
    </div>
  )
}

export default CryptoDetails