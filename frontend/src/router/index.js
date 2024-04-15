import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import SignUp from '@/components/SignUp.vue';
import LibrarianDashboard from '@/components/LibrarianDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import HelloWorld from '@/components/HelloWorld.vue';
import SingleSection from '@/components/SingleSection.vue';
import RequestPage from '@/components/RequestPage.vue';
import MyBooks from '@/components/MyBooks.vue';
import BarChart from '@/components/MyStats.vue';
// import UserStats from '@/components/UserStats.vue';
// import BarChart from '@/components/BC.vue';
const routes = [ 
    {path: '/login' , component: Login, name: 'Login'},
    {path: '/signup' , component: SignUp,name: 'Signup'},
    {path: '/librarian-dashboard' , component: LibrarianDashboard},
    {path: '/user-dashboard' , component: UserDashboard},
    {path: '/hello-world' , component: HelloWorld},
    {path:"/section/:id", component: SingleSection},
    {path: '/requests' , component: RequestPage},
    {path: '/my-books' , component: MyBooks},
    {path: '/mystats' , component: BarChart},
    // if user is logged in, redirect to user dashboard, else redirect to login page
    {
        path: '/',
        redirect: function () {
          if (localStorage.getItem('user') && localStorage.getItem('role') === 'user'){
            return '/user-dashboard'; // Redirect to user dashboard if logged in
          } 
          else if (localStorage.getItem('user') && localStorage.getItem('role') === 'admin'){
            return '/librarian-dashboard'; // Redirect to librarian dashboard if logged in
          }
          else {
            return '/login'; // Redirect to login page if not logged in
          }
        }
      }
    
];


const router = createRouter({
    history: createWebHistory(),
    routes,
    });

export default router;

  