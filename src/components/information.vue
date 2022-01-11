<template>
	<modal @closeModals="closeInfo">
		<div slot="contents" class="modal">
			<div style="align-self: flex-end; padding-bottom: 5px;">
				<button v-on:click.prevent="closeInfo" class="no-border-button x-button">
					✖
				</button>
			</div>
			<div>
				{{ theInfo[whichInfo] }}<br>
				For more info, go here [link]
			</div>
		</div>
	</modal>
</template>
<script>
	import modal from '@/components/modal'
	export default {
		name: 'information',
		components: {
			modal,
		},
		props: {
			closeInfo: {},
			whichInfo: {},
		},
		data () {
			return {
				theInfo: {
					'events': 'Events are like, bro',
					'peopleFilters': 'you know what tho man',
				}
			}
		},
		mounted () {
		},
		methods: {
		}
	}
</script>
<style scoped>
</style>