import axios from 'axios';

const baseUrl = 'http://127.0.0.1:5000/api/';
const instance = axios.create({
    baseURL: baseUrl,
    timeout: 5000
})

export default instance;
