<template>
	<div class="main" style="overflow-y: scroll;">
		<div style="font-size: 36px;">ABOUT US</div>
		<div style="width: 80%; display: flex; flex-direction: column; align-items: flex-start;">
			<img src="@/assets/bandPic.png" style="width: 100%;"/>
			<div style="align-self: center; display: flex; flex-direction: row; justify-content: space-around;
					width: 100%;">
				<small>Mikey</small>
				<small>Louis</small>
				<small>Stu</small>
			</div>
			<h2>{{t('purpose')}}</h2>
			<p>
				{{t('purpose1')}}
			</p>
			<p>
				{{t('purpose2')}}
			</p>
			<p>
				{{t('purpose3')}}
			</p>
			<h2>{{t('history')}}</h2>
			<p>
				{{t('history1')}}
			</p>
			<p>
				{{t('history2')}}
			</p>
			<p>
				{{t('history3')}}
			</p>
			<p>
				{{t('history4')}}
			</p>
			<h2>{{t('hopes and dreams')}}</h2>
			<p>
				{{t('hopes and dreams1')}}
			</p>
			<p>
				{{t('hopes and dreams2')}}
			</p>
			<p>
				{{t('hopes and dreams3')}}
			</p>
			<img src="@/assets/eventhorizonLogo.png" style="width: 100%; max-width: 300px; margin-bottom: 50px;"/>
		</div>
	</div>
	
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'aboutUs',
		data () {
			return {
			}
		},
		mounted () {
		},
		methods: {
			t (w) { return translations.t(w) },
		} // methods
	} // export
</script>
<style scoped>
	p {
		margin: 5px;
	}
</style>
