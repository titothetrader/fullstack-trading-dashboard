import axios from 'axios'


export const getStocks = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:8000/getAllStocks")
        // console.log(response.data)
        return response.data
    } catch (error) {
        console.log(error)
    }
    
    // await axios.get(process.env.DB_BASE_URL)
}