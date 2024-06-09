import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'

const Home = () => import('./views/home.vue')
const About = () => import('./views/about.vue')
const Dashboard = () => import('./views/dashboard.vue')
const Start = () => import('./views/start.vue')
const Index = () => import('./views/index.vue')
const Test = () => import('./views/test.vue')
const Repos = () => import('./views/repos/index.vue')
const ReposSetup = () => import('./views/repos/setup.vue')
const ReposHistory = () => import('./views/repos/history.vue')

const Pages = () => import('./views/pages/index.vue')
const PagesSetup = () => import('./views/pages/setup.vue')
const PagesHistory = () => import('./views/pages/history.vue')

const PassportLogin = () => import('./views/passport/login.vue')
const PassportRegister = () => import('./views/passport/register.vue')
const PassportForget = () => import('./views/passport/forget.vue')

const menuRoutes: Array<RouteRecordRaw> = [
    {
        path: '/',
        meta: { title: '首页' },
        component: Home,
        redirect: '/index',
        children: [{
            path: 'about',
            name: 'about',
            meta: { title: '关于 VulnTrac' },
            component: About
        }, {
            path: 'dashboard',
            name: 'dashboard',
            meta: { title: '个人中心' },
            component: Dashboard
        }, {
            path: 'start',
            name: 'start',
            meta: { title: '检测中心' },
            component: Start
        }, {
            path: '/repos',
            name: 'repos',
            meta: { title: '仓库管理' },
            component: Repos,
            redirect: '/repos/setup',
            children: [{
                path: '/repos/setup',
                name: 'repos-setup',
                meta: { title: '监测设置' },
                component: ReposSetup
            }, {
                path: '/repos/history',
                name: 'repos-history',
                meta: { title: '监测历史' },
                component: ReposHistory
            }]
        }, {
            path: '/pages',
            name: 'pages',
            meta: { title: '常用页面' },
            component: Pages,
            redirect: '/pages/setup',
            children: [ {
                path: '/pages/setup',
                name: 'pages-setup',
                meta: {title: '检测设置'},
                component: PagesSetup
            }, {
                path: '/pages/history',
                name: 'pages-history',
                meta: {title: '检测记录'},
                component: PagesHistory
            }]
        }
        ]
    },
    {
        path: '/index',
        name: 'VulnTrac',
        meta: { title: 'VulnTrac' },
        component: Index
    },
    {
        path: '/test',
        name: 'introduce',
        meta: {title: 'introduce'},
        component: Test
    }
]

const passportRoutes: Array<RouteRecordRaw> = [
    {
        path: '/login',
        name: 'single-login',
        meta: { title: '登录' },
        component: PassportLogin
    },
    {
        path: '/register',
        name: 'single-register',
        meta: { title: '注册' },
        component: PassportRegister
    },
    {
        path: '/forget',
        name: 'single-forget',
        meta: { title: '忘记密码' },
        component: PassportForget
    }
]

const routes: Array<RouteRecordRaw> = [
    ...menuRoutes,
    ...passportRoutes
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior: () => {
        return { top: 1 }
    }
})
export default router