import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

load_dotenv()
app = FastAPI(title="AI Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/api/summarize")
async def summarize(req: dict):
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
    if not api_key:
        raise HTTPException(500, "后端未配置 LLM_API_KEY")

    client = OpenAI(api_key=api_key, base_url=base_url)
    user_text = req.get("text", "")[:2000]

    prompt = f"""你是专业内容分析师。请将以下文本进行结构化总结，输出格式为Markdown：

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
