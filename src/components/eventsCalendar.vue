<template>
	<div>
		<div class="days">
			<button v-on:click.prevent="changeMonth (-1)" class="no-border-button">
				<
			</button>
			{{ selectedYear }} {{ t('month ' + selectedMonth) }}
			<button v-on:click.prevent="changeMonth (1)" class="no-border-button">
				>
			</button>
		</div>
		<div class="weeks"> 
			<div v-for="week in 6">
				<div class="days">
					<div v-for="day in 7">
						<div style="width: 20px;"
								:style="[(
									week == 1 && days((week - 1) * 7 + day - 1) > 7
								) || (
									week > 3 && days((week - 1) * 7 + day - 1) <= 14
								) ? {
									color: '#4b4b4b'
								} : {}]">
							{{ days((week - 1) * 7 + day - 1) }}
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	export default {
		name: 'eventsCalendar',
		data () {
			return {
				selectedMonth: 0,  // note: month goes from 0 to 11 (so dumb)
				selectedYear: 0,
			}
		},
		components: {
		},
		props: {
			tabNo: {},
		},
		computed: {
			today () {
				return new Date()
			},
		},
		watch: {
		},
		async mounted () {
			this.selectedMonth = this.today.getMonth()  // note: month goes from 0 to 11 (so dumb)
			this.selectedYear = this.today.getYear()-100+2000
		},
		methods: {
			t (w) { return translations.t(w) },
			days (calendarLocation) {
				let today = this.today
				let dayOfWeekOfFirstOfMonth = new Date(
					this.selectedYear, this.selectedMonth, 1, 0, 0, 0, 0
				).getDay()
				let startOfMonth = new Date(
					this.selectedYear, this.selectedMonth, 1-dayOfWeekOfFirstOfMonth, 0, 0, 0, 0
				)
				return new Date(
					startOfMonth.getYear(), startOfMonth.getMonth(), startOfMonth.getDate() + calendarLocation, 0, 0, 0, 0
				).getDate()
			},
			changeMonth (change) {
				let date = new Date(this.selectedYear, this.selectedMonth + change, 1, 0, 0, 0, 0)
				this.selectedMonth = date.getMonth()
				this.selectedYear = date.getYear() - 100 + 2000
			}
		}
	}
</script>
<style scoped>
	.weeks {
		width: 100%;
		display: flex;
		flex-direction: column;
		height: 30px;
	}
	.days {
		display: flex;
		flex-direction: row;
		justify-content: space-around;
	}
</style>