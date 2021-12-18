import store from '@/store'
export default {
    focusCursor(id) {
        setTimeout(() => { document.getElementById(id).focus() }, 200)
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
}