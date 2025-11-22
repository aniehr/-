import json, os, time

GALLERY_PATH = "gallery.json"
# 如果没有记录文件就创建
if not os.path.exists(GALLERY_PATH):
    with open(GALLERY_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

import gradio as gr
from epitaph_generator import generate_deepseek_epitaph
from analyzer import analyze_text
import random
import html
from filelock import FileLock


def process_text(input_text):
    if not isinstance(input_text, str) or not input_text.strip():
        return "<div style='color:#ff6666;padding:10px;border-radius:6px;background:#2b2b2b;'>💩请输入想葬送的代码或语段。</div>"

    try:
        analysis = analyze_text(input_text)
        score = analysis.get("score", 0)
        if not isinstance(analysis, dict):
            analysis = {}
    except:
        analysis = {}

    lower_text = input_text.lower()
    tone_hint = None
    if any(k in lower_text for k in ["love", "爱", "喜欢", "孤独"]):
        tone_hint = "情感破碎"
    elif any(k in lower_text for k in ["bug", "error", "代码", "程序", "函数"]):
        tone_hint = "程序崩塌"
    elif any(k in lower_text for k in ["梦", "诗", "虚无", "思考"]):
        tone_hint = "抽象诗意"
    elif len(input_text) < 15:
        tone_hint = "短促的绝唱"
    elif len(input_text) > 200:
        tone_hint = "冗长的遗言"

    analysis["tone_hint"] = tone_hint

    # ✅ 确保真正调用大模型
    print("🟦 正在调用 generate_deepseek_epitaph() ...")
    try:
        epitaph = generate_deepseek_epitaph(input_text, analysis)
    except Exception as e:
        print("⚠️ 调用失败 → fallback\n", e)
        epitaph = "此处原本应有墓志铭，但作者罢工了。"


    preview = html.escape(input_text.strip())
    preview_short = preview[:80] + ("..." if len(preview) > 80 else "")
    symbol = random.choice(["🪦", "💀", "☠️", "⚰️", "📊"])

    # 随机视觉主题
    theme = random.choice(["bloodlight", "voidcore", "neonfaith"])
    if theme == "bloodlight":
        grad = "radial-gradient(circle at 50% 50%, #2b0000 0%, #000000 100%)"
        glow = "#ff0033"
        rune = "rgba(255, 80, 80, 0.25)"
    elif theme == "voidcore":
        grad = "radial-gradient(circle at 50% 50%, #000014 0%, #000000 100%)"
        glow = "#6699ff"
        rune = "rgba(120, 200, 255, 0.25)"
    else:
        grad = "radial-gradient(circle at 50% 50%, #10002b 0%, #000000 100%)"
        glow = "#ff00cc"
        rune = "rgba(255, 120, 255, 0.25)"

    html_modal = f"""
    <style>
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: scale(0.98); }}
        to {{ opacity: 1; transform: scale(1); }}
    }}
    @keyframes runeSpin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    @keyframes flare {{
        0%,100% {{ opacity: 0.2; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.05); }}
    }}
    @keyframes particle {{
        0% {{ transform: translateY(0); opacity: 0; }}
        50% {{ opacity: 1; }}
        100% {{ transform: translateY(-80px); opacity: 0; }}
    }}
    @keyframes glowtext {{
        0%,100% {{ text-shadow: 0 0 15px {glow}, 0 0 45px {glow}; }}
        50% {{ text-shadow: 0 0 35px {glow}, 0 0 80px {glow}; }}
    }}
    </style>

    <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:{grad};
        display:flex;align-items:center;justify-content:center;overflow:hidden;
        animation:fadeIn 0.3s cubic-bezier(0.24, 0.82, 0.27, 1.12);z-index:9999;color:white;font-family:'Noto Sans SC','Orbitron',monospace;">

        <!-- 多层符文阵 -->
        <div style="position:absolute;width:700px;height:700px;border:1px solid {rune};
                    border-radius:50%;animation:runeSpin 80s linear infinite;"></div>
        <div style="position:absolute;width:480px;height:480px;border:1px dashed {rune};
                    border-radius:50%;animation:runeSpin 60s linear infinite reverse;"></div>
        <div style="position:absolute;width:300px;height:300px;border:1px dotted {rune};
                    border-radius:50%;animation:runeSpin 100s linear infinite;"></div>

        <!-- 光晕层 -->
        <div style="position:absolute;width:900px;height:900px;border-radius:50%;
                    background:{glow};filter:blur(180px);opacity:0.05;animation:flare 6s ease-in-out infinite;"></div>

        <!-- 粒子 -->
        {"".join([f"<div style='position:absolute;width:3px;height:3px;background:{glow};border-radius:50%;top:{random.randint(0,100)}%;left:{random.randint(0,100)}%;animation:particle {random.uniform(5,8)}s ease-in-out infinite;animation-delay:{random.uniform(0,4)}s;'></div>" for _ in range(20)])}

        <!-- 仪式中心 -->
        <div style="text-align:center;animation:fadeIn 0.5s cubic-bezier(0.38, 0.68, 0.23, 1.18);max-width:680px;padding:40px;background:rgba(0,0,0,0.35);backdrop-filter:blur(10px);border-radius:30px;border:1px solid {glow};box-shadow:0 0 50px {glow}33, inset 0 0 30px {glow}22;">
            <div style="font-size:96px;animation:glowtext 3s infinite alternate;margin-bottom:10px;">{symbol}</div>
            <h1 style="font-size:42px;letter-spacing:4px;margin:0 0 16px;
                       background:linear-gradient(90deg,{glow},#fff,#ffcc00);
                       -webkit-background-clip:text;color:transparent;
                       animation:glowtext 3s infinite alternate;">屎山修祀</h1>
            <p style="font-size:14px;color:#999;margin-bottom:14px;">入葬：</p>
            <div style="font-size:15px;color:#ccc;background:rgba(0,0,0,0.3);padding:16px;border-radius:10px;max-height:150px;overflow:auto;">{preview_short}</div>
            <div style="margin-top:28px;font-size:22px;line-height:1.5;
                        text-shadow:0 0 20px {glow},0 0 50px {glow};
                        animation:glowtext 4s infinite alternate;">{html.escape(epitaph)}</div>
            <div style="margin-top:12px;font-size:18px;color:#ffcccc;text-shadow:0 0 15px {glow};">
                屎山指数：{score}/100
            </div>
        </div>
    </div>
    """

    # === 保存记录到公共碑墙（并发安全版本） ===
    try:
        record = {
            "epitaph": epitaph,
            "preview": preview_short,
            "score": score,
            "time": int(time.time())
        }

        lock = FileLock(GALLERY_PATH + ".lock")
        with lock:
            # 读取已有数据
            try:
                with open(GALLERY_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = []
            except:
                data = []

            # 追加记录
            data.append(record)

            # 限制最大长度，避免文件无限增长
            data = data[-500:]

            # 覆写保存
            with open(GALLERY_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    except Exception as e:
        print("⚠️ 公共碑墙保存失败:", e)

    return html_modal


def view_gallery():
    try:
        with open(GALLERY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            data = []
    except:
        return "暂无碑文记录。"

    # 按时间倒序排列
    data = sorted(data, key=lambda x: x.get("time", 0), reverse=True)

    items = []
    for d in data[-25:]:
        t = time.strftime("%Y-%m-%d %H:%M", time.localtime(d["time"]))
        items.append(f"**{t}** | 屎山指数：{d['score']}\n\n> {d['epitaph']}\n")

    return "\n---\n".join(items)


with gr.Blocks(css="""
body { background:#0b0b0c; color:#eaeaea; font-family: 'Noto Sans SC', 'PingFang SC', sans-serif; }
.gr-button { background: #444 !important; color: #fff !important; }
""") as demo:
    gr.Markdown("<h1 style='text-align:center'>屎山修祀</h1>")
    gr.Markdown("<p style='text-align:center;color:#bfbfbf'>输入你想送葬的文本或代码，点“送葬”后出现碑文。</p>")

    with gr.Row():
        input_box = gr.Textbox(label="别担心，孩子，不是所有产出都是为了创造价值。", lines=8, placeholder="把你想埋葬的句子、段落或代码粘贴在这里…")

    submit_btn = gr.Button("⚰️ 送葬！")
    html_output = gr.HTML()
    view_btn = gr.Button("进入公共墓园")
    gallery_output = gr.Markdown()

    submit_btn.click(process_text, inputs=input_box, outputs=html_output)
    view_btn.click(fn=view_gallery, inputs=None, outputs=[gallery_output])


if __name__ == "__main__":
    demo.launch()
