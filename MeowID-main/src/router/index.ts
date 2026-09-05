import { createRouter, createWebHistory } from 'vue-router'
import DashBoardView from '../views/DashBoard.vue'


const router = createRouter({
  // history: createWebHistory(import.meta.env.BASE_URL), //开发使用根路径
  history: createWebHistory('/meowid/'), //部署使用 /meowid/ 路径作为 应用的基础路径

  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashBoardView
    },
  ],
})

// 路由守卫
router.beforeEach((to, _, next) => {
  console.log('Navigating to:', to.path); // 添加日志
  next();  // 确保调用 next()，让路由继续
});

export default router
