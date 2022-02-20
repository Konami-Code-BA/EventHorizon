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
                console.log('HERE', response.data)
                if (data.command === 'logout') {
                    console.log(`success - userApi ${data.command}`)
                    store.user = store.defaultUser
                    return store.user
                } else if ([
                        'login', 'register_with_email', 'register_email', 'update_user_do_get_lines',
                        'update_user_do_get_emails', 'update_user_language', 'line_new_device',
                        'change_password', 'update_user_display_name',
                    ].includes(data.command) && !('error' in response.data[0])) {
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
                console.log(`success - eventsApi ${data.command}`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - eventsApi ${data.command}:`, error)
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
                console.log(`success - imagesApi ${data.get('command')}`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - imagesApi: ${data.get('command')}`, error)
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
    async groupApi(method, pk = null, data = null) {
        let id = ''
        if (pk) {
            id = pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + '/api/group/' + id, data)
            .then(response => {
                if (!('error' in response.data[0])) {
                    console.log(`success - groupApi ${data.command}`)
                    return response.data
                } else {
                    console.log(`*INTERNAL ERROR* - groupApi ${data.command}:`, response.data[0]['error'])
                    return response.data
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - groupApi:`, error)
                return error
            })
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    async getUserLimitedInfo(userIds = null) { // userIds is an array. normally it would be my followers. but for now it will be null and we will get everyone
        return await this.userApi('post', null, {
            command: 'get_user_limited_info',
            ids: userIds,
        })
    },
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
    async messageUser(eventId, userId, message) {
        return await this.userApi('post', null, {
            command: 'message_user',
            event_id: eventId,
            user_id: userId,
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
    async feedback(message) {
        return await this.userApi('post', null, {
            command: 'feedback',
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
    async updateUserDisplayName() {
        return await this.userApi('patch', store.user.id, {
            command: 'update_user_display_name',
            display_name: store.user.display_name
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
        let result = await this.eventsApi('get', null, { command: 'getAllEvents' })
        return result
    },
    async getEvent(eventId) {
        let result = await this.eventsApi('get', eventId, { command: 'getEvent' })
        return result[0]
    },
    async createEvent(data) {
        data.command = 'add_event'
        let result = await this.eventsApi('post', null, data)
        return result[0]
    },
    //async getMyEvents() {
    //    let result = await this.eventsApi('post', null, { command: 'my_events' })
    //    return result
    //},
    async checkUserStatus(eventId) {
        return await this.eventsApi('post', null, {
            command: 'check_user_status',
            event_id: eventId,
        })
    },
    async changeGuestStatus(eventId, status, userId = null) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) { // this protection isnt in api yet
            await this.eventsApi('patch', eventId, {
                command: 'update_guest_status',
                status: status,
                user_id: userId,
            })
            return 'done'
        } else {
            return 'failed'
        }
    },
    async setPlusOne(eventId, plusOneName) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) { // this protection isnt in api yet
            await this.plusOneApi('post', null, {
                command: 'set_plus_one',
                plus_one_name: plusOneName,
                event_id: eventId,
            })
            return 'done'
        } else {
            return 'failed'
        }
    },
    async deletePlusOne(eventId) {
        if (f.isoStringDateToDateObject(store.events.selected.date_time) > f.today) { // this protection isnt in api yet
            await this.plusOneApi('post', null, {
                command: 'delete_plus_one',
                event_id: eventId,
            })
            return 'done'
        } else {
            return 'failed'
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
        formData.append('command', 'upload_image')
        let result = await this.imagesApi('post', null, formData)
        return result[0]
    },
    async getEventImage(imageId, eventId) {
        let formData = new FormData()
        formData.append('event_id', eventId)
        formData.append('command', 'get_event_image')
        formData.append('image_id', imageId)
        let result = await this.imagesApi('post', null, formData)
        if (result.length > 0) {
            return result[0].key
        } else {
            return 'fail'
        }
    },
    // GROUPS //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async getGroups() {
        let result = await this.groupApi('get', null, { 'command': 'get' })
        return result
    },
}