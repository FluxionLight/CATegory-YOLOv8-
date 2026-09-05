// 网络请求封装
import axios from 'axios'
import {API_URL} from "../utils/connection";

// 创建一个axios实例
const request = axios.create({
    baseURL: API_URL, // 基础URL
    timeout: 100000 // 请求超时时间
});


export default request;