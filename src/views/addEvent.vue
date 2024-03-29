<template>
	<div class="main" style="overflow-y: scroll;">
		<div style="font-size: 36px;">{{ t('ADD EVENT') }}</div>

		<div class="line-height"/>

		<div style="display: flex; flex-direction: column; align-items: center; width: 80%;">
			<form v-on:keyup.enter="login()" v-if="isAdmin">
				<div style="padding-bottom: 5px;">
					<input :placeholder="t('EVENT NAME')" v-model="name" type="text"
							autocapitalize="words" autocomplete="off"/>
				</div>
				<div class="dual-set" style="padding-bottom: 5px;">
					<button class="button" style="width: 100%" v-on:click.prevent="is_private=!is_private">
						{{ t('PRIVATE EVENT?') }}
					</button>
					<input type="checkbox" class="checkbox" v-model="is_private"/><!--wanna put a little i in a cirle for info about what a private event means vs public-->
				</div>
				<div>
					<textarea :placeholder="t('DESCRIPTION')" v-model="description" type="text"
							autocapitalize="sentences" style="height: 60px" autocomplete="off"/>
				</div>
				<div style="padding-bottom: 5px;">
					<input :placeholder="t('ADDRESS')" v-model="address" type="text" autocorrect="none"
							autocapitalize="words" autocomplete="off"/>
				</div>
				<div style="padding-bottom: 5px;">
					<input :placeholder="t('VENUE NAME')" v-model="venue_name" type="text" autocorrect="none"
							autocapitalize="words" autocomplete="off"/>
				</div>
				<div style="padding-bottom: 5px; width: 100%; display: flex; flex-direction: row;">
					<div :style="[include_time ? {width: '50%'} : {width: '100%'}]">
						<input v-model="date" type="date" autocomplete="off"
								style="width: 100%; height: 30px; font: inherit; font-size: 11px;"/>
					</div>
					<div v-if="include_time" style="width: 50%">
						<input v-model="time" type="time" autocomplete="off" 
								style="width: 100%; height: 30px; font: inherit; font-size: 11px;">
					</div>
				</div>
				<div class="dual-set" style="padding-bottom: 5px;">
					<button class="button" style="width: 100%" v-on:click.prevent="include_time=!include_time">
						{{ t('INCLUDE TIME?') }}
					</button>
					<input type="checkbox" class="checkbox" v-model="include_time"/>
				</div>
				<div class="file-input">
					<div>
						{{ t('IMAGE') }}
					</div>
					<input type="file" accept="image/*" @change="(e) => {imageFile = e.target.files[0]}"/>
				</div>
				<div style="padding-top: 5px;">
					<button class="button" v-on:click.prevent="createEvent()">
						<div style="font-size: 18px;">{{ t('ADD') }}</div>
					</button>
				</div>
			</form>
			<div style="color: grey; display: flex; flex-direction: column; align-items: center" v-else>
				<div>({{ t('COMING SOON') }})</div>
				<div><small>{{ t('CURRENTLY, ONLY ADMINS CAN CREATE EVENTS. THIS FEATURE WILL BECOME OPEN TO THE PUBLIC SOON!') }}</small></div>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import translations from '@/functions/translations.js'
	import api from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'addEvent',
		components: {
		},
		data () {
			return {
				store: store,
				showAddEventModal: false,
				imageFile: null,
				name: '',
				description: '',
				address: '',
				venue_name: '',
				date: null,
				time: null,
				date_time: null,
				include_time: false,
				is_private: true,
				imageId: null,
				eventData: null,
			}
		},
		computed: {
			isAdmin () {
				return f.isAdmin
			},
		},
		watch: {
			'date' () {
				let date_time = new Date(this.date + 'T' + this.time)
				this.date_time = new Date(date_time.setHours(date_time.getHours() + 9))
			},
			'time' () {
				let date_time = new Date(this.date + 'T' + this.time)
				this.date_time = new Date(date_time.setHours(date_time.getHours() + 9))
			},
			async 'imageId' () {
				await this.finishCreateEvent()
			},
		},
		async mounted () {
			this.date_time = new Date()
			let year = (this.date_time.getYear() + 1900).toString()
			let month = (this.date_time.getMonth() + 1).toString()
			let day = (this.date_time.getDate()).toString()
			if (month.length < 2) {
				month = '0' + month
			}
			if (day.length < 2) {
				day = '0' + day
			}
			this.date = year + '-' + month + '-' + day
			this.time = '12:00'
		},
		methods: {
			t (w) { return translations.t(w) },
			async createEvent () {
				this.store.loading = true
				this.eventData = {
					name: this.name,
					description: this.description,
					address: this.address,
					venue_name: this.venue_name,
					date_time: this.date_time,
					include_time: this.include_time,
					is_private: this.is_private,
				}
				if (this.imageFile) {
					await this.saveImage()
				} else {
					await this.finishCreateEvent()
				}
				return
			},
			async saveImage () {
				let input = document.getElementById('img-input')
				let file = this.imageFile
				let blobURL = URL.createObjectURL(file)
				let img = new Image()
				img.src = blobURL
				img.onerror = () => {
					URL.revokeObjectURL(this.src)
					console.log('Cannot load image')
				}
				let vm = this
				this.imgId = img.onload = async () => {
					URL.revokeObjectURL(this.src)
					let width = img.width
					let height = img.height
					let maxWidth = 400
					let maxHeight = 400
					if (width > height) {
						if (width > maxWidth) {
							height = Math.round((height * maxWidth) / width)
							width = maxWidth
						}
					} else {
						if (height > maxHeight) {
							width = Math.round((width * maxHeight) / height)
							height = maxHeight
						}
					}
					let canvas = document.createElement('canvas')
					canvas.width = width
					canvas.height = height
					let ctx = canvas.getContext('2d')
					ctx.drawImage(img, 0, 0, width, height)
					let url = canvas.toDataURL('image/png', .7)
					let formData = new FormData()
					formData.append('data', url)
					let result = await api.saveImage(formData)
					vm.imageId = result.id
				}
			},
			async finishCreateEvent () {
				let data = this.eventData
				if (this.imageId) {
					data['images'] = this.imageId
				}
				let newEvent = await api.createEvent(data)
				console.log('newEvent', newEvent)
				await f.updateEvent(newEvent)
				f.goToPage({ page: 'event', args: { id: newEvent.id}})
				this.store.loading = false
			},
		} // methods
	} // export
</script>
<style scoped>
	.file-input {
		font-family: inherit;
		color: #18002e;
		-webkit-text-fill-color: #18002e;
		font-weight: inherit;
		font-size: inherit;
		border-radius: 15px;
		border: none;
		background-color: #ffe07a;
		box-shadow: 0 0 0 30px #ffe07a inset;
		-webkit-box-shadow: 0 0 0 30px #ffe07a inset;
		padding-top: 5px;
		padding-bottom: 5px;
		padding-left: 10px;
		padding-right: 10px;
		outline: none !important;
		width: 100%;
		height: 60px;
	}
	.button {
		width: 100%;
	}
	.dual-set {
		display: flex;
		flex-direction: row;
		align-self: center;
		align-items: center;
		justify-content: center;
		padding: 0;
		width: 100%;
	}
	.checkbox {
		position: fixed;
		height: 20px;
		width: 20px;
		transform: translate(90px, 0);
		flex-shrink: 0;
	}
</style>
