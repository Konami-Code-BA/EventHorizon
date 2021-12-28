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
    async userApi(method, pk = null, data = null) {
        let uri = '/api/user/'
        if (pk) {
            uri += pk + '/'
        }
        return await this.axiosCall[method](this.baseUrl + uri, data)
            .then(response => {
                if (data.command == 'logout') {
                    console.log(`success - userApi ${data.command}`)
                    store.user = store.defaultUser
                    return store.user
                } else if (!('error' in response.data[0])) {
                    console.log(`success - userApi ${data.command}`)
                    store.user = response.data[0]
                    return store.user
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
                if (pk) {
                    return response.data[0]
                } else {
                    return response.data
                }
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
                if (pk) {
                    return response.data
                } else {
                    return response.data[0]
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - saveImageFunction:`, error)
                return error
            })
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    async registerWithEmail(email, password, displayName = null) {
        if (displayName && displayName !== '') {
            return await this.userApi('post', null, {
                command: 'register_with_email',
                display_name: displayName,
                email: email,
                password: password,
            })
        } else {
            return await this.userApi('patch', store.user.id, {
                command: 'register_email',
                email: email,
                password: password,
            })
        }
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
            command: 'sendEmail',
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
    async updateUserAlerts(name) {
        return await this.userApi('patch', store.user.id, {
            command: 'update_user_alerts',
            name: name,
        })
    },
    // LINE ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async sendWebhook(data) {
        await this.lineApi('post', '/webhook/', data)
    },
    async lineConsumption() {
        await this.lineApi('post', '/api/line/', {
            command: 'consumption',
        })
    },
    async linePush(data) {
        await this.lineApi('post', '/api/line/', {
            command: 'push',
            data: data,
        })
    },
    async lineBroadcast() {
        await this.lineApi('post', '/api/line/', {
            command: 'broadcast',
            message: 'sup this is a broadcast message',
        })
    },
    // EVENTS //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async getAllEvents() {
        return await this.eventsApi('get', null, null)
    },
    async getEvent(pk) {
        return await this.eventsApi('get', pk, null)
    },
    async createEvent(data) {
        data.command = 'add_event'
        return await this.eventsApi('post', null, data)
    },
    async getMyEvents() {
        return await this.eventsApi('post', null, { command: 'my_events' })
    },
    // IMAGES //////////////////////////////////////////////////////////////////////////////////////////////////////////
    async saveImage(formData) {
        return await this.imagesApi('post', null, formData)
    },
    async getImage(pk, formData) {
        formData.append('command', 'get')
        return await this.imagesApi('patch', pk, formData)
    },
}