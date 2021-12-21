<template>
	<div v-if="loaded">
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px; padding-top: 5px;"
				v-show="selectedDate === 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeMonth(-1)" class="button" style="padding-bottom: 1px;">
					{{'⇦'}}
				</button>
				<button v-on:click.prevent="goToToday()" class="button" style="width: 50px; font-size: 10px;">
					{{t('TODAY')}}
				</button>
				<div style="width: 100px; display: flex; justify-content: space-between;">
					<div>{{ selectedYear }}</div><div>{{ t('month ' + selectedMonth) }}</div>
				</div>
				<div style="width: 50px"/>
				<button v-on:click.prevent="changeMonth(1)" class="button" style="padding-bottom: 1px;">
					{{'⇨'}}
				</button>
			</div>
			<div style="height: 87%; display: flex; flex-direction: column; justify-content: center; align-items: center;">
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
				<div v-show="showNoEventsModal" :class="noEventsModalClass" class="no-events-modal">
					{{ t('NO EVENTS') }}
				</div>
			</div>
		</div>
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px" v-if="selectedDate != 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeDay(-1)" class="button" style="padding-bottom: 1px;">
					{{'⇦'}}
				</button>
				<button v-on:click.prevent="selectedDate = 0" class="button"
						style="width: 50px; font-size: 10px">
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
					<div style="width: 5px"/>
					<div style="width: 25px; text-align: center">
						{{ t('day ' + selectedDate.getDay()) }}
					</div>
				</div>
				<div style="width: 50px"/>
				<button v-on:click.prevent="changeDay(1)" class="button" style="padding-bottom: 1px;">
					{{'⇨'}}
				</button>
			</div>
			<div style="height: 87%">
				<ul v-if="getEventsFromDate(selectedDate).length > 0" style="list-style-type: none">
					<li v-for="event in getEventsFromDate(selectedDate)">
						<button v-on:click.prevent="$emit('openEventModal', event.id)" class="no-border-button">
							{{ event.name }}
						</button>
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
	export default {
		name: 'eventsCalendar',
		data () {
			return {
				selectedMonth: 0,  // note: month goes from 0 to 11 (so dumb)
				selectedYear: 0,
				selectedDate: 0,
				eventDates: {},
				loaded: false,
				showNoEventsModal: false,
				noEventsModalClass: null,
			}
		},
		components: {
		},
		props: {
			events: { default: null },
			store: { default: null },
			startingAt: { default: null },
		},
		computed: {
			today () {
				return new Date()
			},
		},
		watch: {
		},
		created () {
			this.selectedMonth = this.today.getMonth()  // note: month goes from 0 to 11 (so dumb)
			this.selectedYear = this.today.getYear() - 100 + 2000
			this.getAllEvents()
			this.loaded = true
		},
		methods: {
			t (w) { return translations.t(w) },
			getAllEvents () {
				for ( let i = 0; i < this.events.length; i++) {
					let dateTime = new Date(this.events[i].date_time)
					let date = new Date(
						dateTime.getYear() - 100 + 2000, dateTime.getMonth(), dateTime.getDate(), 0, 0, 0, 0
					).getTime()
					if (date in this.eventDates) {
						this.eventDates[date].push(this.events[i])
					} else {
						this.eventDates[date] = [this.events[i]]
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
				let date = new Date(
					startOfMonth.getYear() - 100 + 2000, startOfMonth.getMonth(),
					startOfMonth.getDate() + calendarLocation, 0, 0, 0, 0
				)
				return date
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
				if (dayTime in this.eventDates) {
					return this.eventDates[dayTime]
				} else {
					return []
				}
			},
			dayStyling (week, day) {
				let style = {
					'display': 'flex',
					'flex-diretion': 'column',
					'justify-content': 'center',
					'align-items': 'center'
				}
				let calendarLocation = (week - 1) * 7 + day - 1
				let date = this.getDateOfCalendarLocation(calendarLocation)
				let dayDate = date.getDate()
				if (date.toString().split(' ').slice(0, 4).toString() === this.today.toString().split(' ').slice(0, 4).toString()) {
					style['border-radius'] = '50%'
					style['border'] = '2px solid #95c4ff'
					style['background-color'] = 'none'
					style['width'] = '27px'
					style['height'] = '27px'
				}
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
					style['width'] = '27px'
					style['height'] = '27px'
					style['border'] = '2px solid #ffe07a'
				}
				return style		
			},
			async selectDate (date) {
				if (this.getEventsFromDate(date).length > 0) {
					this.selectedDate = date
				} else {
					this.showNoEventsModal = true
					await new Promise(r => setTimeout(r, 700))  // .5 seconds
					this.noEventsModalClass = 'fade-out'
					await new Promise(r => setTimeout(r, 1000))  // 1 seconds
					this.showNoEventsModal = false
					this.noEventsModalClass = null
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
		justify-content: center;
	}
	.no-events-modal {
		position: fixed;
		color: white;
		font-size: 32px;
		background-color: rgba(0, 0, 0, .5);
	}
</style>