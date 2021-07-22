import store from '@/store.js'
export default {
    translationsDict: {
        '': { '': '' },
        'REACH OUT TO NEW HORIZONS': {
            'EN': 'REACH OUT\nTO NEW HORIZONS',
            'JP': '新たな地平線への\n到達を目指して'
        },
        'LOGIN': {
            'EN': 'LOGIN',
            'JP': 'ログイン'
        },
        'REGISTER': {
            'EN': 'REGISTER',
            'JP': '登録'
        },
        'LOGIN / REGISTER': {
            'EN': 'LOGIN / REGISTER',
            'JP': 'ログイン・登録'
        },
        'NEW USER REGISTRATION': {
            'EN': 'NEW USER REGISTRATION',
            'JP': '新規登録'
        },
        'MENU': {
            'EN': 'MENU',
            'JP': 'メニュー'
        },
        'LOGOUT': {
            'EN': 'LOGOUT',
            'JP': 'ログアウト'
        },
        'DISPLAY NAME': {
            'EN': 'DISPLAY NAME',
            'JP': '表示名'
        },
        'EMAIL': {
            'EN': 'EMAIL',
            'JP': 'Eメール'
        },
        'PASSWORD': {
            'EN': 'PASSWORD',
            'JP': 'パスワード'
        },
        'PASSWORD (AGAIN)': {
            'EN': 'PASSWORD (AGAIN)',
            'JP': 'パスワード確認'
        },
        "PASSWORDS DON'T MATCH": {
            'EN': "PASSWORDS DON'T MATCH",
            'JP': 'パスワードが一致しません'
        },
        "FORGOT PASSWORD": {
            'EN': "FORGOT PASSWORD",
            'JP': 'パスワードが忘れました'
        },
        'SHOW': {
            'EN': 'SHOW',
            'JP': '表示'
        },
        'HIDE': {
            'EN': 'HIDE',
            'JP': '非表示'
        },
        'LANGUAGE': {
            'EN': 'LANGUAGE',
            'JP': '言語'
        },
        'GO TO REGISTRATION': {
            'EN': 'GO TO REGISTRATION',
            'JP': '登録画面へ'
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
        'LOGIN WITH EMAIL': {
            'EN': 'LOGIN WITH EMAIL',
            'JP': 'Eメールでログイン'
        },
        'REGISTER WITH EMAIL': {
            'EN': 'REGISTER WITH EMAIL',
            'JP': 'Eメールで登録'
        },
        'OK': {
            'EN': 'OK',
            'JP': '了解'
        },
        'This site uses cookies': {
            'EN': 'This site\nuses cookies',
            'JP': 'このサイトでは\nクッキーが使われています'
        },
        'ADD EMAIL ADDRESS': {
            'EN': 'ADD EMAIL ADDRESS',
            'JP': 'Eメールアドレスを追加する'
        },
        'Password can\'t be empty': {
            'EN': 'Password can\'t be empty',
            'JP': 'Eメールアドレスを追加する'
        },
        'Password confirmation can\'t be empty': {
            'EN': 'Password confirmation can\'t be empty',
            'JP': 'Eメールアドレスを追加する'
        },
        'Must be 4 characters or more': {
            'EN': 'Must be 4 characters or more',
            'JP': '4文字以上'
        },
        'Passwords don\'t match': {
            'EN': 'Passwords don\'t match',
            'JP': 'パスワードが不一致'
        },
        'This is an impossible email': {
            'EN': 'This is an impossible email',
            'JP': '無効なEメールアドレス'
        },
        'Must be 75 characters or less': {
            'EN': 'Must be 75 characters or less',
            'JP': '75文字以下'
        },
        'Required': {
            'EN': 'Required',
            'JP': '必須項目'
        },
        'Only these symbols are allowed: . _ - @': {
            'EN': 'Only these symbols are allowed: . _ - @',
            'JP': '記号は次の中から使用可: . _ - @'
        },
        'Must be 40 characters or less': {
            'EN': 'Must be 40 characters or less',
            'JP': '40文字以下'
        },
    },

    t: function(w) {
        try {
            return this.translationsDict[w][store.user.language]
        } catch (e) {
            console.log(e, 'word:', w)
            return 'TRANSLATION ERROR'
        }
    }
}