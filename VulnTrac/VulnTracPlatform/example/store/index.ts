import { createStore } from 'vuex';

interface Repo {
  id: number;
  name: string;
  description: string;
  url: string;
  type: string;
  status: string;
  created_at: string;
}

interface State {
  repos: Repo[];
  records: any[];  // 根据实际需求替换 `any` 类型
}

export default createStore<State>({
  state: {
    repos: [],
    records: []
  },
  getters: {
    getRecords: (state) => state.records,
    getRepos: (state) => state.repos,
  },
  mutations: {
    setRepos(state, repos: Repo[]) {
      state.repos = repos;
    },
    addRepo(state, repo: Repo) {
      state.repos.push(repo);
    },
    updateRepo(state, updatedRepo: Repo) {
      const index = state.repos.findIndex((repo) => repo.id === updatedRepo.id);
      if (index !== -1) {
        state.repos.splice(index, 1, updatedRepo);
      }
    },
    deleteRepo(state, repoId: number) {
      state.repos = state.repos.filter((repo) => repo.id !== repoId);
    },
    addRecord(state, record) {
      state.records.push(record);
    },
    deleteRecord(state, recordId) {
      state.records = state.records.filter((record) => record.id !== recordId);
    },
  },
  actions: {
    fetchRepos({ commit }) {
      // 模拟 API 调用
      const repos = [
        {
          id: 1,
          name: 'Repo 1',
          description: 'Description 1',
          url: 'https://github.com/repo1',
          type: 'github',
          status: 'active',
          created_at: '2024-01-01'
        },
        {
          id: 2,
          name: 'Repo 2',
          description: 'Description 2',
          url: 'https://github.com/repo2',
          type: 'gitlab',
          status: 'inactive',
          created_at: '2024-02-01'
        }
      ];
      commit('setRepos', repos);
    },
    addRecord({ commit }, record) {
      commit('addRecord', record);
    },
    deleteRecord({ commit }, recordId) {
      commit('deleteRecord', recordId);
    }
  },
  modules: {}
});
