import { createRouter, createWebHistory } from 'vue-router';
import Login from '../components/Login.vue';
import SignUp from '@/components/SignUp.vue';
import LibrarianDashboard from '@/components/LibrarianDashboard.vue';
import UserDashboard from '@/components/UserDashboard.vue';
import HelloWorld from '@/components/HelloWorld.vue';

const routes = [ 
    {path: '/login' , component: Login},
    {path: '/signup' , component: SignUp},
    {path: '/librarian-dashboard' , component: LibrarianDashboard},
    {path: '/user-dashboard' , component: UserDashboard},
    {path: '/hello-world' , component: HelloWorld},
];


const router = createRouter({
    history: createWebHistory(),
    routes,
    });

export default router;