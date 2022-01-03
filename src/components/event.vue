<template>
	<div class="main" v-if="event">
		<div class="flex-row" style="align-items: center; justify-content: space-between; height: 60px;">
			<div style="width: 16px"></div>
			<h2 style="text-align: center; max-width: 80%; overflow-x: scroll;">{{event.name}}</h2>
			<button v-on:click.prevent="$emit('closeModals')" class="no-border-button x-button" style="align-self: flex-start">
				✖
			</button>
			<!-- let say we come here from map. and we go back. itd be cool if list and calendar are focuson on this event -->
		</div>
		<div class="flex-table">
			<div class="flex-row" style="justify-content: space-between">
				<div>
					{{ getDate() }}
				</div>
				<div>
					<small>{{ event.is_private ? 'PRIVATE EVENT' : 'PUBLIC EVENT' }}</small>
				</div>
			</div>
			<br>
			<div style="align-self: center">
				{{ event.description }}
			</div>
			<div v-if="(!event.is_private || this.isInvited) && event.venue_name" class="flex-table">
				<br>
				<div>
					VENUE:
				</div>
				<div style="align-self: center">
					{{ event.venue_name }}
				</div>
			</div>
			<br>
			<div style="align-self: center">
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<small>{{ event.address }}</small>
				</button>
			</div>
			<br>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					HOSTS
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!isInvited && event.is_private">
					<div v-if="this.isInvited || !event.is_private" class="flex-row" style="align-self: center">
						{{ event.hosts.length }}
						<div v-if="event.hosts.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.hosts }}
						<div v-if="event.hosts > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					INVITED
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!isInvited && event.is_private">
					<div v-if="this.isInvited || !event.is_private" class="flex-row" style="align-self: center">
						{{ event.invited.length }}
						<div v-if="event.invited.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.invited }}
						<div v-if="event.invited > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					CONFIRMED GUESTS
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!isInvited && event.is_private">
					<div v-if="this.isInvited || !event.is_private" class="flex-row" style="align-self: center">
						{{ event.confirmed_guests.length }}
						<div v-if="event.confirmed_guests.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.confirmed_guests }}
						<div v-if="event.confirmed_guests > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					INTERESTED
				</div>
				<button v-on:click.prevent="" class="button" style="align-self: center"
						:disabled="!isInvited && event.is_private">
					<div v-if="this.isInvited || !event.is_private" class="flex-row" style="align-self: center">
						{{ event.interested.length }}
						<div v-if="0 >= event.interested.length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event.interested }}
						<div v-if="event.interested > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
				</button>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'event',
		components: {
		},
		data () {
			return {
				store: store,
				event: null,
				isInvited: null,
			}
		},
		props: {
			eventId: { default: null },
		},
		computed: {
		},
		async mounted () {
			this.event = await api.getEvent(this.eventId)
			this.isInvited = this.isInvitedGuest(this.event)
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			getDate () {
				let date_time = this.event.date_time.split('T')
				let date = date_time[0]
				let time = date_time[1]
				time = time.split(':')
				time = time[0] + ':' + time[1]
				return date + '\xa0\xa0-\xa0\xa0' + time
			},
			isInvitedGuest (event) {
				return f.isInvitedGuest(event)
			},
			//async getEventImage () {
			//	let result = await api.getEventImage(this.getimgid, eventId) // this.event.id
			//	this.imagetwo = "data:image/jpg;base64," + result['image_data']
			//},
		} // methods
	} // export
</script>
<style scoped>
	.flex-table {
		width: 100%;
		display: flex;
		flex-direction: column;
	}
	.flex-row {
		width: 100%;
		display: flex;
		flex-direction: row;
	}
</style>
