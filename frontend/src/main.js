import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

  
router.beforeEach((to, from, next) => {
    // Check if the route is not 'Login' or 'Signup'
    if (to.name !== 'Login' && to.name !== 'Signup') {
      // Check if the user is not authenticated
      if (!localStorage.getItem('auth-token')) {
        // Redirect to the 'Login' page
        next({ name: 'Login' })
      } else {
        // Continue to the requested page
        next()
      }
    } else {
      // Allow access to 'Login' and 'Signup' pages
      next()
    }
  })
  

const app = createApp(App);
app.use(router);
app.mount('#app');
