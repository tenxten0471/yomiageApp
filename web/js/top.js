const options = {
    moduleCache: {
      vue: Vue
    },
    async getFile(url) {
      
      const res = await fetch(url);
      if ( !res.ok )
        throw Object.assign(new Error(res.statusText + ' ' + url), { res });
      return {
        getContentData: asBinary => asBinary ? res.arrayBuffer() : res.text(),
      }
    },
    addStyle(textContent) {

      const style = Object.assign(document.createElement('style'), { textContent });
      const ref = document.head.getElementsByTagName('style')[0] || null;
      document.head.insertBefore(style, ref);
    },
  }
const { loadModule } = window['vue3-sfc-loader'];
console.log(location);
var app = {
    el: '#app',

    /* == data == リアクティブなデータを登録 */
    data(){
        return{
            searchtitle:'title',
            searchtext: '',
            colors:{
                bg : '#fefefeff',
                accent : '#ffffff'
            }
        };
    },
    methods:{
        search(e){
            eel.print()
        },
        add_data(){
            eel.add_data()
        }
    },
    /* ==== components ==== */
    // -- 単一ファイルコンポーネントの登録
    components: {
        'app_ui': Vue.defineAsyncComponent( () => loadModule("./js/components/main.vue", options) ),
    },

}


var text_update_func = function(x){}
eel.expose(text_update);
function text_update(x){
  text_update_func(x)
}
var target_url_update_func = function(){}
eel.expose(request_target_url_update);
function request_target_url_update(){
  target_url_update_func()
}


Vue.createApp(app).mount('#app')
