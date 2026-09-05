// API 服务地址配置
// - 开发环境:后端在本地运行时可改为 'http://localhost:5000'
// - 部署环境:通过环境变量 VITE_API_URL 指定后端地址;
//   未设置时默认使用同源地址(由反向代理将 /predictBreed 等请求转发到后端)
export const API_URL: string = import.meta.env.VITE_API_URL ?? ''
