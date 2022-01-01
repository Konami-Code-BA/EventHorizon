import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import api from '@/functions/apiFunctions.js'
import events from '@/views/events'
import profile from '@/views/profile'
import people from '@/views/people'
import search from '@/views/search'
import addEvent from '@/views/addEvent'
import settings from '@/views/settings'
import loginRegister from '@/views/loginRegister'
import registerWithEmail from '@/views/registerWithEmail'
import experiment1 from '@/views/experiment1'
import experiment2 from '@/views/experiment2'

Vue.use(Router)

//1=Admin, 2=User, 3=Temp Visitor, 5=Temp Line Friend
const router = new Router({
    data() {
        return {
            allowBack: true,
        }
    },
    mode: 'history',
    routes: [{
        path: '',
        redirect: { name: 'events' },
        meta: { userGroups: [] },
    }, {
        path: '/',
        redirect: { name: 'events' },
        meta: { userGroups: [] },
    }, {
        path: '/events',
        name: 'events',
        component: events,
        meta: { userGroups: [] },
    }, {
        path: '/events/:id',
        name: 'event',
        component: events,
        meta: { userGroups: [] },
    }, {
        path: '/profile',
        name: 'profile',
        component: profile,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/people',
        name: 'people',
        component: people,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/search',
        name: 'search',
        component: search,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/addEvent',
        name: 'addEvent',
        component: addEvent,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/settings',
        name: 'settings',
        component: settings,
        meta: { userGroups: [1, 2, ] },
    }, {
        path: '/loginRegister',
        name: 'loginRegister',
        component: loginRegister,
        meta: { userGroups: [1, 3, 5, ] },
    }, {
        path: '/registerWithEmail',
        name: 'registerWithEmail',
        component: registerWithEmail,
        meta: { userGroups: [1, 3, 5, ] },
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
    }, ]
})

window.popStateDetected = false
window.addEventListener('popstate', () => {
    window.popStateDetected = true
})

router.beforeEach(
    async(to, from, next) => {
        let isBackButton = window.popStateDetected
        window.popStateDetected = false
        if (isBackButton && !router.allowBack) {
            next(false)
            router.allowBack = true
            return
        } else if (isBackButton) {
            next()
            router.allowBack = true
            return
        }
        if (store.user.groups[0] === 100) { // if never logged in, not even to visitor account, login
            console.log(process.env.PYTHON_ENV)
            await api.login({})
            if (store.user.groups.includes(3)) {
                console.log('visitor')
            } else {
                console.log('existing user')
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
            // if path coming from is loginRegister or events page, don't change pages on failure
            if (['loginRegister', 'event'].includes(from.name)) {
                return
            } else { // any other page, when permission denied, get sent to loginRegister
                next({ name: 'loginRegister' })
                return
            }
        }
    }
)

export default router