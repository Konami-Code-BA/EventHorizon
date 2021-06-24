import store from '@/store.js'
export default {
    translationsDict: {
        '': { '': '' },
        'LOGIN': {
            'EN': 'LOGIN',
            'JP': 'ログイン'
        },
        'MENU': {
            'EN': 'MENU',
            'JP': 'メニュー'
        },
        'LOGOUT': {
            'EN': 'LOGOUT',
            'JP': 'ログアウト'
        },
        'USERNAME': {
            'EN': 'USERNAME',
            'JP': 'ユーザー名'
        },
        'EMAIL': {
            'EN': 'EMAIL',
            'JP': 'Eメール'
        },
        'PASSWORD': {
            'EN': 'PASSWORD',
            'JP': 'パスワード'
        },
        'SHOW': {
            'EN': 'SHOW',
            'JP': '表示'
        },
        'HIDE': {
            'EN': 'HIDE',
            'JP': '非表示'
        },
        'REGISTER': {
            'EN': 'REGISTER',
            'JP': '登録'
        },
        'LANGUAGE': {
            'EN': 'LANGUAGE',
            'JP': '言語'
        },
        'GO TO REGISTRATION': {
            'EN': 'GO TO REGISTRATION',
            'JP': '登録画面へ'
        },
        'LOGGED IN': {
            'EN': 'LOGGED IN ✅',
            'JP': 'ログインした✅'
        },
        'LOGGED OUT': {
            'EN': 'LOGGED OUT 👋',
            'JP': 'ログアウトした👋'
        },
        'REGISTERED': {
            'EN': 'REGISTERED ✅',
            'JP': '登録した✅'
        },
        'HOME': {
            'EN': 'HOME',
            'JP': 'ホーム'
        },
        'SETTINGS': {
            'EN': 'SETTINGS',
            'JP': '設定'
        },
        'GET EMAILS': {
            'EN': 'GET EMAILS',
            'JP': 'Eメール送信'
        },
        'UPCOMING EVENTS': {
            'EN': 'UPCOMING EVENTS',
            'JP': '今後のイベント'
        },
        'MY EVENTS': {
            'EN': 'MY EVENTS',
            'JP': 'マイ・イベント'
        },
        'TBA': {
            'EN': 'TBA',
            'JP': '未定'
        },
        'COMING SOON': {
            'EN': 'COMING SOON',
            'JP': '近日公開'
        },
    },

    t: function(w) {
        return this.translationsDict[w][store.user.language]
    }
}