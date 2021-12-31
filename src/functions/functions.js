import store from '@/store'
export default {
    focusCursor(documentt, id) {
        setTimeout(() => { documentt.getElementById(id).focus() }, 200)
    },
    setBackButtonToCloseModal(thiss, windoww, closeFunc) {
        thiss.$router.allowBack = false
        windoww.addEventListener('popstate', () => {
            closeFunc()
        })
    },
    freeUpBackButton(thiss) {
        thiss.$router.allowBack = true
    },
    get isAuthenticatedUser() {
        return [1, 2].includes(store.user.groups[0])
    },
    get isAdmin() {
        return [1].includes(store.user.groups[0])
    },
    isInvitedGuest(event) {
        if (Array.isArray(event.invited)) {
            return event.invited.includes(store.user.id)
        } else {
            return false
        }
    },
    isHost(event) {
        if (Array.isArray(event.hosts)) {
            return event.hosts.includes(store.user.id)
        } else {
            return false
        }
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
    filterEvents(events, search, criteria) {
        let filtered_events = []
        if (events.length > 0) {
            filtered_events = events.filter(event => {
                for (let i = 0; i < criteria.length; i++) {
                    console.log('this the stuff', event[criteria[i]], search)
                    if (String(event[criteria[i]]).includes(String(search))) {
                        return true
                    }
                }
                return false
            })
        }
        return filtered_events
    },
}