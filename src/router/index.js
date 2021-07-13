import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import apiFunctions from '@/functions/apiFunctions.js'
import frontPage from '@/views/frontPage'
import loginRegister from '@/views/loginRegister'
import registerWithEmail from '@/views/registerWithEmail'
import loginByEmail from '@/views/loginByEmail'
import accountSettings from '@/views/accountSettings'
import home from '@/views/home'
import experiment1 from '@/views/experiment1'
import experiment2 from '@/views/experiment2'

Vue.use(Router)

//export default new Router({
const router = new Router({
    mode: 'history',
    //beforeEach: (to, from, next) => {},
    routes: [{
        path: '',
        redirect: { name: 'frontPage' },
        meta: { userGroups: [] },
    }, {
        path: '/',
        redirect: { name: 'frontPage' },
        meta: { userGroups: [] },
    }, {
        path: '/frontPage',
        name: 'frontPage',
        component: frontPage,
        meta: { userGroups: [] },
    }, {
        path: '/loginRegister',
        name: 'loginRegister',
        component: loginRegister,
        meta: { userGroups: [1, 3, 5, ] }, // [1, 3, 5, ]
    }, {
        path: '/registerWithEmail',
        name: 'registerWithEmail',
        component: registerWithEmail,
        meta: { userGroups: [1, 3, 5, ] },
    }, {
        path: '/loginByEmail',
        name: 'loginByEmail',
        component: loginByEmail,
        meta: { userGroups: [1, 3, 5, ] }, // [1, 3, 5, ]
    }, {
        path: '/experiment1',
        name: 'experiment1',
        component: experiment1,
        meta: { userGroups: [1, ] },
    }, {
        path: '/experiment2',
        name: 'experiment2',
        component: experiment2,
        meta: { userGroups: [1, ] },
    }, {
        path: '/accountSettings',
        name: 'accountSettings',
        component: accountSettings,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/home',
        name: 'home',
        component: home,
        meta: { userGroups: [1, 2, ] },
    }, ]
})

router.beforeEach(
    async(to, from, next) => {
        await apiFunctions.login({})
        console.log('IN FUCKING INDEX', store.user)
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
            if (['loginRegister', 'loginByEmail', 'frontPage', 'registerWithEmail'].includes(from.name)) {
                return
            } else {
                next({ name: 'frontPage' })
                return
            }
        }
    }
)

export default router