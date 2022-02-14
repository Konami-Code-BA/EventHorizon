<template>
	<div class="main" style="padding: 0; padding-left: 10px;">
		<div style="font-size: 36px;">FAQ</div>
		<div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
			<input :placeholder="t('SEARCH')" :value="search" @input="setSearch" type="text" autocorrect="off"
					autocapitalize="none" style="width: 100% padding-bottom: 2px" v-on:keyup.enter="removeFocus()"
					id="search" autocomplete="off"/>
			<div style="width: 10px;"/>
			<x-close-button :closeFunc="() => {setSearch({target: {value: ''}})}" style="padding-bottom: 0;"/>
		</div>
		<div style="overflow-y: scroll; width: 100%; display: flex; flex-direction: column; align-items: center;">
			<div style="width:80%; display: flex; flex-direction: column; align-items: flex-start; justify-content:
					flex-start; padding-bottom: 10px;" v-for="(item, index) in filteredQAndA" :key="index">
				<button class="no-border-button" v-on:click.prevent="item.display = !item.display"
						style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
						height: 50px; text-align: left; width: 100%;">
					{{item.question}}&nbsp;
					<div v-if="item.display"><img src="@/assets/upArrowIcon.png" style="width: 10px;"/></div>
					<div v-else><img src="@/assets/downArrowIcon.png" style="width: 10px;"/></div>
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
					{
						question: 'How can I host an event?',
						answer: `The hosting feature hasn't been released yet. Until then the only hosts are the site 
							creators (and maybe a couple close friends). As a guest, please feel free to check out the 
							events they have on the site.`,
						tags: '',
						display: false,
					}, {
						question: 'What kind of events can we expect to see on this site?',
						answer: `We made this site to help us with the events we were already planning: basically 
							drinking parties. At first that will probably be the main event (pun intended). But we want 
							to branch out so the site can be used for all kinds of events, such as yoga sessions, 
							flower viewing parties, international meet-ups, video game competitions; let your 
							imagination run wild!`,
						tags: 'type except',
						display: false,
					}, {
						question: 'What is the cancelation policy for events?',
						answer: `Event attendance is managed by the hosts of the event. It's different for every event. 
							You can always cancel by just clicking Decline on an event. Or switching from Attending to 
							Undecided. But you could also consider contacting the host to let them know what happened.`,
						tags: 'last minute',
						display: false,
					}, {
						question: 'Do I need an account to attend events?',
						answer: `Attendance is managed by the hosts. If you know the host and can organize with them to 
							attend the event without using EH, then go for it. EH is built to assist hosts by gathering 
							all information relating to the event in one place, so by making a free account and 
							confirming through the site, it would help the host out. Additionally, you'll be able to 
							access information about other events and parties happening in the city.`,
						tags: '',
						display: false,
					}, {
						question: 'What\'s the best way to get in contact with a host of an event?',
						answer: `Guests can message the hosts of an event they are part of. In the event page, under 
							people, you can click on the button next to "HOSTS" and you can message them there.`,
						tags: '',
						display: false,
					}, {
						question: 'How can I turn off line messages / emails / notifications?',
						answer: `In the settings screen you can turn off "Get Emails" and "Get Lines". You can't 
							however turn off messages from hosts of events you are attending. Hosts need to be able to 
							contact their guests. If the host is being annoying, maybe hes just not the kinda guy whose 
							events you want to attend.`,
						tags: '1 2',
						display: false,
					}, {
						question: `My line account and email account are separate. Now I have two accounts. 
						What do I do?`, 
						answer: `You can just log into one of your accounts, and then add the other one in the settings 
							page. For example, login with email, and then add line in the settings page. Or, login with 
							line, and then add email. The two accounts will be automatically merged together into one.`,
						tags: '',
						display: false,
					}, {
						question: 'What happens if I forget my password?',
						answer: `Click the Forgot Password link on the login page. It'll ask for your email address to 
							send you a link. Follow the link from your email and you can change your password.`,
						tags: 'forgot forgotten pw',
						display: false,
					}, {
						question: 'Can I change the language?',
						answer: `Yes! Currently, we support English and Japanese. Change language by clicking on the 
							menu button at the top of the site.`,
						tags: '',
						display: false,
					}, {
						question: 'How come the buttons aren\'t working in a past event?',
						answer: `Just like in real life, regrettably, you can't change past events.`,
						tags: 'click nothing',
						display: false,
					}, {
						question: 'Why are some of the event details missing?',
						answer: `It might be a private event. If you aren't invited to a private event, or you aren't 
							logged in, or don't have an account, private events hide some of the information from 
							outsiders.`,
						tags: 'cant can\'t see hidden anywhere any where',
						display: false,
					}, {
						question: 'How do I join a private event?',
						answer: `Click on the Invite Request button and the host will be alerted that you want to join. 
							Then just wait for the host to accept your request and invite you.`,
						tags: 'invitation',
						display: false,
					}, {
						question: 'Can I bring friends? ',
						answer: `Only 1 plus-one is allowed per guest. However, your friends are very welcome to 
							register (for free) and join the event themselves. If not, the last option is to contact 
							the host directly. `,
						tags: 'plusone, +',
						display: false,
					}
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
