export default {
    defaultUser: { // still need this?
        language: 'EN',
        groups: [100],
    },
    user: {
        language: 'EN', // still need these internal things?
        groups: [100],
    },
    pages: [],
    lastNonLoginRegisterPage: { page: 'home', args: {} },
    events: {
        selected: null,
        none: [],
        display: [],
        all: [],
        mine: [],
    },
    loading: true,
    groups: null,
    modalBack: false,
}