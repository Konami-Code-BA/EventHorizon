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
    }
)

export default router