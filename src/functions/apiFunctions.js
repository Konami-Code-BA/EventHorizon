import store from '@/store.js'
axios.defaults.withCredentials = true
axios.defaults.xsrfHeaderName = "X-CSRFToken"
    //let csrftoken = JSON.parse('{"' + document.cookie.replaceAll('=', '": "').replaceAll('; ', '", "') + '"}')['XSRF-TOKEN']
    //axios.defaults.headers.common['X-CSRFToken'] = csrftoken
import axios from 'axios'
export default {
    get ApiBaseUrl() { return process.env.NODE_ENV == 'development' ? 'http://127.0.0.1:8000' : '' },
    axiosCall: {
        post: axios.post,
        patch: axios.patch,
        get: axios.get,
    },
    // API /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    async userApiFunction(method, uri, data) {
        let output = store.defaultUser
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                if (response.data !== '' && data.command !== 'logout') {
                    output = response.data
                }
            })
            .catch(error => {
                console.log(`${data.command} ERROR:`, error)
            })
            .finally(() => {
                store.user = output
            })
    },
    async lineApiFunction(method, uri, data) {
        let output = null
        await this.axiosCall[method](this.ApiBaseUrl + uri, data)
            .then(response => {
                if (response.data !== '') {
                    output = response.data
                }
            })
            .catch(error => {
                console.log(`${data.command} ERROR:`, error)
            })
        return output
    },
    async secretsApiFunction(toGet) {
        let output = null
        await this.axiosCall['get'](this.ApiBaseUrl + '/api/secrets/' + toGet + '/')
            .then(response => {
                if (response.data !== '') {
                    output = response.data
                }
            })
            .catch(error => {
                console.log(`${toGet} ERROR:`, error)
            })
        return output
    },
    // USERS ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    async registerWithEmail(displayName, email, password) {
        await this.userApiFunction('post', '/api/user/', {
            command: 'register_with_email',
            display_name: displayName,
            email: email,
            password: password,
        })
    },
    async login(data) {
        data['command'] = 'login'
        await this.userApiFunction('post', '/api/user/', data)
    },
    async lineNewDevice(code) {
        await this.userApiFunction('post', '/api/user/', {
            command: 'line_new_device',
            code: code,
        })
    },
    async logout() {
        await this.userApiFunction('post', '/api/user/', {
            command: 'logout',
        })
    },
    async sendEmail() {
        await this.userApiFunction('post', '/api/user/', {
            command: 'sendEmail',
        })
    },
    async updateUserLanguage() {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_language',
            language: store.user.language,
        })
    },
    async updateUserDoGetEmails() {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_do_get_emails',
            do_get_emails: store.user.do_get_emails,
        })
    },
    async updateUserAlerts(name) {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
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
    // SECRETS /////////////////////////////////////////////////////////////////////////////////////////////////////////
    async loginChannelId() {
        let response = await this.secretsApiFunction('login_channel_id')
        return response
    },
    async state() {
        let response = await this.secretsApiFunction('new_random_secret')
        return response
    },
}