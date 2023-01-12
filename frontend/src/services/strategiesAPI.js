import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseURL = process.env.REACT_APP_DB_BASE_URL

export const strategyApi = createApi({
    reducerPath: 'strategyApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
    endpoints: (builder) => ({
        getAllStrategies: builder.query({
            query: () => `/getAllStrategies`
        }),
        getStrategyDetails: builder.query({
            query: (strategyCode) => `/getStrategyDetails/${strategyCode}`
        })
    })
})

export const {
    useGetAllStrategiesQuery, useGetStrategyDetailsQuery,
} = strategyApi