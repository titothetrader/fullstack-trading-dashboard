import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseURL = process.env.REACT_APP_DB_BASE_URL

export const cryptoApi = createApi({
    reducerPath: 'cryptoApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
    endpoints: (builder) => ({
        getCryptos: builder.query({
            query: (limit) => `/getAllCryptos/${limit}`
        }),
        getCryptoDetails: builder.query({
            query: (symbol) => `/getCryptoDetails/${symbol}`
            // query: (id) => `getStockDetails/${id}`
        }),
        getCryptoExchanges: builder.query({
            query: (limit) => `/getAllCryptoExchanges/${limit}`
        }),
        getCryptoExchangeDetails: builder.query({
            query: (exchange_id) => `/getCryptoExchangeDetails/${exchange_id}`
        }),
        getAllCoins: builder.query({
            query: (limit) => `/getAllCoins/${limit}`
        }),
        getCryptoCoin: builder.query({
            query: (symbol) => `/getCryptoCoin/${symbol}`
        })
    })
})

export const {
    useGetCryptosQuery, useGetCryptoDetailsQuery, useGetCryptoExchangesQuery, useGetCryptoExchangeDetailsQuery, useGetAllCoinsQuery, useGetCryptoCoinQuery,
} = cryptoApi