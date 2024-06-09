import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import EslintPlugin from 'vite-plugin-eslint'
import path from 'path'
// eslint-disable-next-line import/no-unresolved
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite'
import autoImportPlugin from '@opentiny/unplugin-tiny-vue'
const resolve = (dir: string) => path.join(__dirname, dir)

// https://vitejs.dev/config/
export default defineConfig({
    define: {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true',
        'process.env': { ...process.env }
    },
    resolve: {
        alias: {
            '@': resolve('example'),
            '@miitvip/admin-pro': resolve('src/index')
        }
    },
    css: {
        devSourcemap: true,
        modules: { generateScopedName: 'mi-[name]-[hash:base64:8]', localsConvention: 'camelCase' },
        preprocessorOptions: { less: { javascriptEnabled: true } }
    },
    optimizeDeps: {
        include: [
            'vue',
            'vue-router',
            'ant-design-vue',
            'axios',
            'nprogress',
            'vue-i18n',
            '@ant-design/icons-vue',
            'pinia',
            'md5',
            'prismjs',
            'style-inject',
            'vue-types',
            'swiper/element/bundle',
            'swiper/modules',
            'swiper/css/*',
            '@material/material-color-utilities',
            'vue3-touch-events',
            'vue3-colorpicker'
        ]
    },
    server: {
        host: '0.0.0.0',
        port: 5800,
        proxy: {
            '/v1': {
                target: 'http://localhost',
                changeOrigin: true
            },
            '/api/trans': {
                target: 'http://fanyi-api.baidu.com',
                changeOrigin: true
            }
        }
    },
    plugins: [
        vue({
            template: {
                compilerOptions: {
                    isCustomElement: (tag: string) => tag.startsWith('swiper-')
                }
            }
        }),
        vueJsx({
            isCustomElement: (tag: string) => tag.startsWith('swiper-')
        }),
        EslintPlugin(),
        VueI18nPlugin({ include: resolve('./src/locales') }),
        [autoImportPlugin('vite')]
    ],
    esbuild: { jsxFactory: 'h', jsxFragment: 'Fragment' }
})
