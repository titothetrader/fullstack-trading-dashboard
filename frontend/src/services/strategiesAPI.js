import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

const baseURL = process.env.REACT_APP_DB_BASE_URL

export const strategyApi = createApi({
    reducerPath: 'strategyApi',
    baseQuery: fetchBaseQuery({ baseUrl: baseURL }),
    tagTypes: ['Strategy'],
    // credentials: 'same-origin',
    endpoints: (builder) => ({
        getAllStrategies: builder.query({
            query: () => `/getAllStrategies`,
            providesTags: ['Strategy']
        }),
        getStrategyDetails: builder.query({
            query: (strategyCode) => `/getStrategyDetails/${strategyCode}`
        }),
        applyStrategy: builder.mutation({
            query: (payload) => ({
                url: '/applyStrategy',
                method: 'POST',
                body: payload,
                // headers: {
                    // 'Content-type': 'application/json; charset=UTF-8' // Use this for JSON output, not inputs from forms
                // },
            }),
            invalidatesTags: ['Strategy']
        })
    })
})

export const {
    useGetAllStrategiesQuery, useGetStrategyDetailsQuery, useApplyStrategyMutation, 
} = strategyApi