import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseURL = process.env.REACT_APP_DB_BASE_URL

export const forexApi = createApi({
    reducerPath: 'forexApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
    endpoints: (builder) => ({
        getAllForex: builder.query({
            query: (limit) => `/getAllForex/${limit}`
        }),
        getForexDetails: builder.query({
            query: (symbol) => `/getForexDetails/${symbol}`
            // query: (id) => `getStockDetails/${id}`
        }),
    })
})

export const {
    useGetAllForexQuery, useGetForexDetailsQuery, 
} = forexApi