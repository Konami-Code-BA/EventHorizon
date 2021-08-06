<template>
	<div>
		<div style="width: 100%; height: 100%" v-show="selectedDate === 0">
			<div class="days">
				<button v-on:click.prevent="changeMonth(-1)" class="no-border-button">
					<
				</button>
				{{ selectedYear }} {{ t('month ' + selectedMonth) }}
				<button v-on:click.prevent="changeMonth(1)" class="no-border-button">
					>
				</button>
			</div>
			<div style="height: 87%">
				<div class="weeks"> 
					<div v-for="week in 6" style="margin-bottom: 5px;">
						<div class="days">
							<div v-for="day in 7">
								<div style="width: 22px; height: 22px;" class="day-individual">
									<button v-on:click.prevent="selectDate(
												getDateOfCalendarLocation((week - 1) * 7 + day - 1)
											)" class="no-border-button">
										<div :style="dayStyling(week, day)">
											{{ getDateOfCalendarLocation((week - 1) * 7 + day - 1).getDate() }}
										</div>
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div style="width: 100%; height: 100%" v-if="selectedDate != 0">
			<div class="days">
				<button v-on:click.prevent="selectedDate = 0" class="no-border-button" style="width: 80px">
					MONTH
				</button>
				<button v-on:click.prevent="changeDay(-1)" class="no-border-button">
					<
				</button>
				{{ selectedYear }}/{{ selectedMonth + 1 }}/{{ selectedDate.getDate() }}
				<button v-on:click.prevent="changeDay(1)" class="no-border-button">
					>
				</button>
				<div style="width: 80px"/>
			</div>
			<div style="height: 87%">
				<div v-if="dayHasEvent(selectedDate)">
					{{ selectedDate.getDate() }}
				</div>
				<div v-else>
					NO EVENTS
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	export default {
		name: 'eventsCalendar',
		data () {
			return {
				selectedMonth: 0,  // note: month goes from 0 to 11 (so dumb)
				selectedYear: 0,
				selectedDate: 0,
				eventDates: [],
				events: [],
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
			this.selectedYear = this.today.getYear() - 100 + 2000
			this.events = await apiFunctions.getAllEvents()
			for ( let i = 0; i < this.events.length; i++) {
				let date = new Date(this.events[i]['date_time'])
				let dateTime = new Date(
					date.getYear() - 100 + 2000, date.getMonth(), date.getDate(), 0, 0, 0, 0
				).getTime()
				this.eventDates.push(dateTime)
			}
		},
		methods: {
			t (w) { return translations.t(w) },
			getDateOfCalendarLocation (calendarLocation) {
				let today = this.today
				let dayOfWeekOfFirstOfMonth = new Date(
					this.selectedYear, this.selectedMonth, 1, 0, 0, 0, 0
				).getDay()
				let startOfMonth = new Date(
					this.selectedYear, this.selectedMonth, 1-dayOfWeekOfFirstOfMonth, 0, 0, 0, 0
				)
				return new Date(
					startOfMonth.getYear() - 100 + 2000, startOfMonth.getMonth(),
					startOfMonth.getDate() + calendarLocation, 0, 0, 0, 0
				)
			},
			changeMonth (change) {
				let date = new Date(this.selectedYear, this.selectedMonth + change, 1, 0, 0, 0, 0)
				this.selectedMonth = date.getMonth()
				this.selectedYear = date.getYear() - 100 + 2000
			},
			changeDay (change) {
				this.selectedDate = new Date(
					this.selectedDate.getYear() - 100 + 2000, this.selectedDate.getMonth(),
					this.selectedDate.getDate() + change, 0, 0, 0, 0
				)
			},
			dayHasEvent (date) {
				let dayTime = date.getTime()
				if (this.eventDates.includes(dayTime)) {
					return true
				} else {
					return false
				}
			},
			dayStyling (week, day) {
				let style = {}
				let calendarLocation = (week - 1) * 7 + day - 1
				let date = this.getDateOfCalendarLocation(calendarLocation)
				let dayDate = date.getDate()
				if ((
					week == 1 && dayDate > 7
				) || (
					week > 3 && dayDate <= 14
				)) {
					style['color'] = 'grey !important'
				} else if (!this.dayHasEvent(date)) {
					style['color'] = '#95c4ff !important'
					style['cursor'] = 'initial !important';
				} else {
					style['border-radius'] = '50%'
					style['background-color'] = '#5300e1'
					style['width'] = '22px'
					style['height'] = '22px'
				}
				return style		
			},
			selectDate (date) {
				if (this.dayHasEvent(date)) {
					this.selectedDate = date
				}
			},
		}
	}
</script>
<style scoped>
	.weeks {
		position: relative;
		width: 100%;
		display: flex;
		flex-direction: column;
		justify-content: space-around;
		height: 100%;
	}
	.days {
		position: relative;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-around;
	}
	.day-individual {
		display: flex;
		flex-direction: column;
		align-items: center !important;
	}
</style>