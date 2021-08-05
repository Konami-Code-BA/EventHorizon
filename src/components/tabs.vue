<template>
	<div class="tabs">
		<div v-for="no in tabNo">
			<div>
				<slot :name="no"/>
			</div>
		</div>
	</div>
</template>
<script>
	export default {
		name: 'appFooter',
		data () {
			return {
			}
		},
		components: {
		},
		props: {
			tabNo: {},
		},
		computed: {
		},
		async mounted () {
		},
		methods: {
		}
	}
</script>
<style scoped>
	.tabs {
		width: 100%;
		display: flex;
		flex-direction: row;
		align-items: flex-end;
		justify-content: space-around;
		height: 30px;
		background-color: rgba(0, 0, 0, .2);
		box-shadow: 0 0 1px rgba(255, 255, 255, .5);
	}
</style>