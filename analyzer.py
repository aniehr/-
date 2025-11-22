# analyzer.py
import re
from collections import Counter

def analyze_text(txt: str):
    s = txt.strip()
    if not s:
        return {"score": 0, "reason": ["空文本"]}

    # ① 重复度
    words = re.findall(r"[\w\u4e00-\u9fa5]+", s)
    freq = Counter(words)
    repeat_ratio = freq.most_common(1)[0][1] / max(len(words), 1)

    # ② 句长松弛度
    sentences = re.split(r"[。！？!?]", s)
    sentences = [x.strip() for x in sentences if x.strip()]
    avg_len = sum(len(x) for x in sentences) / max(len(sentences), 1)

    # ③ 官腔词检测（经典 BS indicator）
    bs_keywords = ["推进", "落实", "提升", "加强", "充分", "全面", "建设", "意义重大", "密切结合"]

    bs_count = sum(1 for k in bs_keywords if k in s)

    # === 屎山指数计算公式 ===
    score = (
        repeat_ratio * 40 +      # 词语复读 = 机械化
        (avg_len / 30) * 30 +    # 句子越长 → 越像废话
        bs_count * 8             # 官话每出现一个就加分
    )

    score = int(min(100, score))  # 保底 0-100 范围

    reasons = []
    if repeat_ratio > 0.2: reasons.append("复读如念经")
    if avg_len > 50: reasons.append("一句话说半天")
    if bs_count > 0: reasons.append("官僚腔拉满")
    if not reasons: reasons.append("还挺清爽的")

    return {
        "score": score,
        "reasons": reasons
    }
