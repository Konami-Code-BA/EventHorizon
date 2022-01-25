import store from '@/store.js'
import f from '@/functions/functions.js'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
    //let csrftoken = JSON.parse('{"' + document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "') + '"}')['XSRF-TOKEN']
    //axios.defaults.headers.common['X-CSRFToken'] = csrftoken
import axios from 'axios'
export default {
    get baseUrl() { return process.env.PYTHON_ENV == 'development' ? 'http://127.0.0.1:8000' : '' },
    axiosCall: {
        post: axios.post,
        patch: axios.patch,
        get: axios.get,
    },
    // API /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async userApi(method, pk = null, data = null) {
        let uri = '/api/user/'
        if (pk) {
            uri += pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + uri, data)
            .then(response => {
                if (data.command === 'logout') {
                    console.log(`success - userApi ${data.command}`)
                    store.user = store.defaultUser
                    return store.user
                } else if (data.command === 'login') {
                    console.log(`success - userApi ${data.command}`)
                    store.user = response.data[0]
                    return response.data
                } else if ((typeof response.data) === 'number') { // when getting a count of users
                    console.log(`success - userApi ${data.command}`)
                    return response.data
                } else if (response.data.length === 0) { // when gettin an empty array of users
                    console.log(`success - userApi ${data.command}`)
                    return response.data
                } else if ('limited_user' in response.data[0]) { // when getting an array of users
                    console.log(`success - userApi ${data.command}`)
                    return response.data
                } else if (!('error' in response.data[0])) {
                    console.log(`success - userApi ${data.command}`)
                    return response.data
                } else {
                    console.log(`*INTERNAL ERROR* - userApi ${data.command}:`, response.data[0]['error'])
                    return response.data[0]
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - userApi ${data.command}:`, error)
                return error
            })
    },
    async lineApi(method, uri, data) {
        return await this.axiosCall[method](this.baseUrl + uri, data)
            .then(response => {
                if (!('error' in response.data)) {
                    console.log(`success - lineApi ${data.command}`)
                    return response.data
                } else {
                    console.log(`*INTERNAL ERROR* - lineApi ${data.command}:`, response.data['error'])
                    return response.data['error']
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - lineApi ${data.command}:`, error)
                return error
            })
    },
    async secretsApi(toGet) {
        return await this.axiosCall['get'](this.baseUrl + '/api/secrets/' + toGet + '/')
            .then(response => {
                console.log(`success - secretsApi ${toGet}`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - secretsApi ${toGet}:`, error)
                return error
            })
    },
    async eventsApi(method, pk = null, data = null) {
        let id = ''
        if (pk) {
            id = pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + '/api/events/' + id, data)
            .then(response => {
                console.log(`success - eventsApi`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - eventsApi:`, error)
                return error
            })
    },
    async imagesApi(method, pk = null, data = null) {
        let id = ''
        if (pk) {
            id = pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + '/api/images/' + id, data, {
                headers: { "content-type": "multipart/form-data" }
            })
            .then(response => {
                console.log(`success - saveImageFunction`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - saveImageFunction:`, error)
                return error
            })
    },
    async plusOneApi(method, pk = null, data = null) {
        let id = ''
        if (pk) {
            id = pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + '/api/plusone/' + id, data)
            .then(response => {
                if (!('error' in response.data[0])) {
                    console.log(`success - plusOneApi ${data.command}`)
                    return response.data
                } else {
                    console.log(`*INTERNAL ERROR* - plusOneApi ${data.command}:`, response.data[0]['error'])
                    return response.data
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - plusOneApi:`, error)
                return error
            })
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    //async getUserLimitedInfo(userIds) { // userIds is an array
    //    return await this.userApi('post', null, {
    //        command: 'get_user_limited_info',
    //        ids: userIds,
    //        pks: userIds,
    //    })
    //},
    async getEventUserInfo(eventId, guestType) {
        return await this.userApi('post', null, {
            command: 'get_event_user_info',
            event_id: eventId,
            guest_type: guestType,
        })
    },
    async registerWithEmail(email, password, displayName) {
        return await this.userApi('post', null, {
            command: 'register_with_email',
            display_name: displayName,
            email: email,
            password: password,
        })
    },
    async addAnEmail(email, password) {
        return await this.userApi('patch', store.user.id, {
            command: 'register_email',
            email: email,
            password: password,
        })
    },
    async messageUser(eventId, user_id, message) {
        return await this.userApi('patch', user_id, {
            command: 'message_user',
            event_id: eventId,
            message: message,
        })
    },
    async messageUsers(eventId, userIds, message) {
        return await this.userApi('post', null, {
            command: 'message_users',
            event_id: eventId,
            user_ids: userIds,
            message: message,
        })
    },
    async forgotPassword(email, returnLink) {
        return await this.userApi('post', null, {
            command: 'forgot_password',
            email: email,
            return_link: returnLink,
        })
    },
    async changePassword(email, newPassword, code = null, currentPassword = null) {
        let data = {
            command: 'change_password',
            email: email,
            new_password: newPassword,
        }
        if (code) {
            data.code = code
        } else if (currentPassword) {
            data.current_password = currentPassword
        }
        return await this.userApi('post', null, data)
    },
    async login(data) {
        data['command'] = 'login'
        return await this.userApi('post', null, data)
    },
    async lineNewDevice(code, path) {
        return await this.userApi('post', null, {
            command: 'line_new_device',
            code: code,
            path: path,
        })
    },
    async logout() {
        return await this.userApi('post', null, {
            command: 'logout',
        })
    },
    async sendEmail() {
        return await this.userApi('post', null, {
            command: 'send_email',
        })
    },
    async updateUserLanguage() {
        return await this.userApi('patch', store.user.id, {
            command: 'update_user_language',
            language: store.user.language,
        })
    },
    async updateUserDoGetEmails() {
        return await this.userApi('patch', store.user.id, {
            command: 'update_user_do_get_emails',
            do_get_emails: store.user.do_get_emails,
        })
    },
    async updateUserDoGetLines() {
        return await this.userApi('patch', store.user.id, {
            command: 'update_user_do_get_lines',
            do_get_lines: store.user.do_get_lines,
        })
    },
    //async updateUserAlerts(name) {
    //    return await this.userApi('patch', store.user.id, {
    //        command: 'update_user_alerts',
    //        name: name,
    //    })
    //},
    // LINE ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async sendWebhook(data) {
        return await this.lineApi('post', '/webhook/', data)
    },
    async lineConsumption() {
        return await this.lineApi('post', '/api/line/', {
            command: 'consumption',
        })
    },
    async linePush(data) {
        return await this.lineApi('post', '/api/line/', {
            command: 'push',
            data: data,
        })
    },
    async lineBroadcast() {
        return await this.lineApi('post', '/api/line/', {
            command: 'broadcast',
            message: 'sup this is a broadcast message',
        })
    },
    // EVENTS //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async getAllEvents() {
        let result = await this.eventsApi('get', null, null)
        return result
    },
    async getEvent(eventId) {
        let result = await this.eventsApi('get', eventId, null)
        return result[0]
    },
    async createEvent(data) {
        data.command = 'add_event'
        let result = await this.eventsApi('post', null, data)
        return result[0]
    },
    async getMyEvents() {
        let result = await this.eventsApi('post', null, { command: 'my_events' })
        return result
    },
    async changeGuestStatus(eventId, status, userId = null) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) {
            return await this.eventsApi('patch', eventId, {
                command: 'update_guest_status',
                status: status,
                user_id: userId,
            })
        }
    },
    async setPlusOne(eventId, plusOneName) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) {
            return await this.plusOneApi('post', null, {
                command: 'set_plus_one',
                plus_one_name: plusOneName,
                event_id: eventId,
            })
        }
    },
    async deletePlusOne(eventId) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) {
            return await this.plusOneApi('post', null, {
                command: 'delete_plus_one',
                event_id: eventId,
            })
        }
    },
    //async getEventWithClosestFutureDate(date_time) {
    //    let data = {
    //        'date_time': date_time,
    //        'command': 'closest_future_date',
    //    }
    //    let result = await this.eventsApi('post', null, data)
    //    return result[0]
    //},
    // IMAGES //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async saveImage(formData) {
        formData.append('command', 'create')
        let result = await this.imagesApi('post', null, formData)
        return result[0]
    },
    async getEventImage(pk, eventId) {
        let formData = new FormData()
        formData.append('event_pk', eventId)
        formData.append('command', 'get')
        let result = await this.imagesApi('patch', pk, formData)
        return result[0]
    },
    async getImage(keys) {
        let formData = new FormData()
        formData.append('keys', keys)
        formData.append('command', 'get')
        let result = await this.imagesApi('post', null, formData)
        return result
    },
}