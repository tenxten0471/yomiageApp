<template>
    <div>
		<button class="cp_button02" @click="click">{{button_text}}</button>
    </div>
</template>

<script>
	export default {

		data(){
			return {
			}
		},

		methods:{
		},
        
		props: {
			click:{type:Function,default:function(){console.log('click!')}},
			button_text:{type:String,default:"+"}
		}

	}
</script>

<style scoped>
.cp_button02 {
	
	width:100%;
	height: 100%;
	line-height: 1.4em;
	cursor: pointer;
	user-select: none;
	transition: box-shadow 0.2s, transform 0.2s;
	color: #ec407a;
	border-width: 0;
	border-style: solid;
	border-radius: 20px;
	background: #ffffff;
	box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1);
}
.cp_button02:hover {
	-webkit-transform: scale(1.02);
	        transform: scale(1.02);
	box-shadow: 0 1px 6px 1px rgba(0, 0, 0, 0.2);
	color: #ec407a;
}
.cp_button02:active {
	transition-duration: 0.05s;
	-webkit-transform: scale(0.99);
	        transform: scale(0.99);
	box-shadow: 0 2px 3px 1px rgba(0, 0, 0, 0.15) inset;
}
.cp_button02:focus,
.cp_button02:focus:hover {
	color: #ec407a;
}
</style>