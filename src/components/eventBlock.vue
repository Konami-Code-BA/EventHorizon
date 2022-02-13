<template>
	<div class="event-box">
		<img :src="image" style="height: 40px; width: 40px; object-fit: cover; border-radius: 50%; flex-shrink: 0;">
		<div style="display: flex; flex-direction: column; align-items: flex-start; width: 100%; min-width: 0">
			<div class="text-area">
				{{ event.name }}
			</div>
			<div class="date-area" style="">
				<div style="font-weight: 100;">{{ event.date_time.split('T')[0] }}</div>
				<div style="color: green">{{ t(userStatus) }}</div>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	export default {
		name: 'eventBlock',
		data () {
			return {
				image: require('@/assets/pexels-photo-event4.jpeg'),
				userStatus: '',
			}
		},
		props: {
			event: {},
		},
		computed: {
		},
		async mounted () {
			this.userStatus = this.event.myStatus
			if (this.event.image_data) {
				this.image = this.event.image_data
			}
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
	.event-box {
		width: 100%;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		background-color: rgba(255, 255, 255, .1);
		color: #cae2ff;
		padding: 8px;
		border-radius: 4px;
		height: 50px;
		min-height: 50px;
	}
	.text-area {
		overflow-x: clip;
		white-space: nowrap;
		width: 100%;
		text-align: left;
		margin-left: 8px;
	}
	.date-area {
		font-size: 12px;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		width: 100%;
		margin-left: 6px;
		padding-right: 8px;
	}
</style>
