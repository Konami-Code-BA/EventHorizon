import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import apiFunctions from '@/functions/apiFunctions.js'
import frontPage from '@/views/frontPage'
import registration from '@/views/registration'
import login from '@/views/login'
import pageTwo from '@/views/pageTwo'
import accountSettings from '@/views/accountSettings'
import home from '@/views/home'

Vue.use(Router)

//export default new Router({
const router = new Router({
    mode: 'history',
    //beforeEach: (to, from, next) => {},
    routes: [{
        //    path: '/',
        //    redirect: { name: 'frontPage' },
        //}, {
        path: '/',
        name: 'frontPage',
        component: frontPage,
        meta: { userGroups: [] },
    }, {
        path: '/registration',
        name: 'registration',
        component: registration,
        meta: { userGroups: [] },
    }, {
        path: '/login',
        name: 'login',
        component: login,
        meta: { userGroups: [] },
    }, {
        path: '/pageTwo',
        name: 'pageTwo',
        component: pageTwo,
        meta: { userGroups: [1] },
    }, {
        path: '/accountSettings',
        name: 'accountSettings',
        component: accountSettings,
        meta: { userGroups: [1, 2] },
    }, {
        path: '/home',
        name: 'home',
        component: home,
        meta: { userGroups: [1, 2] },
    }, ]
})

router.beforeEach(
    async(to, from, next) => {
        await apiFunctions.authenticateFromSession()
        console.log('routed', from.name, to.name)
            //if (from.name == to.name) {
            //    console.log(from.name, to.name)
            //    return
            //} else 
        if (to.meta.userGroups.length === 0) {
            next()
            return
        } else {
            for (let i = 0; i < to.meta.userGroups.length; i++) {
                for (let j = 0; j < store.user.groups.length; j++) {
                    if (to.meta.userGroups[i] === store.user.groups[j]) { // permission granted
                        next()
                        return
                    }
                }
            }
            // permission denied
            if (['login', 'frontPage', 'registration'].includes(from.name)) {
                return
            } else {
                next({ name: 'frontPage' })
                return
            }
        }

        //if (to.meta.requiresAuth) {
        //    if (!store.user) {
        //        console.log("MAKE IT?", store.user)
        //        next({
        //            name: 'login'
        //        })
        //    } else {
        //        next()
        //    }
        //} else {
        //    next()
        //}
    }
)

export default router