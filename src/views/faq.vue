<template>
	<div class="main" style="padding: 0; padding-left: 10px;">
		<div style="font-size: 36px;">FAQ</div>
		<div style="display: flex; flex-direction: row; justify-content: center; align-items: center;">
			<input :placeholder="t('SEARCH')" :value="search" @input="setSearch" type="text" autocorrect="off"
					autocapitalize="none" style="width: 100% padding-bottom: 2px" v-on:keyup.enter="removeFocus()"
					id="searchFaq" autocomplete="off"/>
			<div style="width: 10px;"/>
			<x-close-button :closeFunc="() => {setSearch({target: {value: ''}})}" style="padding-bottom: 0;"/>
		</div>
		<div style="overflow-y: scroll; width: 100%; display: flex; flex-direction: column; align-items: center;
				justify-content: flex-start; padding-top: 20px;">
			<div style="width:80%; display: flex; flex-direction: column; align-items: flex-start; justify-content:
					flex-start; padding-bottom: 10px; height: fit-content; flex-shrink: 0; line-height:1.5em; min-height:6em;"
					v-for="(item, index) in filteredQAndA" :key="index">
				<button class="no-border-button" v-on:click.prevent="item.display = !item.display"
						style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
						height: 50px; text-align: left; width: 100%;">
					{{item.question}}&nbsp;
					<div v-if="item.display"><img src="@/assets/upArrowIcon.png" style="width: 10px;"/></div>
					<div v-else><img src="@/assets/downArrowIcon.png" style="width: 10px;"/></div>
				</button>
				<div v-show="item.display" style="padding-top: 5px;">
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
				qAndA: [],
				filteredQAndA: null,
			}
		},
		created () {
			for (let i = 0; i < 13 ; i++) {
				this.qAndA.push({
					question: this.t('Q' + (i + 1)),
					answer: this.t('A' + (i + 1)),
					tags: this.t('T' + (i + 1)),
					display: false,
				})
			}
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
				document.getElementById('searchFaq').blur()
			},
		} // methods
	} // export
</script>
<style scoped>
</style>
