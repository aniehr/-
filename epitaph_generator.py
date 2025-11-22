print("🧠 epitaph_generator.py 已成功加载 ✅")

import os
import requests

API_KEY = os.environ.get("DEEPSEEK_API_KEY")

FALLBACK = "此处原本应有墓志铭，但作者罢工了。"

def fallback_local_epitaph(text, tone):
    t = tone or "未知情绪"
    s = (text.strip()[:40] + "…") if isinstance(text, str) and len(text.strip()) > 40 else (text or "")
    presets = {
        "情感破碎": f"把{('它' if not s else s)}埋了吧，心还在流血。",
        "程序崩塌": f"{('它' if not s else s)}被堆叠到坟里，bug 终于安息。",
        "抽象诗意": f"{('它' if not s else s)}走进虚空，词语在黑暗里发光。",
        "短促的绝唱": f"短到只剩叹息，{('它' if not s else s)}化作尘。",
        "冗长的遗言": f"冗语漫流到墓前，{('它' if not s else s)}终于止息。",
    }
    return presets.get(t, FALLBACK)

def generate_deepseek_epitaph(text, analysis):
    """
    使用 DeepSeek API 生成抽象、带语境关联的墓志铭。
    text: 用户输入文本
    analysis: { tone_hint: ... } 语气提示 + 分析信息
    """

    tone = analysis.get("tone_hint", "未知情绪")

    if not API_KEY:
        return fallback_local_epitaph(text, tone)

    prompt = f"""
你是一个写数字墓碑铭文的赛博朋克荒诞派诗人。这是一片人类用于埋葬他们创造的文本屎山的“屎山修祀”，你的任务是针对他们埋葬的内容予以简短且艺术的墓志铭。
要求：
- 与输入内容高度相关
- 懂哲学，计算机，文学等领域黑话，带有疏离的文艺疯感
- 懂中国互联网语感
- 不要用套话，不要解释,句子要短，但是要具有犀利的批判感
- 带情绪刺痛感，但不要矫情，也不要像AI
- 带一点黑色幽默、精神状态不太稳定、但必须有美感
- 最大字数：50 字

输入内容：
{text}

语气线索：{tone}

请直接输出一句话，不要任何额外内容。
"""

    try:
        attempts = 2
        last_err = None
        for _ in range(attempts):
            try:
                resp = requests.post(
                    "https://api.deepseek.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.85,
                        "max_tokens": 60
                    },
                    timeout=8
                )
                result = resp.json()
                choices = result.get("choices") or []
                if choices:
                    msg = choices[0].get("message") or {}
                    content = (msg.get("content") or "").strip()
                    if content:
                        return content
            except Exception as e:
                last_err = e
        if last_err:
            print("⚠️ 碑文生成失败：", last_err)
    except Exception as e:
        print("⚠️ 碑文生成失败：", e)

    return fallback_local_epitaph(text, tone)

