<template>
    <el-dialog :visible.sync="visible" title="仓库详情" @close="handleClose">
      <div>
        <p><strong>名称:</strong> {{ repo?.name }}</p>
        <p><strong>描述:</strong> {{ repo?.description }}</p>
        <p><strong>URL:</strong> <a :href="repo?.url" target="_blank">{{ repo?.url }}</a></p>
        <p><strong>类型:</strong> {{ repo?.type }}</p>
        <p><strong>状态:</strong> {{ repo?.status }}</p>
        <p><strong>创建时间:</strong> {{ repo?.created_at }}</p>
      </div>
      <el-button type="primary" @click="startScan">扫描仓库</el-button>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">关闭</el-button>
      </span>
    </el-dialog>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  import { ref } from 'vue';
  interface Repo {
    id: number;
    name: string;
    description: string;
    url: string;
    type: string;
    status: string;
    created_at: string;
  }
  
  export default defineComponent({
    props: {
      repo: {
        type: Object as PropType<Repo | null>,
        default: null,
      },
    },
    emits: ['close'],
    setup(props, { emit }) {
      const visible = ref(true);
  
      const handleClose = () => {
        visible.value = false;
        emit('close');
      };
  
      const startScan = () => {
        // Implement scanning logic
        console.log('Scanning repository:', props.repo);
      };
  
      return {
        visible,
        handleClose,
        startScan,
      };
    },
  });
  </script>
  