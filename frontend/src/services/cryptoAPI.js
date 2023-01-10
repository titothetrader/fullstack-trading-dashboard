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
    })
})

export const {
    useGetCryptosQuery, useGetCryptoDetailsQuery,
} = cryptoApi