# 📝 AI 网页长文结构化总结助手

> 人机协同程序设计 · 期末大作业

📍 **在线体验链接**：`https://你的应用名.onrender.com`（部署后替换）

一款基于 FastAPI + Qwen-2.5 大模型的轻量级文本总结工具。粘贴长文本，AI 自动按 **核心结论 → 关键要点 → 行动启发** 三段式结构化输出，支持 Markdown 渲染。

---

## 功能特性

- ✅ 一键结构化总结：AI 将任意长文本提炼为核心结论 + 关键要点 + 行动启发
- ✅ Markdown 渲染：结果清晰美观，重点一目了然
- ✅ 前后端分离：后端 FastAPI 代理 API 请求，前端纯静态单页
- ✅ 跨域安全：避免 API Key 暴露在前端

## 技术栈

| 模块 | 技术 |
|------|------|
| 前端 | HTML5 + CSS3 + JavaScript（原生，零依赖） |
| 后端 | Python FastAPI |
| AI 引擎 | 硅基流动 SiliconFlow（兼容 OpenAI API）/ Qwen-2.5-72B |
| 部署 | Render.com |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/ai-summarizer-hackathon.git
cd ai-summarizer-hackathon
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`，填入你的 API Key：

```
LLM_API_KEY=你的硅基流动API密钥
LLM_BASE_URL=https://api.siliconflow.cn/v1
```

**免费申请 API Key**：[硅基流动 SiliconFlow](https://cloud.siliconflow.cn) → 注册 → 实名认证 → 创建 API Key

### 4. 本地运行

```bash
uvicorn main:app --reload
```

访问 `http://localhost:8000/static/index.html` 即可使用。

## 部署到 Render

1. 将代码推送至 GitHub
2. 登录 [Render.com](https://render.com) → New Web Service → 连接你的 GitHub 仓库
3. Build Command：`pip install -r requirements.txt`
4. Start Command：`uvicorn main:app --host 0.0.0.0 --port $PORT`
5. 添加环境变量 `LLM_API_KEY`
6. 部署完成，获取 `*.onrender.com` 链接

## 项目结构

```
ai-summarizer/
├── main.py              # FastAPI 后端入口
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量模板
├── .gitignore
├── README.md
└── static/
    └── index.html       # 前端单页应用
```

## AI 协作说明

本项目 80% 代码由 AI 大模型生成，人工决策与修正部分：

| 环节 | AI 贡献 | 人工决策 |
|------|---------|----------|
| 架构设计 | 建议 FastAPI + 纯前端方案 | 决定拆分 static 目录，使用 .env 管理密钥 |
| 后端代码 | 生成 FastAPI 路由与 OpenAI 调用代码 | 替换 URL 为硅基流动兼容端点，添加长度截断 |
| 前端渲染 | 生成原生 JS fetch + Markdown 渲染 | 引入 marked.js CDN，优化 UI/UX |
| 部署配置 | 提供 Render 部署模板配置 | 添加 $PORT 环境变量处理健康检查 |
