<template>
	<div class="main" style="padding: 0; padding-left: 10px;">
		<div style="font-size: 36px;">FAQ</div>
		<div style="overflow-y: scroll; width: 100%; display: flex; flex-direction: column; align-items: center;">
			<div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
				<input :placeholder="t('SEARCH')" :value="search" @input="setSearch" type="text" autocorrect="off"
						autocapitalize="none" style="width: 100% padding-bottom: 2px" v-on:keyup.enter="removeFocus()"
						id="search" autocomplete="off"/>
				<div style="width: 10px;"/>
				<x-close-button :closeFunc="() => {setSearch({target: {value: ''}})}" style="padding-bottom: 0;"/>
			</div>
			<div style="width:80%; display: flex; flex-direction: column; align-items: flex-start; justify-content: flex-start;" v-for="(item, index) in filteredQAndA" :key="index">
				<button class="no-border-button" v-on:click.prevent="item.display = !item.display"
						style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
						height: 50px; text-align: left; width: 100%">
					{{item.question}}&nbsp;
					<div v-if="item.display">⇧</div>
					<div v-else>⇩</div>
				</button>
				<div v-show="item.display">
					{{item.answer}}
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import xCloseButton from '@/components/xCloseButton.vue'
	export default {
		name: 'faq',
		components: {
            xCloseButton,
        },
		data () {
			return {
				search: '',
				//display: {1: false, 2: false, 3: false, 4: false, 5: false,},
				qAndA: [
					{question: 'How can I host an event?', answer: `The hosting services are currently under 
					construction and should be available in the coming weeks/months. Until then, 
					users can see upcoming events, including public events like festivals and parties 
					held by the app creators.`, tags: '', display: false},
					{question: 'What kind of events can we expect to see on this app?', answer: `This 
					service was built with house/rental space parties in mind. After the release of the hosting 
					services, general users can plan and advertise any type of event (within reason, of course), 
					such as yoga sessions, flower viewing parties, international meet-ups, video game competitions; 
					let your imagination run wild!`, tags: 'type except', display: false},
					{question: 'What is the cancelation policy for events?', answer: `Event attendance is managed by the hosts of the event. 
					It's different for every event. You can always cancel by just clicking Decline on an event, 
					or switch from Attending to Maybe. However, you could also consider contacting the host to 
					let them know what happened.`, tags: 'last minute', display: false},
					{question: 'I clicked into an event with no details, what is this?', answer: `It might be a private event. 
					If you aren't invited to a private event, or you aren't logged in, or don't have an account, 
					private events hide some of the information from outsiders.`, tags: 'cant can\'t see any where hidden no', display: false},
					{question: 'How do I join a private event', answer: `Click on the Invite Request button and the 
					host will be alerted that you want to join. Then just wait for the host to accept your request 
					and invite you.`, tags: '', display: false},
					{question: 'Do I need an account to attend events?', answer: `Attendance is managed by the host. If you know the host and can organise with them to attend the event 
					without using EH, then you can. EH is built to assist event planners by gathering all information 
					relating to the event in one place, so by making a free account and confirming through the app, it 
					would help the host out. Additionally, you'll be able to access information about other events and 
					parties happening in the city.`, tags: '', display: false},
					{question: 'Can I change the language?', answer: `Yes! Currently, we support English and Japanese.`, tags: '', display: false},
					{question: 'Why aren’t the buttons working for past events?', answer: `Just like in real life, regrettably, 
					you can't change past events.`, tags: 'click nothing', display: false},
					{question: 'Can I bring friends to events?', answer: `Only 1 plus-one is allowed per guest. 
					However, your friends are very welcome to register (for free) and join the event themselves. 
					If not, the last option is to contact the host directly. `, tags: 'plusone +', display: false},
				],
				filteredQAndA: null,
			}
		},
		created () {
			this.filteredQAndA = this.qAndA
		},
		methods: {
			t (w) { return translations.t(w) },
			setSearch (evt) {
				this.search = evt.target.value
				let upperCaseSearch = this.search.toUpperCase()
				let result = this.qAndA.filter(item => {
					return item.question.toUpperCase().includes(upperCaseSearch) || item.answer.toUpperCase().includes(upperCaseSearch) || item.tags.toUpperCase().includes(upperCaseSearch)
				})
				this.filteredQAndA = result
			},

			removeFocus() {
				document.getElementById('search').blur()
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
