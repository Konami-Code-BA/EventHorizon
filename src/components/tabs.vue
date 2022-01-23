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
			numTabs: { default: 0 },
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
		outline: none;
		border: 2px solid rgba(255, 255, 255, .3);
		padding-top: 5px;
		padding-bottom: 5px;
		align-items: center;  /* this isnt for buttons, its for text */
	}
	.tab {
		width: 100%;
		padding-left: 5px;
		padding-right: 5px;
		display: flex;
		flex-direction: column;
		align-items: stretch;
		justify-content: center;
	}
	.button {
		outline: none;
		border: none;
		background: none;
		color: #ffe07a;
		cursor: pointer;
		padding: 0;
		text-decoration: none;
		width: 100%;
		border-radius: 0;
		height: 100%;
	}
	.selected {
		background-color: rgba(255, 255, 255, .2);  /*140,128,151,0.6 after combinging with #18002e*/
		width: 100%;
		height: 100%;
	}
</style>