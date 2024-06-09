<template>
  <div class="card">
    <div
      style="top: 0; bottom: 0; left: 0; right: 0; margin: auto; display: flex; flex-direction: column; gap:8px; width: 95%;">
      <el-text style="color: #1B9CFC; font-weight: 600; font-size: 25px;">检测中心</el-text>
      <el-text style="color: #dff9fb; font-weight: 500;">
        <el-text style="color: #1B9CFC; font-weight: 600;">提示：</el-text>
        系统会根据您所提交的文件或代码文本自动生成检测报告；检测报告可以在检测记录中查看
      </el-text>
      <hr style="width: 100%; margin-bottom: 20px">
    </div>
    <div class="inputholder">
      <div style="text-align: left; width: 94%; margin-bottom: -5px;">
        <el-text style="color: #00a8ff; font-weight: 600;">请输入以下内容：</el-text>
      </div>
      <div class="notification" v-if="dialogVisible">
        <div class="notiglow"></div>
        <div class="notiborderglow"></div>
        <div class="notititle">提示:</div>
        <div class="notibody">该系统目前支持检测以下代码：<br> C、C++、java、python、go以及javaScript</div>
        <div class="notibody" style="justify-content: end;">
          <button class="confirmA" @click="dialogVisible = false">
            我已知晓
          </button>
        </div>
      </div>
      <div class="inputbox">
        <input v-model="codeType" required="required" type="text">
        <div class="tooltip">
          <div class="icon" @click="dialogVisible = true"> ? </div>
          <div class="tooltiptext">查看支持文件</div>
        </div>
        <span>代码类型</span>
        <i></i>
      </div>
      <div class="inputbox">
        <input v-model="codeName" required="required" type="text">
        <span>代码名称</span>
        <i></i>
      </div>
      <div class="inputbox">
        <input v-model="username" required="required" type="text">
        <span>检测用户名</span>
        <i></i>
      </div>
      <div style="text-align: left; width: 94%;">
        <el-text style="color: #00a8ff; font-weight: 600;">请选择报告适用度：</el-text>
      </div>
      <div class="radio-inputs">
        <label class="label-test">
          <input class="radio-input" type="radio" name="engine" v-model="granularity" value="beginner">
          <span class="radio-tile">
            <span class="radio-label">初学者</span>
            <hr style="width: 90%;">
            <span class="radio-label">1.更简单的讲解<br>2.更丰富的介绍</span>
          </span>
        </label>
        <label class="label-test">
          <input class="radio-input" type="radio" name="engine" v-model="granularity" value="developer">
          <span class="radio-tile">
            <span class="radio-label">程序员</span>
            <hr style="width: 90%;">
            <span class="radio-label">1.更详细的技术分析<br>2.更专业的检测分析</span>
          </span>
        </label>
        <label class="label-test">
          <input class="radio-input" type="radio" name="engine" v-model="granularity" value="reviewer">
          <span class="radio-tile">
            <span class="radio-label">审计师</span>
            <hr style="width: 90%;">
            <span class="radio-label">1.更深入的技术细节<br>2.更精简的检测分析</span>
          </span>
        </label>
      </div>
      <div style="text-align: left; width: 94%; margin-bottom: 10px;">
        <el-text style="color: #00a8ff; font-weight: 600;">请选择上传方式：</el-text>
      </div>
      <div class="radio-input-fot">
        <input @click="uploadMethod = 'file'" value="value-1" name="value-radio" id="value-1" type="radio">
        <label for="value-1">上传文件</label>
        <input @click="uploadMethod = 'text'" value="value-2" name="value-radio" id="value-2" type="radio">
        <label for="value-2">上传文本</label>
      </div>
      <div class="upload-card">
        <template v-if="uploadMethod === 'file'">
          <label for="file" class="labelFile">
            <span>
              <svg xml:space="preserve" viewBox="0 0 184.69 184.69" xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns="http://www.w3.org/2000/svg" id="Capa_1" version="1.1" width="60px" height="60px"
                style="margin-top: 10px">
                <g>
                  <g>
                    <g>
                      <path d="M149.968,50.186c-8.017-14.308-23.796-22.515-40.717-19.813
                C102.609,16.43,88.713,7.576,73.087,7.576c-22.117,0-40.112,17.994-40.112,40.115c0,0.913,0.036,1.854,0.118,2.834
                C14.004,54.875,0,72.11,0,91.959c0,23.456,19.082,42.535,42.538,42.535h33.623v-7.025H42.538
                c-19.583,0-35.509-15.929-35.509-35.509c0-17.526,13.084-32.621,30.442-35.105c0.931-0.132,1.768-0.633,2.326-1.392
                c0.555-0.755,0.795-1.704,0.644-2.63c-0.297-1.904-0.447-3.582-0.447-5.139c0-18.249,14.852-33.094,33.094-33.094
                c13.703,0,25.789,8.26,30.803,21.04c0.63,1.621,2.351,2.534,4.058,2.14c15.425-3.568,29.919,3.883,36.604,17.168
                c0.508,1.027,1.503,1.736,2.641,1.897c17.368,2.473,30.481,17.569,30.481,35.112c0,19.58-15.937,35.509-35.52,35.509H97.391
                v7.025h44.761c23.459,0,42.538-19.079,42.538-42.535C184.69,71.545,169.884,53.901,149.968,50.186z"
                        style="fill:#12CBC4; font-weight: 600; "></path>
                    </g>
                    <g>
                      <path d="M108.586,90.201c1.406-1.403,1.406-3.672,0-5.075L88.541,65.078
                c-0.701-0.698-1.614-1.045-2.534-1.045l-0.064,0.011c-0.018,0-0.036-0.011-0.054-0.011c-0.931,0-1.85,0.361-2.534,1.045
                L63.31,85.127c-1.403,1.403-1.403,3.672,0,5.075c1.403,1.406,3.672,1.406,5.075,0L82.296,76.29v97.227
                c0,1.99,1.603,3.597,3.593,3.597c1.979,0,3.59-1.607,3.59-3.597V76.165l14.033,14.036
                C104.91,91.608,107.183,91.608,108.586,90.201z" style="fill:#12CBC4; font-weight: 600;"></path>
                    </g>
                  </g>
                </g>
              </svg>
            </span>
            <p style="margin-top: 5px;margin-bottom: 10px">点击或者拖拽上传文件</p>
          </label>
          <input class="input" name="text" id="file" type="file" @change="handleFileUpload" />
          <div class="uploaded-file" v-if="file">
            <p>文件名: {{ file.name }}</p>
            <p>文件大小: {{ (file.size / 1024).toFixed(2) }} KB</p>
          </div>
          <div class="buttonholder">
            <button class="confirmB" @click="submitFile" style="background-color:#00a8ff;">
              <div class="svg-wrapper-1">
                <div class="svg-wrapper">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                    <path fill="none" d="M0 0h24v24H0z"></path>
                    <path fill="currentColor"
                      d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z">
                    </path>
                  </svg>
                </div>
              </div>
              <span>确认上传</span>
            </button>
          </div>
        </template>
        <template v-else-if="uploadMethod === 'text'">
          <textarea class="upload-text" v-model="codeText"
            placeholder="输入字符仅限 50 字以上，10000 字以下，如果超过限制请使用上传文档; 如果此处输入或者粘贴文字后也同时上传了文档，则此处的内容将被忽略!"></textarea>
          <div class="buttonholder">
            <button class="confirmB" @click="submitText" style="background-color:#00a8ff;">
              <div class="svg-wrapper-1">
                <div class="svg-wrapper">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                    <path fill="none" d="M0 0h24v24H0z"></path>
                    <path fill="currentColor"
                      d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z">
                    </path>
                  </svg>
                </div>
              </div>
              <span>确认上传</span>
            </button>
          </div>
        </template>
      </div>
    </div>
    <div style="height: 10px"></div>
    <hr style="width: 95%">
    <div style="height: 10px"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const dialogVisible = ref(false);
const codeType = ref('');
const codeName = ref('');
const username = ref('');
const granularity = ref('');
const uploadMethod = ref('file');
const codeText = ref('');
const file = ref<File | null>(null);
const router = useRouter();

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    file.value = target.files[0];
  }
};

const submitFile = async () => {
  if (file.value) {
    const formData = new FormData();
    formData.append('file', file.value);
    formData.append('codeType', codeType.value);
    formData.append('codeName', codeName.value);
    formData.append('username', username.value);
    formData.append('granularity', granularity.value);

    try {
      const uploadResponse = await axios.post('/v1/upload_file', formData);
      if (uploadResponse.data) {
        const processResponse = await axios.post('/v1/process', { filepath: uploadResponse.data });
        if (processResponse.data.success) {
          router.push('/pages/history');
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
};

const submitText = async () => {
  if (codeText.value) {
    const formData = {
      codeText: codeText.value,
      codeType: codeType.value,
      codeName: codeName.value,
      username: username.value,
      granularity: granularity.value,
    };

    try {
      const uploadResponse = await axios.post('/v1/upload_text', formData);
      if (uploadResponse.data) {
        const processResponse = await axios.post('/v1/process', { filepath: uploadResponse.data });
        router.push('/pages/history');
        if (processResponse.data.success) {
          router.push('/pages/history');
        }
      }
    } catch (error) {
      console.error(error);
    }
  }
};
</script>

<style scoped>
.card {
  align-items: start;
  position: relative;
  margin: 2.5%;
  background-color: #2C3A47;
  display: fixed;
  flex-direction: column;
  justify-content: start;
  padding: 12px;
  gap: 12px;
  border-radius: 8px;
  cursor: pointer;
}

.card::after {
  content: "";
  z-index: -1;
  position: absolute;
  inset: 0;
  background: linear-gradient(-45deg, #fc00ff 0%, #00dbde 100%);
  filter: blur(10px);
}

.inputholder {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.inputbox {
  margin: 20px;
  position: relative;
  width: 94%;
}

.inputbox input {
  position: relative;
  width: 95%;
  padding: 20px 10px 10px;
  background: transparent;
  outline: none;
  box-shadow: none;
  border: none;
  color: #2C3A47;
  font-size: 1em;
  font-weight: 600;
  letter-spacing: 0.05em;
  transition: 0.5s;
  z-index: 10;
}

.inputbox span {
  position: absolute;
  left: 0;
  padding: 20px 10px 10px;
  font-size: 1em;
  font-weight: 600;
  color: #8f8f8f;
  letter-spacing: 00.05em;
  transition: 0.5s;
  pointer-events: none;
}

.inputbox input:valid~span,
.inputbox input:focus~span {
  color: #12CBC4;
  transform: translateX(-10px) translateY(-34px);
  font-size: 0, 75em;
}

.inputbox i {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 2px;
  background: #12CBC4;
  border-radius: 4px;
  transition: 0.5s;
  pointer-events: none;
  z-index: 9;
}

.inputbox input:valid~i,
.inputbox input:focus~i {
  height: 35px;
}

.radio-inputs {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 98%;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

.radio-inputs .label-test {
  width: 33%;
}

.radio-inputs>* {
  margin-left: 2%;
  margin-right: 2%;
  margin-bottom: 2%;
  margin-top: 2%;
}

.radio-input:checked+.radio-tile {
  border-color: #12CBC4;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  color: #12CBC4;
}

.radio-input:checked+.radio-tile:before {
  transform: scale(1);
  opacity: 1;
  background-color: #535c68;
  border-color: #c7ecee;
}

.radio-input:checked+.radio-tile .radio-icon svg {
  fill: #1B9CFC;
}

.radio-input:checked+.radio-tile .radio-label {
  font-weight: 800;
  font-size: 0, 75em;
  max-width: 90%;
  color: #2f3640;
}

.radio-input:focus+.radio-tile {
  background-color: #12CBC4;
  border-color: #1B9CFC;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1), 0 0 0 4px #25CCF7;
}

.radio-input:focus+.radio-tile:before {
  transform: scale(1);
  opacity: 1;
}

.radio-input:checked+.radio-tile {
  background-color: #12CBC4;
  border-color: #1B9CFC;
  box-shadow: 0 2.5px 5px rgba(0, 0, 0, 0.1), 0 0 0 2px rgb(129, 235, 129);
}

.radio-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 150px;
  border-radius: 0.5rem;
  border: 2px solid #b5bfd9;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: 0.15s ease;
  cursor: pointer;
  position: relative;
}

.radio-tile:before {
  content: "";
  position: absolute;
  display: block;
  width: 0.75rem;
  height: 0.75rem;
  border: 2px solid #b5bfd9;
  background-color: #12CBC4;
  border-radius: 50%;
  top: 0.25rem;
  left: 0.25rem;
  opacity: 0;
  transform: scale(0);
  transition: 0.25s ease;
}

.radio-tile:hover {
  border-color: #2260ff;
}

.radio-tile:hover:before {
  transform: scale(1);
  opacity: 1;
}

.radio-icon svg {
  width: 2rem;
  height: 2rem;
  fill: #1e272e;
}

.radio-label {
  font-size: 1em;
  font-weight: 600;
  color: #12CBC4;
  transition: 0.375s ease;
  text-align: center;
}

.radio-input {
  clip: rect(0 0 0 0);
  -webkit-clip-path: inset(100%);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}

.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
  font-family: "Arial", sans-serif;
  z-index: 11;
  font-weight: 600;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

.tooltiptext {
  visibility: hidden;
  width: 200px;
  background-color: #333;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  top: 125%;
  left: 50%;
  margin-left: -100px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltiptext::after {
  content: "";
  position: absolute;
  top: -10px;
  left: 50%;
  margin-left: -10px;
  border-width: 10px;
  border-style: solid;
  border-color: transparent transparent #333 transparent;
}

.tooltip .icon {
  display: inline-block;
  width: 19px;
  height: 19px;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
}

.upload-card {
  width: 95%;
}

.upload-options-card {
  margin-bottom: 15px;
  width: 100%;
  border: 5px solid #b5bfd9;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  transition: 0.15s ease;
  cursor: pointer;
  position: relative;
  background-color: #f5f6fa;
}

::v-deep .upload-btn-box {
  text-align: center;
  margin-top: 20px;
  background-color: #1B9CFC;
}

.upload-file-box {
  border-radius: 10px;
  margin-bottom: 20px;
}

.file-list {
  margin-bottom: 20px;
}

.upload-demo .el-upload__text {
  font-size: 16px;
  color: #606266;
  background-color: black;
}

.upload-click {
  color: #409eff;
  cursor: pointer;
}

.upload-tips-red {
  color: #f56c6c;
}

.file-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background: url('/path/to/file-icon.png') no-repeat center;
  background-size: contain;
  margin-right: 8px;
}

.upload-wait {
  width: 16px;
  height: 16px;
  background: url('/path/to/upload-wait-icon.png') no-repeat center;
  background-size: contain;
}

.progress-bar {
  margin-top: 20px;
}

.submit-btn-box {
  text-align: center;
  margin-top: 20px;
}

.text-pasting {
  background: #fff;
  border-radius: 10px;
}

.buttonholder {
  margin-top: 10px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.confirmB {
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  background: #2260ff;
  color: white;
  padding: 0.7em;
  padding-left: 0.9em;
  display: flex;
  align-items: center;
  border: none;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.2s;
  cursor: pointer;
  height: 35px;
}

.confirmB span {
  display: block;
  margin-left: 0.3em;
  transition: all 0.3s ease-in-out;
}

.confirmBb svg {
  display: block;
  transform-origin: center center;
  transition: transform 0.3s ease-in-out;
}

.confirmB:hover .svg-wrapper {
  animation: fly-1 0.6s ease-in-out infinite alternate;
}

.confirmB:hover svg {
  transform: translateX(1.2em) rotate(45deg) scale(1.1);
}

.confirmB:hover span {
  transform: translateX(5em);
}

.confirmB:active {
  transform: scale(0.95);
}

@keyframes fly-1 {
  from {
    transform: translateY(0.1em);
  }

  to {
    transform: translateY(-0.1em);
  }
}

.input {
  max-width: 100%;
  display: none;
}

.labelFile {
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 150x;
  border: 2px dashed #12CBC4;
  align-items: center;
  text-align: center;
  padding: 5px;
  color: #12CBC4;
  font-weight: 600;
  cursor: pointer;
}

.radio-input-fot {
  display: flex;
  flex-direction: row;
  font-size: 13px;
  font-weight: 600;
  color: #12CBC4;
  margin-bottom: 10px;
}

.radio-input-fot input[type="radio"] {
  display: none;
}

.radio-input-fot label {
  display: flex;
  align-items: center;
  padding: 5px;
  border: 2px solid #12CBC4;
  ;
  border-radius: 10px;
  margin-right: 12px;
  cursor: pointer;
  position: relative;
  transition: all 0.3s ease-in-out;
}

.radio-input-fot label:before {
  content: "";
  display: block;
  position: absolute;
  top: 50%;
  left: 0;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #fff;
  border: 2px solid #ccc;
  transition: all 0.3s ease-in-out;
}

.radio-input-fot input[type="radio"]:checked+label:before {
  background-color: #535c68;
  top: 0;
}

.radio-input-fot input[type="radio"]:checked+label {
  background-color: #12CBC4;
  color: #2f3640;
  border-color: rgb(129, 235, 129);
  animation: radio-translate 0.5s ease-in-out;
}

@keyframes radio-translate {
  0% {
    transform: translateX(0);
  }

  50% {
    transform: translateY(-10px);
  }

  100% {
    transform: translateX(0);
  }
}

.upload-text {
  border-radius: 8px;
  height: 130px;
  width: 100%;
  resize: none;
  outline: 0;
  padding: 8px 14px;
  border: 2px solid #12CBC4;
  background-color: #2C3A47;
  color: white;
  margin-bottom: -8px;
}


.notification {
  display: flex;
  flex-direction: column;
  isolation: isolate;
  position: absolute;
  top: 240px;
  width:40%;
  z-index: 100;
  background: #2d3436;
  border-radius: 1rem;
  overflow: hidden;
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  font-size: 16px;
  --gradient: linear-gradient(to bottom, #2eadff, #3d83ff, #7e61ff);
  --color: #32a6ff
  margin-bottom: 20px;
  animation: fadeIn 0.25s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.notification:before {
  position: absolute;
  content: "";
  inset: 0.0625rem;
  border-radius: 0.9375rem;
  background:  #2d3436;
  z-index: 2
}

.notification:after {
  position: absolute;
  content: "";
  width: 0.25rem;
  inset: 0.65rem auto 0.65rem 0.5rem;
  border-radius: 0.125rem;
  background: var(--gradient);
  transition: transform 300ms ease;
  z-index: 4;
}

.notification:hover:after {
  transform: translateX(0.15rem)
}

.notititle {
  color: var(--color);
  padding: 0.65rem 0.25rem 0.4rem 1.25rem;
  font-weight: 500;
  font-size: 1.1rem;
  transition: transform 300ms ease;
  z-index: 5;
}

.notification:hover .notititle {
  transform: translateX(0.15rem)
}

.notibody {
  color: #99999d;
  padding: 0 1.25rem;
  transition: transform 300ms ease;
  z-index: 5;
  margin-bottom: 10px;
}

.notification:hover .notibody {
  transform: translateX(0.25rem);
}

.notiglow,
.notiborderglow {
  position: absolute;
  width: 20rem;
  height: 20rem;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle closest-side at center, white, transparent);
  opacity: 0;
  transition: opacity 300ms ease;
}

.notiglow {
  z-index: 3;
}

.notiborderglow {
  z-index: 1;
}

.notification:hover .notiglow {
  opacity: 0.1
}

.notification:hover .notiborderglow {
  opacity: 0.1
}

.note {
  color: var(--color);
  position: fixed;
  top: 80%;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  font-size: 0.9rem;
  width: 75%;
}

.confirmA {
  width: 8em;
  position: relative;
  height: 2.5em;
  border: 3px ridge #149CEA;
  outline: none;
  background-color: transparent;
  color: white;
  transition: 1s;
  border-radius: 0.3em;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
}

.confirmA::after {
  content: "";
  position: absolute;
  top: -10px;
  left: 3%;
  width: 95%;
  height: 40%;
  background-color:  #2d3436;
  transition: 0.5s;
  transform-origin: center;
}

.confirmA::before {
  content: "";
  transform-origin: center;
  position: absolute;
  top: 80%;
  left: 3%;
  width: 95%;
  height: 40%;
  background-color: #2d3436;
  transition: 0.5s;
}

.confirmA:hover::before, button:hover::after {
  transform: scale(0)
}

.confirmA:hover {
  box-shadow: inset 0px 0px 25px #1479EA;
}
</style>
