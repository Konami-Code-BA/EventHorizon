import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import apiFunctions from '@/functions/apiFunctions.js'
import events from '@/views/events'
import profile from '@/views/profile'
import people from '@/views/people'
import search from '@/views/search'
import addEvent from '@/views/addEvent'
import settings from '@/views/settings'
import loginRegister from '@/views/loginRegister'
import registerWithEmail from '@/views/registerWithEmail'
import loginWithEmail from '@/views/loginWithEmail'
import experiment1 from '@/views/experiment1'
import experiment2 from '@/views/experiment2'

Vue.use(Router)

//1=Admin, 2=User, 3=Temp Visitor, 5=Temp Line Friend
const router = new Router({
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
        meta: { userGroups: [3, 5, ] },
    }, {
        path: '/registerWithEmail',
        name: 'registerWithEmail',
        component: registerWithEmail,
        meta: { userGroups: [3, 5, ] },
    }, {
        path: '/loginWithEmail',
        name: 'loginWithEmail',
        component: loginWithEmail,
        meta: { userGroups: [3, 5, ] },
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

router.beforeEach(
    async(to, from, next) => {
        if (store.user.groups[0] === 100) { // if never logged in, not even to visitor account, login
            console.log(process.env.PYTHON_ENV)
            await apiFunctions.login({})
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
            // if path coming from is login, register, or events page, don't change pages on failure
            if (['loginRegister', 'loginWithEmail', 'event', 'registerWithEmail'].includes(from.name)) {
                return
            } else { // any other page, when permission denied, get sent to events page
                next({ name: 'loginRegister' })
                return
            }
        }
    }
)

export default router