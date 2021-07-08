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
    async registerByEmail(email, password) {
        await this.userApiFunction('post', '/api/user/', {
            command: 'register_by_email',
            email: email,
            password: password,
            language: store.user.language,
        })
    },
    //async registerByLine(line, lineAccessToken) {
    //    await this.userApiFunction('post', '/api/user/', {
    //        command: 'register_by_line',
    //        line: line,
    //        lineAccessToken: lineAccessToken,
    //        language: store.user.language,
    //    })
    //},
    async login(data) {
        data['command'] = 'login'
        console.log('login')
        await this.userApiFunction('post', '/api/user/', data)
    },
    //async loginByLine(email, password) {
    //    await this.userApiFunction('post', '/api/user/', {
    //        command: 'login',
    //		email: email,
    //		password: password,
    //    })
    //},
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
            getEmail: store.user.do_get_emails,
        })
    },
    async updateUserLocation() {
        await this.userApiFunction('patch', '/api/user/' + store.user.id + '/', {
            command: 'update_user_location',
            ip_continent_name: store.user.ip_continent_name,
            ip_country_name: store.user.ip_country_name,
            ip_state_prov: store.user.ip_state_prov,
            ip_city: store.user.ip_city,
            ip_date: store.user.ip_date,
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
    //async lineGetAccessToken(code, state) {
    //    await this.lineApiFunction('post', '/api/line/', {
    //        command: 'get_access_token',
    //        code: code,
    //        state: state,
    //    })
    //},
    async lineNewDevice(code) {
        await this.lineApiFunction('post', '/api/line/', {
            command: 'new_device',
            code: code,
            language: store.user.language,
        })
    },
    // SECRETS /////////////////////////////////////////////////////////////////////////////////////////////////////////
    async loginChannelId() {
        let response = await this.secretsApiFunction('login_channel_id')
        return response
    },
    async state() {
        let response = await this.secretsApiFunction('random_secret')
        return response
    },
    async ip() {
        axios.defaults.withCredentials = false
        await this.axiosCall['get']('https://api.db-ip.com/v2/free/self')
            .then(response => {
                store.user.ip_continent_name = response.data['continentName']
                store.user.ip_country_name = response.data['countryName']
                store.user.ip_state_prov = response.data['stateProv']
                store.user.ip_city = response.data['city']
                store.user.ip_date = new Date().toISOString()
            })
            .catch(error => {
                console.log(`ip ERROR:`, error)
            })
    },
}