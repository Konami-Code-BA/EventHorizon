import store from '@/store.js'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
    //let csrftoken = JSON.parse('{"' + document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "') + '"}')['XSRF-TOKEN']
    //axios.defaults.headers.common['X-CSRFToken'] = csrftoken
import axios from 'axios'
export default {
    get ApiBaseUrl() { return process.env.PYTHON_ENV == 'development' ? 'http://127.0.0.1:8000' : '' },
    axiosCall: {
        post: axios.post,
        patch: axios.patch,
        get: axios.get,
    },
    // API /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async userApiFunction(method, uri, data) {
        let output = store.user
        let error = null
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                if (data.command == 'logout') {
                    console.log(`success - userApiFunction ${data.command}`)
                    output = store.defaultUser
                } else if (!('error' in response.data[0])) {
                    console.log(`success - userApiFunction ${data.command}`)
                    output = response.data[0]
                } else {
                    console.log(`*INTERNAL ERROR* - userApiFunction ${data.command}:`, response.data[0]['error'])
                    error = response.data[0]['error']
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - userApiFunction ${data.command}:`, error)
            })
            .finally(() => {
                store.user = output
            })
        return error
    },
    async lineApiFunction(method, uri, data) {
        let output = null
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                if (!('error' in response.data)) {
                    console.log(`success - lineApiFunction ${data.command}`)
                    output = response.data
                } else {
                    console.log(`*INTERNAL ERROR* - lineApiFunction ${data.command}:`, response.data['error'])
                }
            })
            .catch(error => {
                console.log(`*API ERROR* - lineApiFunction ${data.command}:`, error)
            })
        return output
    },
    async secretsApiFunction(toGet) {
        let output = null
        await this.axiosCall['get'](this.ApiBaseUrl + '/api/secrets/' + toGet + '/')
            .then(response => {
                console.log(`success - secretsApiFunction ${toGet}`)
                output = response.data
            })
            .catch(error => {
                console.log(`*API ERROR* - secretsApiFunction ${toGet}:`, error)
            })
        return output
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    async registerWithEmail(email, password, displayName = null) {
        if (displayName && displayName !== '') {
            return await this.userApiFunction('post', '/api/user/', {
                command: 'register_with_email',
                display_name: displayName,
                email: email,
                password: password,
            })
        } else {
            return await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
                command: 'register_email',
                email: email,
                password: password,
            })
        }
    },
    async login(data) {
        data['command'] = 'login'
        return await this.userApiFunction('post', '/api/user/', data)
    },
    async lineNewDevice(code) {
        return await this.userApiFunction('post', '/api/user/', {
            command: 'line_new_device',
            code: code,
        })
    },
    async logout() {
        return await this.userApiFunction('post', '/api/user/', {
            command: 'logout',
        })
    },
    async sendEmail() {
        return await this.userApiFunction('post', '/api/user/', {
            command: 'sendEmail',
        })
    },
    async updateUserLanguage() {
        return await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_language',
            language: store.user.language,
        })
    },
    async updateUserDoGetEmails() {
        return await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_do_get_emails',
            do_get_emails: store.user.do_get_emails,
        })
    },
    async updateUserAlerts(name) {
        return await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_alerts',
            name: name,
        })
    },
    // LINE ////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async sendWebhook() {
        await this.lineApiFunction('post', '/webhook/', {
            command: 'sendWebhook',
        })
    },
    async lineConsumption() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'consumption',
        })
    },
    async linePush() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'push',
            message: 'sup this is a push message',
            to: 'mikey',
        })
    },
    async lineBroadcast() {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'broadcast',
            message: 'sup this is a broadcast message',
        })
    },
}