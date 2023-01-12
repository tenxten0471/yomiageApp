<template>
	<div class="switch_root"  @click="enabled = !enabled">
		<input type="checkbox" v-model="enabled" />
		<div class="switch">
			<slot name="switch"/>
		</div>
		<div class="components">
			<slot name="components"/>
		</div>
		<div class="overlay"/>
	</div>
</template>

<script>
	export default {

		data(){
			return {
				enabled:false
			}
		},

		methods:{
			// toggle_enable(){
			// 	this.enabled = !this.enabled
			// 	console.log('enable')
			// },
		},
        
		props: {
		}

	}
</script>

<style scoped>
input{
	display: none;
}
.switch_root{
	display: flex;
	flex-direction: column;
	justify-content: left;
}
.switch{
	display: flex;
	position: relative;
	top: 0;left: 0;
	z-index: 2;
}
.components{
	visibility: collapse;
	display: flex;
	flex-direction: column;
	justify-content: left;
	z-index: 3;
	top:-500px;left: 0;
	filter:drop-shadow(10px 10px 10px #00000040);
	transition: 0.5s;
	position:absolute;
}
input:checked ~ .components{
	visibility: visible;
	position:relative;
	top:0;left: 0;
	/* top: 100;left: 0; */
}
.overlay{
	position: fixed;
	top: 0;left: 0;
	/* width: 0%;
	height: 0%; */
	transition: 0.5s;
}
input:checked ~ .overlay{
	/* display: block; */
	position: fixed;
	z-index: 1;
	width: 100%;
	height: 100%;
	background: #88888800;
	backdrop-filter: blur(5px);
}
</style>