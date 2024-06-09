import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'
import App from './app.vue'
import store from './store'
import TinyVue from '@opentiny/vue'
import 'fullpage.js'
import VueFullpage from 'vue-fullpage.js'
import {
    Layout,
    Code,
    Title,
    Quote,
    Modal,
    Captcha,
    Dropdown,
    Password,
    Login,
    Register,
    Backtop,
    Anchor,
    Forget,
    Link,
    Menu,
    Notice,
    Search
} from '../src/index'

const app = createApp(App)
app.use(router)

const components = [
    Layout,
    Code,
    Title,
    Quote,
    Modal,
    Captcha,
    Dropdown,
    Password,
    Login,
    Register,
    Backtop,
    Anchor,
    Forget,
    Link,
    Menu,
    Notice,
    Search
]
components.forEach((component) => app.use(component))
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }
app.use(TinyVue)
app.use(ElementPlus)
app.use(store)
app.use(VueFullpage)
app.mount('#app')
