import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseURL = process.env.REACT_APP_DB_BASE_URL

export const stocksApi = createApi({
    reducerPath: 'stocksApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
    endpoints: (builder) => ({
        getStocks: builder.query({
            query: ({limit, filter}) => `/getAllStocks/${limit}?filter=${filter}`
        }),
        getStockDetails: builder.query({
            query: (symbol) => `/getStockDetails/${symbol}`
            // query: (id) => `getStockDetails/${id}`
        }),
    })
})

export const {
    useGetStocksQuery, useGetStockDetailsQuery,
} = stocksApi