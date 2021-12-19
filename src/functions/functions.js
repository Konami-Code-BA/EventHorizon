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
        let sorted_events = events.sort((a, b) => {
            if (Date(a.date_time) > Date(b.date_time)) {
                return 1
            } else if (Date(a.date_time) < Date(b.date_time)) {
                return -1
            } else {
                return 0
            }
        })
        return sorted_events
    },
}