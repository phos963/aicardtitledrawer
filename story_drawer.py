import streamlit as st
import random
import json
from datetime import datetime

st.set_page_config(page_title="靈感抽籤機", layout="centered")
st.title("🎰 靈感抽籤發想機")
st.caption("編輯籤盒 → 設定抽幾個籤 → 點擊抽籤 → 獲得故事靈感與紀錄保存！")

# 儲存紀錄的筆記檔案
LOG_FILE = "draw_log.json"

# 初始化 session state
if "boxes" not in st.session_state:
    st.session_state.boxes = [
        {"title": "角色身份", "items": "勇者, 刺客, 科學家"},
        {"title": "角色屬性", "items": "火, 冰, 雷, 光"},
        {"title": "角色性格", "items": "冷靜, 衝動, 傲嬌"},
        {"title": "世界觀", "items": "後末日, 魔法現代, 賽博龐克"},
        {"title": "主題劇情", "items": "背叛與救贖, 拯救世界, 命運對抗"},
    ]

st.subheader("🧾 編輯籤盒")
for i, box in enumerate(st.session_state.boxes):
    st.session_state.boxes[i]["title"] = st.text_input(f"籤盒名稱 {i+1}", box["title"])
    st.session_state.boxes[i]["items"] = st.text_area(f"籤內容（用 , 分隔）", box["items"], height=70)

# 自訂抽幾個籤
st.subheader("🎯 每籤盒抽幾個")
draw_counts = []
for i, box in enumerate(st.session_state.boxes):
    max_items = len([x for x in box["items"].split(",") if x.strip()])
    count = st.selectbox(f"從「{box['title']}」中抽幾個？", range(1, max_items + 1), index=0, key=f"count_{i}")
    draw_counts.append(count)

# 抽籤按鈕
if st.button("🎲 點我抽靈感！"):
    result = {}
    for i, box in enumerate(st.session_state.boxes):
        items = [x.strip() for x in box["items"].split(",") if x.strip()]
        drawn = random.sample(items, min(len(items), draw_counts[i]))
        result[box["title"]] = drawn

    st.subheader("✨ 抽籤結果")
    for k, v in result.items():
        st.markdown(f"**{k}**：{'、'.join(v)}")

    # 抓故事元素
    titles = list(result.keys())
    flat = lambda x: x[0] if isinstance(x, list) and len(x) == 1 else "與".join(x)
    identity = flat(result.get("角色身份", ["未知角色"]))
    attribute = flat(result.get("角色屬性", ["神秘屬性"]))
    traits = flat(result.get("角色性格", ["未知性格"]))
    world = flat(result.get("世界觀", ["未知世界"]))
    theme = flat(result.get("主題劇情", ["未知主題"]))

    story_titles = [
        (f"《{attribute}影之{identity}》", f"在{world}中，一位{traits}的{identity}踏上了關於「{theme}」的旅程。"),
        (f"《{world}的命運連鎖》", f"{identity}懷抱{attribute}之力，在{world}中展開{theme}的故事。"),
        (f"《{traits}者的{theme}詩篇》", f"這是一位{traits}的{identity}，在{world}中挑戰命運的故事。")
    ]

    st.subheader("📚 AI 推薦故事名稱與方向")
    for i, (title, desc) in enumerate(story_titles, 1):
        st.markdown(f"**{i}. {title}**\n> {desc}")

    # 儲存紀錄
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "result": result,
        "story_titles": story_titles
    }
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_data = json.load(f)
    except:
        log_data = []

    log_data.append(log_entry)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)

    st.success("✅ 本次抽籤結果已儲存！")

# 查看歷史紀錄（可選）
with st.expander("📜 查看過往抽籤紀錄"):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
        for entry in reversed(logs[-5:]):
            st.markdown(f"🕒 **{entry['timestamp']}**")
            for k, v in entry["result"].items():
                st.markdown(f"- **{k}**：{'、'.join(v)}")
    except:
        st.info("尚無任何抽籤紀錄。")
