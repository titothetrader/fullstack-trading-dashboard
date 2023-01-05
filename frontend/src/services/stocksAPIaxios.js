import axios from 'axios'


export const getStocks = async (limit) => {
    try {
        const response = await axios.get(`${process.env.REACT_APP_DB_BASE_URL}/getAllStocks/${limit}`)
        // console.log(response.data)
        return response.data
    } catch (error) {
        console.log(error)
    }
}