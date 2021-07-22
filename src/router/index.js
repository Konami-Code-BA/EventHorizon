import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import apiFunctions from '@/functions/apiFunctions.js'
import front from '@/views/front'
import loginRegister from '@/views/loginRegister'
import registerWithEmail from '@/views/registerWithEmail'
import loginWithEmail from '@/views/loginWithEmail'
import settings from '@/views/settings'
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
        redirect: { name: 'front' },
        meta: { userGroups: [] },
    }, {
        path: '/',
        redirect: { name: 'front' },
        meta: { userGroups: [] },
    }, {
        path: '/front',
        name: 'front',
        component: front,
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
        path: '/loginWithEmail',
        name: 'loginWithEmail',
        component: loginWithEmail,
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
        path: '/settings',
        name: 'settings',
        component: settings,
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
        if (store.user.groups[0] === 100) { // if never logged in, not even to visitor account, login
            console.log(process.env.PYTHON_ENV)
            await apiFunctions.login({})
            if (store.user.groups.includes(3)) {
                console.log('visitor')
            } else {
                console.log('user')
            }
        }
        if (to.meta.userGroups.length === 0) { // this path has no requirements, go ahead
            next()
            return
        } else { // this path does have requirements for group permission
            for (let i = 0; i < to.meta.userGroups.length; i++) {
                for (let j = 0; j < store.user.groups.length; j++) {
                    if (to.meta.userGroups[i] === store.user.groups[j]) { // permission granted, go ahead
                        next()
                        return
                    }
                }
            } // permission denied
            // if path coming from is login, register, or front page, don't change pages on failure
            if (['loginRegister', 'loginWithEmail', 'front', 'registerWithEmail'].includes(from.name)) {
                return
            } else { // any other page, when permission denied, get sent to front page
                next({ name: 'front' })
                return
            }
        }
    }
)

export default router