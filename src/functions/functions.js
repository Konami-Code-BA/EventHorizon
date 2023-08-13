import store from '@/store'
import api from '@/functions/apiFunctions.js'
export default {
    get currentPage() {
        return store.pages[store.pages.length - 1]
    },
    get previousPage() {
        return store.pages[store.pages.length - 2]
    },
    get currentUrl() {
        let result = window.origin + '/?page=' + this.currentPage.page
        let argKeys = Object.keys(this.currentPage.args)
        for (let i = 0; i < argKeys.length; i++) {
            result += '&' + argKeys[i] + '=' + this.currentPage.args[argKeys[i]]
        }
        return result
    },
    get isAuthenticatedUser() {
        let result = this.inGroups(['User', 'Admin']) && store.user.display_name !== ''
        return result
    },
    get isAdmin() {
        let result = this.inGroups(['Admin'])
        return result
    },
    get today() {
        return new Date()
    },
    get queryFromUrl() {
        let urlSearchParams = new URLSearchParams(window.location.search)
        return Object.fromEntries(urlSearchParams.entries())
    },
    inGroups(groupNames) {
        let result = false
        if (store.groups) {
            let groupIds = []
            for (let i = 0; i < groupNames.length; i++) {
                groupIds.push(store.groups.filter(group => {
                    if (group.name === groupNames[i]) {
                        return true
                    } else {
                        return false
                    }
                })[0].id)
            }
            result = groupIds.includes(store.user.groups[0])
        }
        return result
    },
    createUrl(pageDict) {
        let result = window.origin + '/?page=' + pageDict.page
        let argKeys = Object.keys(pageDict.args)
        for (let i = 0; i < argKeys.length; i++) {
            result += '&' + argKeys[i] + '=' + pageDict.args[argKeys[i]]
        }
        return result
    },
    areDictsEqual(dict1, dict2) {
        let dict1Keys = Object.keys(dict1)
        let dict2Keys = Object.keys(dict2)
        for (let i = 0; i < dict1Keys.length; i++) {
            if (dict2Keys.includes(dict1Keys[i])) {
                if (typeof dict2[dict1Keys[i]] === 'object') {
                    if (!this.areDictsEqual(dict2[dict1Keys[i]], dict1[dict1Keys[i]])) {
                        return false
                    }
                } else {
                    if (dict2[dict1Keys[i]] !== dict1[dict1Keys[i]]) {
                        return false
                    }
                }
            } else {
                return false
            }
        }
        return true
    },
    goToPage(pageDict) {
        if (store.pages.length === 0 || !this.areDictsEqual(store.pages[store.pages.length - 1], pageDict)) {
            store.pages.push(pageDict)
            if (this.currentPage.page === 'home' && window.initMap) {
                window.initMap()
            }
        }
        if (!['loginRegister', 'welcome'].includes(pageDict.page)) {
            store.lastNonLoginRegisterPage = pageDict
        }
    },
    goBack() {
        if (store.pages.length === 1) {
            window.history.go(-2)
        } else if (!store.modalBack) {
            store.pages.pop() // remove the current page
            if (this.currentPage.page === 'home' && window.initMap) {
                window.initMap()
            }
        }
    },
    focusCursor(documentt, id) {
        setTimeout(() => { documentt.getElementById(id).focus() }, 200)
    },
    isGuestStatus(event, guestStatus) {
        if (Array.isArray(event[guestStatus])) {
            return event[guestStatus].includes(store.user.id)
        } else {
            return false
        }
    },
    async getImageDataPeopleMyAttendingStatus(event) {
        // only get image_data if (there is an image to get AND
        // (there are store events not got yet OR (there are store events and the image_data hasnt been saved yet)))
        let ind = store.events.all.find(ev => { ev.id === event.id })
        if (event.images.length > 0 && (store.events.all.length === 0 || (store.events.all.length > 0 && !('image_data' in store.events.all[ind])))) {
            let result = await api.getEventImage(event.images[0], event.id)
            if (result != 'fail') {
                event.image_data = `https://eventhorizon-us-east-1.s3.amazonaws.com/${result}`
            }
            // otherwise just get the image from the store, if
            // there is an image to get but events have been stored and the image is saved there too
        } else if (event.images.length > 0 && store.events.all.length > 0 && 'image_data' in store.events.all[ind]) {
            event.image_data = store.events.all[ind].image_data
        }

        let eventUserInfo = await this.getEventUserInfoCheckPeopleList(event.id)
        event.people = eventUserInfo.people
        event.myAttendingStatus = eventUserInfo.myAttendingStatus
        return event
    },
    async getEvents() {
        let events = await api.getAllEvents()
        events = this.sortEventsByDate(events)
        for (let i = 0; i < events.length; i++) { // get image data, people, and myAttendingStatus
            events[i] = await this.getImageDataPeopleMyAttendingStatus(events[i])
        }
        store.events.all = events
        store.events.mine = this.filterEventsByMyStatus()
        store.events.display = store.events.all
    },
    async updateEvent(event) {
        event = await this.getImageDataPeopleMyAttendingStatus(event) // update event
        let ind = store.events.all.find(ev => { ev.id === event.id })
        if (ind) { // this event exists, simply update it
            store.events.all[ind] = event
        } else { // this event doesn't exist, add it
            store.events.all.push(event)
        }
        store.events.mine = this.filterEventsByMyStatus()
        store.events.display = store.events.all
        store.events.selected = event
        return event
    },
    async asyncFilter(arr, callback) { // how to use: await this.asyncFilter(events, async event => {})
        const fail = Symbol()
        return (await Promise.all(arr.map(async item => (await callback(item)) ? item : fail))).filter(i => i !== fail)
    },
    filterEventsByMyStatus() {
        let filteredEvents = []
        for (let i = 0; i < store.events.all.length; i++) {
            if (
                store.events.all[i].myAttendingStatus['hosts'] ||
                store.events.all[i].myAttendingStatus['invited'] ||
                store.events.all[i].myAttendingStatus['attending'] ||
                store.events.all[i].myAttendingStatus['maybe'] ||
                store.events.all[i].myAttendingStatus['wait_list'] ||
                store.events.all[i].myAttendingStatus['invite_request']
            ) {
                filteredEvents.push(store.events.all[i])
            }
        }
        return filteredEvents
    },
    sortEventsByDate(events) {
        let sorted_events = []
        if (events.length > 0) {
            sorted_events = events.sort((a, b) => {
                let a_date = new Date(a.date_time)
                let b_date = new Date(b.date_time)
                if (a_date.getTime() > b_date.getTime()) {
                    return 1
                } else if (a_date.getTime() < b_date.getTime()) {
                    return -1
                } else {
                    return 0
                }
            })
        }
        return sorted_events
    },
    filterEvents(events, search, criteria, strictlyEqual = false) {
        let filtered_events = []
        if (events.length > 0) {
            filtered_events = events.filter(event => {
                for (let i = 0; i < criteria.length; i++) {
                    if (!strictlyEqual) {
                        if (String(event[criteria[i]]).toUpperCase().includes(String(search).toUpperCase())) {
                            return true
                        }
                    } else {
                        if (String(event[criteria[i]]).toUpperCase() === String(search).toUpperCase()) {
                            return true
                        }
                    }
                }
                return false
            })
        }
        return filtered_events
    },
    isoStringDateToDateObject(date) {
        let b = date.split(/\D+/)
        return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
    },
    getEventWithClosestFutureDate(events, dateTime) {
        let event = []
        events = this.sortEventsByDate(events)
        if (events.length > 0) {
            event = events.filter(event => {
                let eventDate = this.isoStringDateToDateObject(event['date_time'])
                return eventDate >= dateTime
            })
            return event[0]
        }
        return event
    },
    hasIllegalSymbols(value) {
        let symbols = '`~!#$%^&*()=[{]}\\|;:\'",<>/?'
        for (let i = 0; i < symbols.length; i++) {
            if (value.includes(symbols[i])) {
                return true
            }
        }
        return false
    },
    createEncodedURL() {
        let url = 'https%3A%2F%2Fwww.eventhorizon.vip'
        if (process.env.PYTHON_ENV == 'development') {
            url = 'http%3A%2F%2Flocalhost%3A8080'
        } else if (process.env.PYTHON_ENV == '"test"') {
            url = 'https%3A%2F%2Fevent-horizon-test.herokuapp.com'
        }
        return url
    },
    createUriForReturnFromLogin(currentPageDict, returnToPageDict, encode) {
        let e = {
            '/': '%2F',
            '?': '%3F',
            '=': '%3D',
            '&': '%26',
        }
        let uri = null
        let argKeys = Object.keys(returnToPageDict.args)
        if (encode) {
            uri = `${e['/']}${e['?']}page${e['=']}${currentPageDict.page}${e['&']}next`
            uri += `${e['=']}${returnToPageDict.page}${e['&']}lang${e['=']}${store.user.language}`
        } else {
            uri = `/?page=${currentPageDict.page}&next=${returnToPageDict.page}`
        }
        if (argKeys.length > 0) {
            for (let i = 0; i < argKeys.length; i++) {
                if ([
                        'code',
                        'friendship_status_changed',
                        'state',
                        'liffClientId',
                        'liffRedirectUri',
                    ].includes(argKeys[i])) {
                    continue
                }
                if (encode) {
                    uri += `${e['&']}${argKeys[i]}${e['=']}${returnToPageDict.args[argKeys[i]]}`
                } else {
                    uri += `&${argKeys[i]}=${returnToPageDict.args[argKeys[i]]}`
                }
            }
        }
        return uri
    },
    createNextPageFromCurrentPage() {
        let nextArgKeys = Object.keys(this.currentPage.args)
        let nextPage = null
        if (this.currentPage.args.next) {
            nextPage = this.currentPage.args.next
        } else {
            nextPage = 'home'
        }
        let nextArgs = {}
        if (nextArgKeys.length > 0) {
            for (let i = 0; i < nextArgKeys.length; i++) {
                if (['next', 'code', 'friendship_status_changed', 'state'].includes(nextArgKeys[i])) {
                    continue
                } else {
                    nextArgs[nextArgKeys[i]] = this.currentPage.args[nextArgKeys[i]]
                }
            }
        }
        return { page: nextPage, args: nextArgs }
    },
    createUrlForLoginRegister(email) {
        let nextArgKeys = Object.keys(store.lastNonLoginRegisterPage.args)
        console.log('HERE I AM', store.lastNonLoginRegisterPage.page)
        let returnUrl = `${window.origin}/?page=welcome&next=${store.lastNonLoginRegisterPage.page}`
        returnUrl += `&email=${encodeURIComponent(email)}`
        if (nextArgKeys.length > 0) {
            for (let i = 0; i < nextArgKeys.length; i++) {
                returnUrl += `&${nextArgKeys[i]}=${store.lastNonLoginRegisterPage.args[nextArgKeys[i]]}`
            }
        }
        return returnUrl
    },
    removeArgFromUrl(argName) {
        let query = window.location.search
        query = query.split('&')
        query = query.filter(item => { return !item.includes(argName) && !item.includes('?') })
        let params = Object.assign({}, ...query.map(item => ({
            [item.split('=')[0]]: item.split('=')[1]
        })))
        store.pages[store.pages.length - 1].args = params
        window.history.pushState({ path: this.currentUrl }, '', this.currentUrl)
    },
    shakeFunction(thiss) {
        if (Array.isArray(thiss)) {
            for (let i = 0; i < thiss.length; i++) {
                thiss[i].shakeIt = true
                setTimeout(() => { thiss[i].shakeIt = false; }, 1000)
            }
        } else {
            thiss.shakeIt = true
            setTimeout(() => { thiss.shakeIt = false; }, 1000)
        }
    },
    checkPeopleList(people, guestStatus) {
        if (this.isAuthenticatedUser) {
            let me = {
                id: store.user.id,
                display_name: store.user.display_name,
                limited_user: true,
                plus_one: false,
            }
            for (let i = 0; i < people[guestStatus].length; i++) {
                if (JSON.stringify(people[guestStatus][i]) === JSON.stringify(me)) {
                    return true
                }
            }
        }
        return false
    },
    async getEventUserInfoCheckPeopleList(eventId) {
        let myAttendingStatus = {
            'hosts': false,
            'invited': false,
            'attending': false,
            'maybe': false,
            'wait_list': false,
            'invite_request': false,
        }
        let people = {
            'hosts': [],
            'invited': [],
            'attending': [],
            'maybe': [],
            'wait_list': [],
            'invite_request': [],
            'uninvited_followers': [],
        }
        let eventUserInfo = await api.getEventUserInfo(eventId)
        people['hosts'] = eventUserInfo['hosts']
        people['invited'] = eventUserInfo['invited']
        people['maybe'] = eventUserInfo['maybe']
        people['attending'] = eventUserInfo['attending']
        people['wait_list'] = eventUserInfo['wait_list']
        people['invite_request'] = eventUserInfo['invite_request']
        people['uninvited_followers'] = await api.getUserLimitedInfo()
        people['uninvited_followers'] = people['uninvited_followers'].filter(person => {
            return !(people['hosts'].concat(
                people['invited'], people['maybe'], people['attending'], people['wait_list']
            ).map(
                x => { return x.id }
            ).includes(person.id)) && this.isAuthenticatedUser
        })
        if (this.isAuthenticatedUser) {
            myAttendingStatus['hosts'] = this.checkPeopleList(people, 'hosts')
            myAttendingStatus['invited'] = this.checkPeopleList(people, 'invited')
            myAttendingStatus['attending'] = this.checkPeopleList(people, 'attending')
            myAttendingStatus['maybe'] = this.checkPeopleList(people, 'maybe')
            myAttendingStatus['wait_list'] = this.checkPeopleList(people, 'wait_list')
            myAttendingStatus['invite_request'] = this.checkPeopleList(people, 'invite_request')
        }
        return { people: people, myAttendingStatus: myAttendingStatus }
    }
}