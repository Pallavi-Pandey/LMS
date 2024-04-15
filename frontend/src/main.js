import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

  
router.beforeEach((to, from, next) => {
    if (to.name !== 'Login' && to.name !== 'Signup') {
      if (!localStorage.getItem('auth-token')) {
        next({ name: 'Login' })
      } else {
        next()
      }
    } else {
      next()
    }
  })
  

const app = createApp(App);
app.use(router);
app.mount('#app');
