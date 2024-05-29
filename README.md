`本仓库为2024年全国大学生信息安全竞赛作品赛项目代码仓库（在研）`
# VulnTrac:一种基于RLHF的代码脆弱性检测系统
# System Overview
![PPT学术图-Latest drawio (2)](https://github.com/Nash-Equilibrium/ciscn/assets/90449797/60e10a32-12b4-4392-a35e-a9cd2d18f127)


# 功能介绍
## 1.智能漏洞检测和修复提示
实现路线：
1. 拆解漏洞检测任务为漏洞定位任务、信息检索任务和总结任务。
2. 利用LangChain，通过SimpleSequentialChain将针对子任务所设计的不同Prompt Template进行链式使用。
3. 利用Secure_Programming_DPO数据集进行DPO微调。

## 2.支持对代码仓库实时监控
实现路线：
1. 维护一个Repo缓存数据库，利用request库下载仓库压缩包到本地，利用Celery库保证数据更新，间隔为设定值。
2. Repo缓存数据库中存放仓库压缩包Hash值，将更新后的压缩包Hash与前一项比较，若不同，则执行检测流程。
3. 检测结果形成PDF，通过邮件通知用户。

## 3.支持长文件分析
实现路线：
1. 首先判断代码长度，若超长则利用tree-sitter提取代码的AST。
2. 将提取的AST与LLM交互，自动进行代码注释标注。
3. 将包含代码注释的代码送入LangChain，进行下一步处理。

## 4.支持多源文件分析
实现路线：
1. 如果多个源文件中有长文件，先对其执行长文件的处理。
2. 维护一个过滤名单，以后缀名为匹配字段，将无关文件（例如配置文件、图片等）过滤。
3. 分别对预处理后的文件进行相似度分析，并按相似度降序排列，以达到设置的窗口大小为目标贪心组合代码块。

# 启动方法
`由于模型的微调尚未完成，故暂未提供模型文件下载。微调完成后会同步至Huggingface与Modelscope。`

​	

1. vendor文件夹需自行clone构建，在tree-sitter官方代码库clone对应语言解析库到vendor文件夹下，网址如下https://tree-sitter.github.io/tree-sitter/
1. 安装Redis，启动redis-server。
2. 启动celery ，在另一个终端执行：
```shell
$ celery -A app.celery worker --beat --scheduler redis --loglevel=info
```
3. 开启flask服务，执行app.py即可。
