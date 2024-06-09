<template>
    <mi-theme>
        <mi-layout />
    </mi-theme>
</template>

<script lang="ts" setup>
import { DashboardOutlined, ThunderboltOutlined, CrownOutlined, SisternodeOutlined, GlobalOutlined, SendOutlined, SaveOutlined, ToolOutlined, SnippetsOutlined, LoginOutlined, ScheduleOutlined, QuestionCircleOutlined, AppstoreAddOutlined, FireFilled, LayoutOutlined, BellOutlined, SwitcherOutlined, ScanOutlined, LikeFilled, SearchOutlined, ClockCircleOutlined, SafetyCertificateOutlined, BorderlessTableOutlined, OrderedListOutlined, MenuOutlined, CodeOutlined, InfoCircleOutlined, ExclamationCircleOutlined, HighlightOutlined, VerticalAlignTopOutlined, GithubOutlined, WarningOutlined, AlignCenterOutlined, ToTopOutlined, PicRightOutlined, SecurityScanOutlined, TransactionOutlined } from '@ant-design/icons-vue'
import { useStoreMenu, useStoreSearch } from '../../src/index'

// update menus
const menuStore = useStoreMenu()
const searchStore = useStoreSearch()
menuStore.updateMenus([
    {
        name: 'about',
        path: '/about',
        meta: {
            title: '关于我们',
            subTitle: '什么是VulnTrac',
            icon: InfoCircleOutlined
        }
    },
    {
        name: 'dashboard',
        path: '/dashboard',
        meta: {
            title: '用户中心',
            subTitle: '查看个人主页',
            icon: DashboardOutlined,
            // tag: {color: '#f50', content: 'Hot'}
        }
    },
    {
        name: 'start',
        path: '/start',
        meta: {
            title: '检测中心',
            subTitle: '快速开始检测',
            icon: ThunderboltOutlined
        }
    },
    {
        name: 'repos',
        path: '/repos',
        meta: {
            title: '仓库管理',
            subTitle: '查看并配置仓库',
            icon: SisternodeOutlined
        },
        children: [{
            name: 'repos-setup',
            path: '/repos/setup',
            meta: {
                title: '监测设置',
                subTitle: '管理仓库监测',
                icon: ToolOutlined
            }
        }, {
            name: 'repos-history',
            path: '/repos/history',
            meta: {
                title: '监测历史',
                subTitle: '仓库监测历史',
                icon: GlobalOutlined
            }
        }]
    },
    {
        name: 'pages',
        path: '/pages',
        meta: {
            title: '检测管理',
            subTitle: '查看或配置检测',
            icon: SnippetsOutlined
        },
        children: [{
            name: 'pages-history',
            path: '/pages/history',
            meta: {
                title: '检测记录',
                subTitle: '查看检测记录',
                icon: ScheduleOutlined
            }

        }]
    }
])
searchStore.updateData([
    {
        title: `关于我们`,
        summary: '介绍',
        icon: ExclamationCircleOutlined,
        path: '/about'
    },
    {
        title: `用户中心`,
        summary: `纵观全局 · 运筹帷幄`,
        icon: DashboardOutlined,
        path: '/dashboard'
    },
    {
        title: `检测中心`,
        summary: `一目十行 · 滴水成冰`,
        icon: ThunderboltOutlined,
        path: '/start'
    },
    {
        title: `监测设置`,
        summary: `以一驭万 · 顾全大局`,
        icon: GlobalOutlined,
        path: '/repos/setup'
    },
    {
        title: `监测历史`,
        summary: `为民请命 · 响应风从`,
        icon: SendOutlined,
        path: '/repos/history'
    },
    {
        title: `登录页面`,
        summary: `先发制人 · 先声夺人`,
        icon: LoginOutlined,
        path: '/pages/login'
    },
    {
        title: `注册页面`,
        summary: `欣欣向荣 · 马到成功`,
        icon: ScheduleOutlined,
        path: '/pages/register'
    },
    {
        title: `忘记密码`,
        summary: `吃水忘源 · 得新忘旧`,
        icon: QuestionCircleOutlined,
        path: '/pages/forget'
    }
])
</script>