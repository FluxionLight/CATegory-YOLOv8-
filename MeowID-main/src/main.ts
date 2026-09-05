
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

// window.bootstrap = require('bootstrap');
import 'bootstrap/dist/css/bootstrap.css' // 引用bootstrap的样式
import 'bootstrap/dist/js/bootstrap.bundle.min.js' // 引用bootstrap的js
import 'bootstrap-icons/font/bootstrap-icons.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import 'animate.css';


const app = createApp(App)

app.use(ElementPlus)
app.use(router)


app.mount('#app')
