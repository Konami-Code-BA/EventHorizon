<template>
	<div v-if="loaded">
		<!--month view-->
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px; padding-top: 5px;"
				v-show="selectedDate === 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeMonth(-1)" class="button" style="padding-bottom: 1px; width: auto;">
					<img src="@/assets/leftArrowIcon.png" style="width: 12px;"/>
				</button>
				<button v-on:click.prevent="goToToday()" class="button" style="width: 45px; font-size: 10px;">
					{{t('TODAY')}}
				</button>
				<div style="width: 125px; display: flex; justify-content: space-around;">
					<div>{{ selectedYear }}</div><div>{{ t('month ' + selectedMonth) }}</div>
				</div>
				<div style="width: 45px"/>
				<button v-on:click.prevent="changeMonth(1)" class="button" style="padding-bottom: 1px; width: auto;">
					<img src="@/assets/rightArrowIcon.png" style="width: 12px;"/>
				</button>
			</div>
			<!-- day labels -->
				<div style="width: 100%; padding-top: 20px; display: flex; flex-diretion: row; justify-content: space-around">
					<div v-for="week in 7" style="margin-bottom: 5px;">
						<div>{{ t('day ' + (week)) }}</div>
					</div>
				</div>
			<div style="height: 87%; display: flex; flex-direction: column; justify-content: center;
					align-items: center;">
				<div class="weeks">
					<div v-for="week in 6" style="margin-bottom: 5px;">
						<div class="days">
							<div v-for="day in 7" style="width: 100%; height: 100%;">
								<div style="width: 100%; height: 100%;" class="day-individual">
									<button v-on:click.prevent="selectDate(
												getDateOfCalendarLocation((week - 1) * 7 + day - 1)
											)" class="no-border-button" style="height: 100%">
										<div :style="dayStyling(week, day)" style="height: 100%">
											{{ getDateOfCalendarLocation((week - 1) * 7 + day - 1).getDate() }}
										</div>
									</button>
								</div>
							</div>
						</div>
					</div>
				</div>
				<flash-modal :text="t('NO EVENTS')" ref="flashNoEvents"/>
			</div>
		</div>
		<!--day view-->
		<div style="width: 100%; height: 100%; padding-left: 5px; padding-right: 5px; padding-top: 5px;"
				v-if="selectedDate != 0">
			<div style="width: 100%; display: flex; flex-direction: row; align-items: center;
					justify-content: space-between">
				<button v-on:click.prevent="changeDay(-1)" class="button" style="padding-bottom: 1px; width: auto;">
					<img src="@/assets/leftArrowIcon.png" style="width: 12px;"/>
				</button>
				<button v-on:click.prevent="selectedDate = 0" class="button"
						style="width: 45px; font-size: 10px; justify-self: flex-start">
					{{t('MONTH VIEW')}}
				</button>
				<div style="display: flex; flex-direction: row; align-items: center; justify-content: space-between;
						width: 125px;">
					<div style="display: flex; flex-direction: row; align-items: center;">
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
					</div>
					<div>
						<div style="width: 20px; text-align: center;">
							{{ t('day ' + selectedDate.getDay()) }}
						</div>
					</div>
				</div>
				<div style="width: 45px"/>
				<button v-on:click.prevent="changeDay(1)" class="button" style="padding-bottom: 1px; width: auto;">
					<img src="@/assets/rightArrowIcon.png" style="width: 12px;"/>
				</button>
			</div>
			<div style="height: 90%">
				<div style="width: 100%; overflow-y: scroll; overflow-x: hidden; display: flex; flex-direction: column;
						align-items: center; padding-left: 10px; height: 100%;" id="scroller">
					<div style="width: 90%;">
						<div class="list" v-if="getEventsFromDate(selectedDate).length > 0">
							<div v-for="event in getEventsFromDate(selectedDate)"  class="event-card-item">
								<button v-on:click.prevent="openEventModal(event.id)" class="no-border-button" style="width: 100%; margin-top: 2px;">
									<event-block :event="event" style="width: 100%"/>
								</button>
							</div>
						</div>
						<div v-else style="font-size: 20px; text-align: center;">{{t('NO EVENTS')}}</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import f from '@/functions/functions.js'
	import eventBlock from '@/components/eventBlock.vue'
	import flashModal from '@/components/flashModal.vue'
	export default {
		name: 'eventsCalendar',
		components: {
			eventBlock,
			flashModal,
		},
		data () {
			return {
				store: store,
				selectedMonth: 0,  // note: month goes from 0 to 11 (so dumb)
				selectedYear: 0,
				selectedDate: 0,
				eventDates: {},
				loaded: false,
			}
		},
		created () {
			this.selectedMonth = f.today.getMonth()  // note: month goes from 0 to 11 (so dumb)
			this.selectedYear = f.today.getYear() - 100 + 2000
			this.getAllEvents()
			this.loaded = true
		},
		methods: {
			t (w) { return translations.t(w) },
			getAllEvents () {
				for ( let i = 0; i < this.store.events.display.length; i++) {
					let dateTime = new Date(this.store.events.display[i].date_time)
					dateTime = new Date(dateTime.setHours(dateTime.getHours()-9))
					let date = new Date(
						dateTime.getYear() - 100 + 2000, dateTime.getMonth(), dateTime.getDate(), 0, 0, 0, 0
					).getTime()
					console.log(dateTime.getDate(), this.store.events.display[i].name)
					if (date in this.eventDates) {
						this.eventDates[date].push(this.store.events.display[i])
					} else {
						this.eventDates[date] = [this.store.events.display[i]]
					}
				}
			},
			getDateOfCalendarLocation (calendarLocation) {
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
				let style = {  // changed this after mac fix. check this is still ok
					'display': 'flex',
					'flex-diretion': 'column',
					'justify-content': 'center',
					'align-items': 'center',
          'height':'34px',
          'width':'34px'
				}
				let calendarLocation = (week - 1) * 7 + day - 1
				let date = this.getDateOfCalendarLocation(calendarLocation)
				let dayDate = date.getDate()
				if (date.toString().split(' ').slice(0, 4).toString() === f.today.toString().split(' ').slice(0, 4).toString()) {
					style['border-radius'] = '4px'
					style['border'] = '2px solid #cae2ff'
					style['background-color'] = 'none'
				}
				if ((
					week == 1 && dayDate > 7
				) || (
					week > 3 && dayDate <= 14
				)) {
					style['color'] = 'grey !important'
				} else if (this.getEventsFromDate(date).length == 0) {
					style['color'] = '#cae2ff !important'
					style['cursor'] = 'initial !important';
				} else {
					style['border-radius'] = '4px'
					style['border'] = '2px solid #ffe07a'
				}
				return style
			},
			async selectDate (date) {
				if (this.getEventsFromDate(date).length > 0) {
					this.selectedDate = date
				} else {
					await this.$refs.flashNoEvents.flashModal()
				}
			},
			goToToday () {
				this.selectedMonth = f.today.getMonth()
				this.selectedYear = f.today.getYear() - 100 + 2000
			},
			openEventModal (id) {
				f.goToPage({ page: 'event', args: { id: id } })
			}
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
	.success-modal {
		position: fixed;
		color: white;
		font-size: 32px;
		background-color: rgba(0, 0, 0, .5);
	}
	.list {
		position: relative;
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		justify-content: flex-start;
		overflow-x: hidden;
		overflow-y: visible;
		width: 100%;
		height: 100%;
		padding-top: 10px;
	}
	.event-card-item {
		width:100%;
		margin: 6px auto;
    min-height: 50px;
	}
</style>
