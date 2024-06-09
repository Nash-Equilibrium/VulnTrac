<template>
    <el-dialog :visible.sync="visible" title="添加/编辑仓库" @close="handleClose">
      <el-form :model="form" ref="formRef" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description"></el-input>
        </el-form-item>
        <el-form-item label="URL">
          <el-input v-model="form.url"></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.type">
            <el-option label="GitHub" value="github"></el-option>
            <el-option label="GitLab" value="gitlab"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </span>
    </el-dialog>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, watch, PropType } from 'vue';
  import { useStore } from 'vuex';
  
  interface Repo {
    id?: number;
    name: string;
    description: string;
    url: string;
    type: string;
    status?: string;
    created_at?: string;
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
      const store = useStore();
      const form = ref<Repo>({ name: '', description: '', url: '', type: '' });
      const formRef = ref(null);
      const visible = ref(true);
  
      watch(() => props.repo, (newRepo) => {
        if (newRepo) {
          form.value = { ...newRepo };
        } else {
          form.value = { name: '', description: '', url: '', type: '' };
        }
      }, { immediate: true });
  
      const handleClose = () => {
        emit('close');
      };
  
      const handleSave = () => {
        if (props.repo) {
          store.commit('updateRepo', form.value);
        } else {
          form.value.id = Date.now(); // 简单的ID生成策略
          form.value.status = 'active';
          form.value.created_at = new Date().toISOString();
          store.commit('addRepo', form.value);
        }
        emit('close');
      };
  
      return {
        form,
        formRef,
        visible,
        handleClose,
        handleSave,
      };
    },
  });
  </script>
  