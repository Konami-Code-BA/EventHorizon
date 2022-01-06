import Vue from 'vue'
import Router from 'vue-router'
import temp from '@/views/temp'
import front from '@/views/front'

Vue.use(Router)

//1=Admin, 2=User, 3=Temp Visitor, 5=Temp Line Friend
const router = new Router({
    data() {
        return {}
    },
    mode: 'history',
    routes: [{
        path: '',
        redirect: to => {
            const { hash, params, query } = to
            return { name: 'temp', params: query }
        },
        meta: { userGroups: [] },
    }, {
        path: '/temp',
        name: 'temp',
        component: temp,
        meta: { userGroups: [] },
    }, {
        path: '/front',
        name: 'front',
        component: front,
        meta: { userGroups: [] },
    }]
})

router.beforeEach(
    async(to, from, next) => {
        if (['', '/', '/temp'].includes(from.path)) {
            next()
        } else {
            next(false)
        }

        //if (to.meta.userGroups.length === 0) { // this path has no requirements, go ahead
        //    store.path = to.path
        //    next()
        //    return
        //} else { // this path does have requirements for group permission
        //    for (let i = 0; i < to.meta.userGroups.length; i++) {
        //        for (let j = 0; j < store.user.groups.length; j++) {
        //            if (to.meta.userGroups[i] === store.user.groups[j]) { // permission granted, go ahead
        //                store.path = to.path
        //                next()
        //                return
        //            }
        //        }
        //    } // permission denied
        //    // if path coming from is loginRegister or front page, don't change pages on failure
        //    if (['loginRegister', 'event'].includes(from.name)) {
        //        return
        //    } else { // any other page, when permission denied, get sent to loginRegister
        //        store.path = '/loginRegister'
        //        next({ name: 'loginRegister' })
        //        return
        //    }
        //}
    }
)

export default router