<template>
	<div class="tabs">
		<div v-for="num in numTabs" class="tab">
			<div v-if="notButtons.includes(num)">
				<slot :name="num"/>
			</div>
			<div v-else>
				<button v-on:click.prevent="buttonClick(num)" class="button" :class="{ selected : selected === num}">
					<slot :name="num"/>
				</button>
			</div>
		</div>
	</div>
</template>
<script>
	export default {
		name: 'appFooter',
		data () {
			return {
				selected: this.initial
			}
		},
		components: {
		},
		props: {
			numTabs: {},
			notButtons: { default: function () { return [] } },
			initial: { default: 0 },  // initial = 0 will turn off having a tab set to selected styling
		},
		computed: {
		},
		async mounted () {
		},
		methods: {
			buttonClick (num) {
				this.$emit('on-click', num)
				if (this.initial != 0) {
					this.selected = num
				}
			}
		}
	}
</script>
<style scoped>
	.tabs {
		display: flex;
		flex-direction: row;
		border: 1px solid rgba(255, 255, 255, .1);
		padding-bottom: 0;
		align-items: flex-end;  /* this isnt for buttons, its for text */
	}
	.tab {
		width: 100%;
		padding-left: 5px;
		padding-right: 5px;
		display: flex;
		flex-direction: column;
	}
	.button {
		border: none;
		background: none;
		color: #ffe07a;
		cursor: pointer;
		padding: 0;
		text-decoration: none;
		width: 100%;
		border-radius: 0;
	}
	.selected {
		background-color: rgba(255, 255, 255, .1);
		width: 100%;
	}
</style>