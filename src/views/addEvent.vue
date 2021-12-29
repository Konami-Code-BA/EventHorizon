<template>
	<div>
		<div class="main">
			<div style="font-size: 36px;">{{ t('ADD EVENT') }}</div>
			<div class="line-height"></div>
			<div style="display: flex; flex-direction: column; align-items: center; width: 80%;">
				<form v-on:keyup.enter="login()">
					<div style="padding-bottom: 5px;">
						<input :placeholder="t('EVENT NAME')" v-model="name" type="text"
								autocapitalize="words"/>
					</div>
					<div>
						<textarea :placeholder="t('DESCRIPTION')" v-model="description" type="text"
								autocapitalize="sentences"/>
					</div>
					<div style="padding-bottom: 5px;">
						<input :placeholder="t('ADDRESS')" v-model="address" type="text" autocorrect="none"
								autocapitalize="words"/>
					</div>
					<div style="padding-bottom: 5px;">
						<input :placeholder="t('VENUE NAME')" v-model="venue_name" type="text" autocorrect="none"
								autocapitalize="words"/>
					</div>
					<div style="display: flex; flex-direction: column; justify-content: center; height: 60px;">
						<div style="padding-bottom: 5px;">
							<input v-model="venue_name" type="date" style="width: 100%"/>
						</div>
						<div v-if="include_time" style="padding-bottom: 5px;">
							<input v-model="venue_name" type="time" style="width: 100%"/>
						</div>
					</div>
					<div class="dual-set" style="padding-bottom: 5px;">
						<button class="button" style="width: 100%" v-on:click.prevent="include_time=!include_time">
							Include time?&nbsp;
						</button>
						<input type="checkbox" class="checkbox" v-model="include_time"/>
					</div>
					<div class="file-input">
						<div>
							IMAGE
						</div>
						<input type="file" accept="image/*" @change="(e) => {imageFile = e.target.files[0]}"/>
					</div>
					<div style="padding-top: 5px;">
						<button class="button" v-on:click.prevent="createEvent()" :disabled="!isAdmin">
							<div style="font-size: 18px;">{{ t('ADD') }}</div>
						</button>
					</div>
				</form>
				<div style="color: grey" v-if="!isAdmin"><small>({{ t('COMING SOON') }})</small></div>
			</div>
		</div>
	</div>
</template>
<script>
	import store from '@/store.js'
	import modal from '@/components/modal.vue'
	import translations from '@/functions/translations.js'
	import apiFunctions from '@/functions/apiFunctions.js'
	import f from '@/functions/functions.js'
	export default {
		name: 'addEvent',
		components: {
			modal,
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
				date_time: new Date(),
				include_time: false,
				is_private: true,
			}
		},
		computed: {
			isAdmin () {
				return f.isAdmin
			},
		},
		watch: {
		},
		async mounted () {
			this.$emit('endLoading')
		},
		methods: {
			t (w) { return translations.t(w) },
			async createEvent () {
				let image_id = null
				if (this.imageFile) {
					image_id = await this.saveImage()
				}
				console.log(this.date_time, typeof this.date_time)
				await apiFunctions.createEvent({  // lets make this a form
					name: this.name,
					description: this.description,
					address: this.address,
					venue_name: this.venue_name,
					date_time: this.date_time,
					include_time: this.include_time,
					is_private: this.is_private,
					images: [image_id],
				})
			},
			async saveImage () {
				let formData = new FormData()
				formData.append('file', this.imageFile)
				let result = await apiFunctions.saveImage(formData)
				return result.id
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
		-webkit-box-shadow: 0 0 0 30px #ffe07a inset;
		padding-top: 5px;
		padding-bottom: 5px;
		padding-left: 10px;
		padding-right: 10px;
		outline: none !important;
		width: 100%;
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
		transform: translate(60px, 0)
	}
</style>
