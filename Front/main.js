import Vue from 'vue'
import App from './App'

Vue.config.productionTip = false

Vue.prototype.$host = 'http://127.0.0.1:5000';
//Vue.prototype.$host = 'https://www.luobodazahui.top';

App.mpType = 'app'

const app = new Vue({
    ...App
})
app.$mount()
