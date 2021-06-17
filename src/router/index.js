import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import frontPage from '@/components/frontPage'
import login from '@/components/login'
import page2 from '@/components/page2'

Vue.use(Router)

//export default new Router({
const router = new Router({
    mode: 'history',
    //beforeEach: (to, from, next) => {},
    routes: [{
        path: '/',
        name: 'frontPage',
        component: frontPage,
        meta: { userGroups: [] },
    }, {
        path: '/login',
        name: 'login',
        component: login,
        meta: { userGroups: [] },
    }, {
        path: '/page2/',
        name: 'page2',
        component: page2,
        meta: { userGroups: [1] },
        //beforeEnter: ifAuthenticated
    }]
})

router.beforeEach((to, from, next) => {
    if (to.meta.userGroups.length === 0) {
        next()
        return
    } else {
        for (let i = 0; i < to.meta.userGroups.length; i++) {
            for (let j = 0; j < store.groups.length; i++) {
                if (to.meta.userGroups[i] === store.groups[j]) { // permission granted
                    next()
                    return
                }
            }
        }
        next({ // permission denied
            name: 'login'
        })
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
})

export default router