import store from '@/store.js'
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
    async userApiFunction(method, pk = null, data = null) {
        let uri = '/api/user/'
        if (pk) {
            uri += pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + uri, data)
            .then(response => {
                if (data.command == 'logout') {
                    console.log(`success - userApiFunction ${data.command}`)
                    store.user = store.defaultUser
                    return store.user
                } else if (!('error' in response.data[0])) {
                    console.log(`success - userApiFunction ${data.command}`)
                    store.user = response.data[0]
                    return store.user
                } else {
                    console.log(`*INTERNAL ERROR* - userApiFunction ${data.command}:`, response.data[0]['error'])
                    return response.data[0]
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - userApiFunction ${data.command}:`, error)
                return error
            })
    },
    async lineApiFunction(method, uri, data) {
        return await this.axiosCall[method](this.baseUrl + uri, data)
            .then(response => {
                if (!('error' in response.data)) {
                    console.log(`success - lineApiFunction ${data.command}`)
                    return response.data
                } else {
                    console.log(`*INTERNAL ERROR* - lineApiFunction ${data.command}:`, response.data['error'])
                    return response.data['error']
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - lineApiFunction ${data.command}:`, error)
                return error
            })
    },
    async secretsApiFunction(toGet) {
        return await this.axiosCall['get'](this.baseUrl + '/api/secrets/' + toGet + '/')
            .then(response => {
                console.log(`success - secretsApiFunction ${toGet}`)
                return response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - secretsApiFunction ${toGet}:`, error)
                return error
            })
    },
    async eventsApiFunction(method, pk = null, data = null) {
        let output = null
        let id = ''
        if (pk) {
            id = pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + '/api/events/' + id, data)
            .then(response => {
                console.log(`success - eventsApiFunction`)
                if (pk) {
                    return response.data[0]
                } else {
                    return response.data
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - eventsApiFunction:`, error)
                return error
            })
    },
    async saveImage(formData) {
        return await this.axiosCall['post'](this.baseUrl + '/api/images/', formData, {
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
    async getImage(pk) {
        return await this.axiosCall['get'](this.baseUrl + '/api/images/' + pk + '/')
            .then(response => {
                console.log(`success - saveImageFunction`)
                return response.data[0]
            })
            .catch(error => {
                console.log(`*API ERROR* - saveImageFunction:`, error)
                return error
            })
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    async registerWithEmail(email, password, displayName = null) {
        if (displayName && displayName !== '') {
            return await this.userApiFunction('post', null, {
                command: 'register_with_email',
                display_name: displayName,
                email: email,
                password: password,
            })
        } else {
            return await this.userApiFunction('patch', store.user.id, {
                command: 'register_email',
                email: email,
                password: password,
            })
        }
    },
    async login(data) {
        data['command'] = 'login'
        return await this.userApiFunction('post', null, data)

    },
    async lineNewDevice(code, path) {
        return await this.userApiFunction('post', null, {
            command: 'line_new_device',
            code: code,
            path: path,
        })
    },
    async logout() {
        return await this.userApiFunction('post', null, {
            command: 'logout',
        })
    },
    async sendEmail() {
        return await this.userApiFunction('post', null, {
            command: 'sendEmail',
        })
    },
    async updateUserLanguage() {
        return await this.userApiFunction('patch', store.user.id, {
            command: 'update_user_language',
            language: store.user.language,
        })
    },
    async updateUserDoGetEmails() {
        return await this.userApiFunction('patch', store.user.id, {
            command: 'update_user_do_get_emails',
            do_get_emails: store.user.do_get_emails,
        })
    },
    async updateUserAlerts(name) {
        return await this.userApiFunction('patch', store.user.id, {
            command: 'update_user_alerts',
            name: name,
        })
    },
    // LINE ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async sendWebhook(data) {
        await this.lineApiFunction('post', '/webhook/', data)
    },
    async lineConsumption() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'consumption',
        })
    },
    async linePush(data) {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'push',
            data: data,
        })
    },
    async lineBroadcast() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'broadcast',
            message: 'sup this is a broadcast message',
        })
    },
    // EVENTS //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async getAllEvents() {
        return await this.eventsApiFunction('get', null, null)
    },
    async getEvent(pk) {
        return await this.eventsApiFunction('get', pk, null)
    },
    async createEvent(data) {
        data.command = 'add_event'
        return await this.eventsApiFunction('post', null, data)
    },
    async getMyEvents() {
        return await this.eventsApiFunction('post', null, { command: 'my_events' })
    },
}