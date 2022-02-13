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
			<h2>Purpose</h2>
			<p>
				Getting people together is what life is all about, but man if it isn't a pain in the ass.
			</p>
			<p>
				We want to make it so you spend less time on the GETTING together and more time on the BEING together.
			</p>
			<p>
				Make events, invite friends, and sit back and relax.
			</p>
			<h2>History</h2>
			<p>
				Basically Mikey started working on this idea somewhere around Feb 16 2021.
			</p>
			<p>
				Stu was immediately brought in for moral support / advice / brainstorming / business planning.
			</p>
			<p>
				Louis joined Feb 1 2022, he and Stu helped out finishing up the site before the launch, 
				and now the team is us three.
			</p>
			<p>
				The initial launch date was Feb 15 2022, officially less than 1 year after conception.
			</p>
			<h2>Hopes and dreams</h2>
			<p>
				Literally everything that happens is an event. The big bang was an event. T
			</p>
			<p>
				We think the potential for Event Horizon could be a lot more than parties.
			</p>
			<p>
				And we intend to find out just how far we can take it.
			</p>
			<img src="@/assets/eventhorizonLogo.png" style="width: 100%; margin-bottom: 50px;"/>
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
