<template>
	<div class="main" v-if="event">
		<div class="flex-row" style="align-items: center; justify-content: space-between; height: 60px;">
			<div style="width: 16px"></div>
			<h2 style="text-align: center">{{event['name']}}</h2>
			<button v-on:click.prevent="$emit('closeModals')" class="no-border-button" style="align-self: flex-start">
				✖
			</button>
			<!-- let say we come here from map. and we go back. itd be cool if list and calendar are focuson on this event -->
		</div>
		<div class="flex-table">
			<div style="align-self: flex-end">
				<small>{{ event['is_private'] ? 'PRIVATE EVENT' : 'PUBLIC EVENT' }}</small>
			</div>
			<br>
			<div>
				DESCRIPTION
			</div>
			<div style="align-self: center">
				{{event['description']}}
			</div>
			<div v-if="!event['is_private'] || Array.isArray(event['invited'])" class="flex-table">
				<br>
				<div>
					VENUE
				</div>
				<div style="align-self: center">
					{{event['venue_name']}}
				</div>
			</div>
			<br>
			<div>
				ADDRESS
			</div>
			<div style="align-self: center">
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<small>{{ event['address'] }}</small>
				</button>
			</div>
			<br>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					DATE
				</div>
				<div>
					<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
						{{ getDate() }}
					</button>
				</div>
			</div>
			<br>
			<div class="flex-row" style="justify-content: space-between">
				<div style="align-self: center">
					HOSTS
				</div>
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<div v-if="Array.isArray(event['invited'])" class="flex-row" style="align-self: center">
						{{ event['hosts'].length }}
						<div v-if="event['hosts'].length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event['hosts'] }}
						<div v-if="event['hosts'] > 1">
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
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<div v-if="Array.isArray(event['invited'])" class="flex-row" style="align-self: center">
						{{ event['invited'].length }}
						<div v-if="event['invited'].length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event['invited'] }}
						<div v-if="event['invited'] > 1">
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
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<div v-if="Array.isArray(event['invited'])" class="flex-row" style="align-self: center">
						{{ event['confirmed_guests'].length }}
						<div v-if="event['confirmed_guests'].length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event['confirmed_guests'] }}
						<div v-if="event['confirmed_guests'] > 1">
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
				<button v-on:click.prevent="$emit('goToMap')" class="button" style="align-self: center">
					<div v-if="Array.isArray(event['invited'])" class="flex-row" style="align-self: center">
						{{ event['interested'].length }}
						<div v-if="0 >= event['interested'].length > 1">
							&nbsp;people
						</div>
						<div v-else>
							&nbsp;person
						</div>
					</div>
					<div v-else class="flex-row" style="align-self: center">
						{{ event['interested'] }}
						<div v-if="event['interested'] > 1">
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
	import apiFunctions from '@/functions/apiFunctions.js'
	import functions from '@/functions/functions.js'
	export default {
		name: 'event',
		components: {
		},
		data () {
			return {
				store: store,
				event: null,
				eventId: null,
			}
		},
		props: {
			id: {},
		},
		async mounted () {
			if (this.$route.params.id) {
				this.eventId = this.$route.params.id
			} else {
				this.eventId = this.id
			}
			this.event = await apiFunctions.getEvent(this.eventId)
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			getDate () {
				let date_time = this.event['date_time'].split('T')
				let date = date_time[0]
				let time = date_time[1]
				time = time.split(':')
				time = time[0] + ':' + time[1]
				return date + '\xa0\xa0-\xa0\xa0' + time
			}
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
