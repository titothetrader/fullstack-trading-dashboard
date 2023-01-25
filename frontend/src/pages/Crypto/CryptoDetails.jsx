import HTMLReactParser from 'html-react-parser'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { useGetCryptoDetailsQuery } from '../../services/cryptoAPI'

import { ApplyStrategy, StockBarChart, TradingViewWidget } from '../../components'

const CryptoDetails = () => {
  const { cryptoSymbol } = useParams()

  const [cryptoDetails, setCryptoDetails] = useState()
  const [cryptoPrices, setCryptoPrices] = useState()

  const { data: cryptoData, isFetching: isFetchingCrypto, isSuccess: isSuccessCrypto } = useGetCryptoDetailsQuery(cryptoSymbol)

  const detailLabels = []
  
  useEffect(() => {
    setCryptoDetails(cryptoData?.details?.[0])
    setCryptoPrices(cryptoData?.prices)
  }, [isFetchingCrypto])

  // useEffect(() => {
  //   setBars(barsData?.[`0`])
  //   console.log(barsData)
  // }, [isFetchingBars])


  return (
    <div className='mt-6'>
      <h1 className='text-lg h-16 underline bold'>
        Stock Details: {cryptoDetails?.exchange} {'>>'} {cryptoDetails?.symbol} {'>>'} {cryptoDetails?.name}
      </h1>
      { cryptoDetails?.exchange &&
        <TradingViewWidget exchange="binance" symbol={cryptoDetails?.symbol.replace("/", "")} />
      }
      <ApplyStrategy assetType="crypto" parentSymbol={cryptoDetails?.symbol} parentData={cryptoData} isParentSuccess={isSuccessCrypto} isParentFetching={isFetchingCrypto}/>
      <div className='my-8'>
        {cryptoDetails && Object.keys(cryptoDetails).map((key, i) => (
          <div key={i}>
            <div>
              
            </div>
            <p>{key}: {cryptoDetails[key]}</p>
          </div>
        ))}
      </div>
        {!isFetchingCrypto && cryptoPrices &&
          <StockBarChart prices={cryptoPrices} />
        }
    </div>
  )
}

export default CryptoDetails