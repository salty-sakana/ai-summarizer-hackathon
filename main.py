import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from openai import OpenAI

load_dotenv()
app = FastAPI(title="AI Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

INDEX_HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI 网页长文总结助手</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;max-width:820px;margin:2rem auto;padding:0 1.5rem;background:#f1f5f9;color:#1e293b;line-height:1.6}
h1{color:#0f172a;text-align:center;font-size:1.6rem;margin-bottom:.5rem}
.subtitle{text-align:center;color:#64748b;margin-bottom:1.5rem;font-size:.9rem}
textarea{width:100%;min-height:160px;padding:1rem;border:2px solid #cbd5e1;border-radius:10px;font-size:.95rem;font-family:inherit;resize:vertical;transition:border-color .2s}
textarea:focus{outline:none;border-color:#2563eb}
button{width:100%;padding:.85rem;margin:1rem 0;background:#2563eb;color:#fff;border:none;border-radius:10px;font-size:1.05rem;font-weight:600;cursor:pointer;transition:background .2s}
button:hover{background:#1d4ed8}
button:disabled{background:#94a3b8;cursor:not-allowed}
#output{background:#fff;padding:1.5rem;border:1px solid #e2e8f0;border-radius:10px;min-height:120px;margin-top:.5rem;overflow-x:auto}
#output h3{margin-top:1rem;color:#0f172a}
#output ul,#output ol{padding-left:1.5rem;margin:.5rem 0}
#output p{margin:.5rem 0}
.loading{color:#64748b;font-style:italic;text-align:center;padding:2rem}
.footer{text-align:center;margin-top:2rem;color:#94a3b8;font-size:.8rem}
</style>
</head>
<body>
<h1>📝 AI 长文结构化总结助手</h1>
<p class="subtitle">粘贴文本，AI 自动提炼核心结论 · 关键要点 · 行动启发</p>
<textarea id="input" placeholder="在此粘贴网页长文、论文摘要、会议记录或任何长文本..."></textarea>
<button id="btn" onclick="run()">🚀 一键总结</button>
<div id="output">等待输入...</div>
<div class="footer">AI 驱动 · 人机协同课程大作业</div>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
const btn=document.getElementById('btn'),input=document.getElementById('input'),out=document.getElementById('output');
async function run(){const t=input.value.trim();if(!t)return alert('请先粘贴文本');btn.disabled=true;btn.textContent='⏳ AI 分析中...';out.innerHTML='<div class="loading">🤖 AI 正在分析提炼中，请稍候...</div>';try{const r=await fetch('/api/summarize',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:t})});if(!r.ok){const e=await r.json();throw new Error(e.detail||'HTTP '+r.status)}const d=await r.json();out.innerHTML=marked.parse(d.result||'无结果')}catch(e){out.innerHTML='<div style="color:#dc2625;padding:1rem">❌ 错误: '+e.message+'</div>'}finally{btn.disabled=false;btn.textContent='🚀 一键总结'}}
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.ctrlKey)run()});
</script>
</body>
</html>"""

@app.get("/")
def root():
    return HTMLResponse(INDEX_HTML)

@app.get("/6107125110.txt")
def domain_verify():
    try:
        with open("6107125110.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(404, "验证文件未找到")

@app.post("/api/summarize")
async def summarize(req: dict):
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    if not api_key:
        raise HTTPException(500, "后端未配置 LLM_API_KEY")

    client = OpenAI(api_key=api_key, base_url=base_url)
    user_text = req.get("text", "")[:2000]

    prompt = """你是专业内容分析师。请将以下文本进行结构化总结，输出格式为Markdown：

### 📌 核心结论
...

### 🔑 关键要点
1. ...

### 💡 行动/启发
..."""

    try:
        response = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct",
            messages=[{"role": "user", "content": prompt + "\n\n" + user_text}],
            temperature=0.7
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(500, f"模型调用失败: {str(e)}")
