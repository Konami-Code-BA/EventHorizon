<template>
	<div>
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px" v-show="selectedDate === 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeMonth(-1)" class="no-border-button">
					{{'<'}}
				</button>
				<button v-on:click.prevent="goToToday()" class="no-border-button" style="width: 40px; font-size: 10px">
					{{t('TODAY')}}
				</button>
				{{ selectedYear }} {{ t('month ' + selectedMonth) }}
				<div style="width: 40px"/>
				<button v-on:click.prevent="changeMonth(1)" class="no-border-button">
					{{'>'}}
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
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px" v-if="selectedDate != 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeDay(-1)" class="no-border-button">
					{{'<'}}
				</button>
				<button v-on:click.prevent="selectedDate = 0" class="no-border-button"
						style="width: 40px; font-size: 10px">
					{{t('MONTH VIEW')}}
				</button>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: center">
					<div style="width: 40px; text-align: center">
						{{ selectedYear }}
					</div>
					/
					<div style="width: 20px; text-align: center">
						{{ selectedMonth + 1 }}
					</div>
					/
					<div style="width: 20px; text-align: center">
						{{ selectedDate.getDate() }}
					</div>
					&nbsp;
					<div style="width: 25px; text-align: center">
						{{ t('day ' + selectedDate.getDay()) }}
					</div>
				</div>
				<div style="width: 40px"/>
				<button v-on:click.prevent="changeDay(1)" class="no-border-button">
					{{'>'}}
				</button>
			</div>
			<div style="height: 87%">
				<ul v-if="getEventsFromDate(selectedDate).length > 0" style="list-style-type: none">
					<li v-for="event in getEventsFromDate(selectedDate)">
						{{ event['name'] }}
					</li>
				</ul>
				<ul v-else style="list-style-type: none">
					<li>
						{{t('NO EVENTS')}}
					</li>
				</ul>
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
				eventDates: {},
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
			await this.getAllEvents()
		},
		methods: {
			t (w) { return translations.t(w) },
			async getAllEvents () {
				this.events = await apiFunctions.getAllEvents()
				for ( let i = 0; i < this.events.length; i++) {
					let date = new Date(this.events[i]['date_time'])
					let dateTime = new Date(
						date.getYear() - 100 + 2000, date.getMonth(), date.getDate(), 0, 0, 0, 0
					).getTime()
					if (dateTime.toString() in this.eventDates) {
						this.eventDates[dateTime.toString()].push(this.events[i])
					} else {
						this.eventDates[dateTime.toString()] = [this.events[i]]
					}
				}
			},
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
				this.selectedMonth = this.selectedDate.getMonth()
				this.selectedYear = this.selectedDate.getYear() - 100 + 2000
			},
			getEventsFromDate (date) {
				let dayTime = date.getTime()
				if (dayTime.toString() in this.eventDates) {
					return this.eventDates[dayTime.toString()]
				} else {
					return []
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
				} else if (this.getEventsFromDate(date).length == 0) {
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
				if (this.getEventsFromDate(date).length > 0) {
					this.selectedDate = date
				}
			},
			goToToday () {
				this.selectedMonth = this.today.getMonth()
				this.selectedYear = this.today.getYear() - 100 + 2000
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