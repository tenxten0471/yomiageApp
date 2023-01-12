

<template>
    <div class="root" >

		<div class="content" v-if="!is_play">
			<br/>
			<a>YomiageApp</a>
			<br/>
			<div class="form">
				<p>url　:　 </p>
				<input type="url" id="url" v-model="target_url" @input="set_url">
			</div>

			<div class="form">
				<p>text selector　:　</p>
				<input type="text" id="text_selectors" v-model="text_selector">
				<floating_button class="form_button" button_text="set" @click="set_texts_selector"></floating_button>
			</div>

			<div class="preview">
				{{ text_example ? "preview\n"+text_example : '' }}
			</div>

			<div class="form">
				<p>next url selector　:　</p>
				<input type="text" id="next_selector" v-model="next_url_selector">
				<floating_button class="form_button" button_text="set" @click="set_next_url_selector"></floating_button>
			</div>

			<div class="preview">
				{{ next_url.length ? "preview\n"+next_url : '' }}
			</div>

			<div class="form">
				<p>setting　:　</p>
				<div class="content">
					<p>auto_next</p>
					<input type="checkbox" v-model="setting['auto_next']" @change="set_setting"/>
				</div>
				<div class="content">
					<p>volume</p>
					<input type="range" min="0" max="1" step="0.01" v-model="setting['volume_rate']" @change="set_volume_rate"/>
				</div>
				<div class="content">
					<p>speaker</p>
					<!-- <input type="number" v-model="setting['speaker_id']" @change="set_setting"/> -->
					<select v-model="setting['speaker_id']" @change="set_setting">
						<option v-for="v,k in speaker_data" v-if="v != speaker_id" :value="v">{{ k }}</option>
					</select>
				</div>
				
			</div>

			<floating_button class="play_button" button_text="play▷" @click="play"></floating_button>
			<!-- <div class="pause"></div> -->
		</div>

		<div class="content" v-if="is_play">
			<!-- <div class="inplay"></div> -->
			<div class="finish_button" @click="finish">{{ " < " }}</div>
			<br/>
			<a>{{ target_url }}</a>
			<br/>
			<div class="content" v-for="text in playing_texts['prev_texts']">
				<div class="text_card prev_texts">
					{{ text }}
				</div>
			</div>
			<div id="playing_text" class="text_card">
				{{ playing_texts['playing_text'] }}
			</div>
			<div class="content" v-for="text in playing_texts['next_texts']">
				<div class="text_card next_texts">
					{{ text }}
				</div>
			</div>
			<div class="content" v-for="text in playing_texts['pre_texts']">
				<div class="text_card pre_texts">
					{{ text }}
				</div>
			</div>
			
			<div class="player_controller">
				<floating_button button_text="❙◁" @click="to_prev"></floating_button>
				<floating_button v-if="is_pause" button_text="▷" @click="toggle_pause"></floating_button>
				<floating_button v-if="!is_pause" button_text="❙❙" @click="toggle_pause"></floating_button>
				<floating_button button_text="▷❙" @click="to_next"></floating_button>
				<div class="left">
					<input type="range" min="0" max="1" step="0.01" v-model="setting['volume_rate']" @change="set_volume_rate" title="volume"/>
					<input type="checkbox" v-model="setting['auto_next']" @change="set_setting" title="auto_next"/>
				</div>
				
				<floating_button class="right" button_text="nextpage >" @click="to_next_page"></floating_button>
			</div>

		</div>
		
		
    </div>
</template>

<script>
  	import floating_button from "./floating_button.vue";
	export default {

		data(){
			return {
				speaker_id:0,
				target_url:'',
				text_selector:'',
				text_example:'',
				next_url_selector:'',
				next_url:[],
				urls:{},
				is_play:false,
				playing_texts:{
					'prev_texts':[],
					'playing_text':'get voice...',
					'next_texts':[],
					'pre_texts':[],
				},
				is_pause:false,
				// auto_next:true,
				// volume_rate:1,
				setting:{
					'auto_next':true,
					'volume_rate':1,
					'speaker_id':0
				},
				speaker_data:{},
			}
		},

		methods:{
			print(data='notdata'){
				console.log(data);
				eel.print_eel(data)
			},
			play(){
				eel.yomiage_url_eel()
				this.is_play=true
				eel.set_is_play(this.is_play)()
			},
			toggle_pause(){
				eel.toggle_pause()
				this.is_pause = !this.is_pause
				eel.set_is_pause(this.is_pause)()
			},
			to_next(){
				eel.to_next()()
			},
			to_prev(){
				eel.to_prev()()
			},
			to_next_page(){
				eel.to_next_page()()
			},
			finish(){
				eel.finish()()
				this.is_play=false
				eel.set_is_play(this.is_play)()
			},
			sleep: time => new Promise(resolve => setTimeout(resolve, time)),
			async text_update(playing_texts){
				this.playing_texts = playing_texts
				await this.sleep(100)
				var scroll_target =  document.getElementById('playing_text')
				var rect = scroll_target.getBoundingClientRect()
				scrollBy(0,rect.top-(window.innerHeight*0.15))

			},
			async set_url(){
				var selectors=await eel.set_url(this.target_url)()
				this.print(selectors)
				this.text_selector=selectors['get_texts']
				this.next_url_selector=selectors['get_next_url']
			},
			set_texts_selector(){
				eel.set_texts_selector(this.text_selector)()
				this.preview_text()
			},
			set_next_url_selector(){
				eel.set_next_url_selector(this.next_url_selector)()
				this.preview_next_url()
			},
			async preview_text(){
				this.text_example = await eel.text_example()()
			},
			async preview_next_url(){
				this.next_url = await eel.next_url_example()()
				this.print(this.next_url)
			},
			async get_is_play(){
				this.is_play = await eel.get_is_play()()
			},
			async get_is_pause(){
				this.is_pause = await eel.get_is_pause()()
			},
			async get_url(){
				this.target_url = await eel.get_url()()
				this.set_url()
			},
			// async get_auto_next(){
			// 	this.auto_next = await eel.get_auto_next()()
			// 	this.print(this.auto_next)
			// },
			// toggle_auto_next(){
			// 	this.auto_next = !this.auto_next
			// 	this.set
			// },
			async get_setting(){
				this.setting = await eel.get_setting()()
				this.print(this.setting)
			},
			set_setting(){
				eel.set_setting(this.setting)()
				this.print(this.setting)
			},
			// async get_volume_rate(){
			// 	this.volume_rate = await eel.get_volume_rate()()
			// },
			set_volume_rate(){
				eel.set_volume_rate(this.setting['volume_rate'])()
				this.print(this.setting['volume_rate'])
			},
			async get_speakers(){
				this.speaker_data = await eel.get_speakers()()
				this.print(this.speaker_data)
			},

		},
        
		computed: {
		},
		props: {
			items_init:{type:Array,default:[]},
			colors: {type:Object,default:{
				accent : '#da3c41'
			}},
		},
		components: {
			floating_button,

		},
		mounted(){
			text_update_func = this.text_update
			target_url_update_func = this.get_url
			this.get_is_play()
			this.get_is_pause()
			this.get_url()
			this.get_setting()
			this.get_speakers()
			// this.get_auto_next()
			// this.get_volume_rate()
			this.is_play ? eel.request_text_update()():0
		},
		watch:{
		},

	}
</script>
<style scoped>
/* html	{
} */
.root{
	content: "";
	position: absolute;
	top: 0;left: 0;
	width: 100%;
	min-height: 100%;
	background: #f8f8fa;
	/* font-size: 5.46875%; */
}
.root > .content{
	padding-bottom: 30vh;
}
.content{
	display: flex;
	flex-direction: column;
	align-items: center;
	width: 100%;
	/* padding-bottom: 30vh; */
}
.content > *{
	margin: 10px;
}
.form{
	display: flex;
	align-items: center;
	border-radius: 5px;
	max-width: 80%;
	width: 800px;
	padding: 10px;
	filter:drop-shadow(10px 10px 10px #00000040);
	background-color: #ffffff;

}
.form > input{
	border: 0px;
	width: 100%;
	padding: 20px;
	background-color: transparent;
}
.form > input:focus{
  	outline: none;
}
.form > input:hover{
    border-left: 3px solid #00000044;
}
.form_button{
	width: 40px;
	height: 40px;
}
.preview{
	max-width: 80%;
	width: 800px;
}
.play_button{
	font-size: 50px;
	width: 20%;
	height: 40px;
}
.text_card{
	display: block;
	background-color: #ffffffff;
	color: #000000CC;
	position: relative;
	z-index: 1;
	border-radius: 5px;
	max-width: 80%;
	width: 800px;
	padding: 20px;
	margin: 5px;
	white-space: pre-line;
	filter:drop-shadow(10px 10px 10px #00000040);
	backdrop-filter: blur(20px);
}
.prev_texts, .next_texts{
	/* background-color: #ffffff99; */
	z-index: 0;
	filter:drop-shadow(10px 10px 10px #00000000);
}
.pre_texts{
	color: #00000044;
	/* background-color: #ffffff99; */
	z-index: 0;
	filter:drop-shadow(10px 10px 10px #00000000);
}
.player_controller{
	position: fixed;
	bottom: 0px;
	left:0px;
	z-index: 1;

	display: flex;
	justify-content: center;
	align-items: center;

	width:100%;
	height: 50px;
	margin: 0px;

	background-color: #070e18d3;
	/* backdrop-filter: blur(12px); */
}
.player_controller > *{
	display: flex;
	align-items: center;
	min-width: 40px;
	min-height: 40px;
	margin: 5px;
}
.player_controller > .right{
	position: absolute;
	right: 10px;
	/* float: right; */
}
.player_controller > .left{
	position: absolute;
	left: 10px;
	/* float: right; */
}
.player_controller *{
	font-size: 30px;
}
.finish_button{
	display: flex;
	align-items: center;
	position:fixed;
	top: 0px;
	left: 0px;
	z-index: 1;
    -webkit-box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0);
            box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0);
	
	padding: 15px;
	margin: 10px;
	backdrop-filter: blur(20px);
}
.finish_button:hover{
    -webkit-box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.5);
            box-shadow: 1px 3px 7px -3px rgba(0, 0, 0, 0.5);
}
.inplay::before {
	content: "";
	opacity: v-bind(is_pause ? 0.05 : 0.2);
	transition: opacity 0.5s;
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;height: 100%;
	background: linear-gradient(-45deg, #ff00bf, #005eff, #b6ffc8,#ff00bf, #005eff,  #ffe5b9) fixed;
	background-size: 800% 800%;
	animation: GradietionAnimation 15s ease infinite;
}

@keyframes GradietionAnimation { 
	0%{background-position:0% 50%}
	50%{background-position:100% 50%}
	100%{background-position:0% 50%}
}
</style>