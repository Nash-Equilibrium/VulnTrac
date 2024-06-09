import { type App, reactive } from 'vue'
import type { GlobalProperties } from './types'
import { __LOGO__ } from './images'

const MI_YEAR = new Date().getFullYear()
export const __MI_AUTHOR__ = 'VulnTrac'
export const __MI_POWERED__ = 'VulnTrac'
export const __MI_LOGO__ = __LOGO__
export const __MI_SITE__ = 'https://github.com/Nash-Equilibrium/VulnTrac'
export const __MI_SOCIALITE_DOMAIN__ = 'https://github.com/Nash-Equilibrium/VulnTrac'

/**
 * 全局变量 - ( `this.$g` )
 * @param title 文档标题
 * @param site 站点名称
 * @param author 作者
 * @param powered 提供方
 * @param keywords 关键词
 * @param description 描述
 * @param prefix 前缀
 * @param salt 加密盐值
 * @param separator 加密字符串的分隔符
 * @param apiVersion API 版本
 * @param emptyFormatter 空串格式化的字符串
 * @param theme 主题配置属性
 * @param copyright 版权所有
 * @param protocols URL 校验协议数组
 * @param regExp 常用正则
 * @param caches 缓存 key 值
 * @param menus 菜单
 */
export const $g = reactive({
    title: 'VulnTrac',
    site: 'VulnTrac',
    author: __MI_AUTHOR__,
    powered: __MI_POWERED__,
    logo: __MI_LOGO__,
    locale: `zh-cn`,
    keywords: '',
    description: 'test',
    prefix: 'mi-',
    salt: 'mi-ZBmnY3mojbXvijFf',
    separator: '/!#!$/',
    apiVersion: 'v1',
    emptyFormatter: '-',
    theme: {
        type: 'dark',
        primary: '#FFD464',
        radius: 6
    },
    copyright: {
        laptop: `${MI_YEAR} <a href="https://github.com/Nash-Equilibrium/VulnTrac" target="_blank">VulnTrac</a> All Rights Reserved. `,
        mobile: `${MI_YEAR} <a href="https://github.com/Nash-Equilibrium/VulnTrac" target="_blank">VulnTrac</a>`
    },
    protocols: ['https', 'http', 'ftp', 'mms', 'rtsp'],
    regExp: {
        phone: /^((0\d{2,3}-\d{7,8})|(1[3456789]\d{9}))$/,
        password: /^[A-Za-z0-9~!@#$%^&*()_+=\-.,]{6,32}$/,
        username: /^[a-zA-Z]{1}([a-zA-Z0-9]|[_]){3,15}$/,
        email: /^[A-Za-z0-9\.-_\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/,
        chinese: /^[\u4e00-\u9fa5]*$/,
        hex: /^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$/,
        rgb: /^(rgb|RGB)/
    },
    caches: {
        storages: {
            theme: {
                type: 'theme-type',
                hex: 'theme-color-hex'
            },
            user: 'user-info',
            email: 'user-email',
            locale: 'language-locale',
            collapsed: 'layout-menu-collapsed',
            languages: {
                custom: 'languages-custom',
                categories: 'languages-categories'
            },
            captcha: {
                login: 'login-captcha-key',
                register: 'register-captcha-key',
                email: 'email-captcha-key'
            },
            password: {
                reset: {
                    time: 'password-reset-code-sent-time',
                    token: 'password-reset-verify-token',
                    uid: 'password-reset-uid',
                    username: 'password-reset-username'
                }
            }
        },
        cookies: {
            autoLogin: 'auto-login',
            token: {
                access: 'access-token',
                refresh: 'refresh-token'
            }
        }
    },
    breakpoints: {
        xs: 480,
        sm: 576,
        md: 768,
        lg: 992,
        xm: 1024,
        xl: 1200,
        xxl: 1600,
        xxxl: 2000
    },
    winSize: {
        width: 0,
        height: 0
    }
}) as unknown as GlobalProperties

export default {
    install(app: App) {
        app.config.globalProperties.$g = $g
        return app
    }
}
