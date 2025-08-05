import streamlit as st
import random
import json
import os

st.set_page_config(page_title="靈感抽籤機", layout="wide")

# 最大籤盒數量
MAX_BOXES = 15

# 預設籤盒數量
if "num_boxes" not in st.session_state:
    st.session_state.num_boxes = 5

# 載入抽籤紀錄（存在本地JSON）
def load_draw_log():
    if os.path.exists("draw_log.json"):
        with open("draw_log.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_draw_log(log):
    with open("draw_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

# 初始化籤盒資料結構
def init_boxes(n):
    if "boxes" not in st.session_state or len(st.session_state.boxes) != n:
        st.session_state.boxes = []
        for i in range(n):
            st.session_state.boxes.append({
                "title": f"籤盒 {i+1}",
                "contents": "",
                "draw_count": 1
            })

# 顯示輸入區塊
def render_input_area():
    st.header("自訂抽籤籤盒與抽取數量")
    num = st.number_input(
        "請輸入籤盒數量（最大15）",
        min_value=1,
        max_value=MAX_BOXES,
        value=st.session_state.num_boxes,
        step=1,
        key="num_boxes_input"
    )
    if num != st.session_state.num_boxes:
        st.session_state.num_boxes = num
        init_boxes(num)

    for i in range(st.session_state.num_boxes):
        box = st.session_state.boxes[i]
        st.subheader(f"籤盒 {i+1}")
        box["title"] = st.text_input(
            "籤盒標題",
            value=box["title"],
            key=f"title_{i}"
        )
        box["contents"] = st.text_area(
            "籤內容（請用逗號分隔）",
            value=box["contents"],
            height=100,
            key=f"contents_{i}"
        )
        options = [x.strip() for x in box["contents"].split(",") if x.strip()]
        max_draw = len(options)
        box["draw_count"] = st.number_input(
            f"從此籤盒中抽幾個？(0 - {max_draw})",
            min_value=0,
            max_value=max_draw,
            value=min(box["draw_count"], max_draw),
            step=1,
            key=f"draw_count_{i}"
        )
        st.markdown("---")

def draw_sticks():
    result = {}
    for box in st.session_state.boxes:
        options = [x.strip() for x in box["contents"].split(",") if x.strip()]
        count = box["draw_count"]
        if count > len(options):
            count = len(options)
        picks = random.sample(options, count) if options and count > 0 else []
        result[box["title"]] = picks
    return result

def recommend_titles():
    # 範例簡易推薦，這裡可擴充成AI模型呼叫
    return [
        "命運之輪的轉動",
        "破曉的冒險",
        "暗影下的真相"
    ]

def main():
    st.title("✨ 靈感抽籤機 ✨")

    render_input_area()

    if st.button("🎲 抽靈感！"):
        results = draw_sticks()
        st.success("抽籤結果：")
        for box_title, picks in results.items():
            st.write(f"**{box_title}**: {', '.join(picks) if picks else '未抽取'}")

        titles = recommend_titles()
        st.info("AI 推薦故事標題：")
        for t in titles:
            st.write(f"- {t}")

        # 儲存抽籤紀錄
        draw_log = load_draw_log()
        draw_log.insert(0, {"result": results, "titles": titles})
        draw_log = draw_log[:5]  # 只保留最近5筆
        save_draw_log(draw_log)

    st.markdown("---")
    st.header("🎴 最近5筆抽籤紀錄")
    draw_log = load_draw_log()
    for i, entry in enumerate(draw_log):
    st.write(f"第 {i+1} 次抽籤：")
    for box_title, picks in entry["result"].items():
        st.write(f"- **{box_title}**: {', '.join(picks) if picks else '未抽取'}")
    titles = entry.get("titles", [])  # 用 get() 預防沒有 titles
    st.write("推薦標題： " + ", ".join(titles))
    st.markdown("---")


if __name__ == "__main__":
    init_boxes(st.session_state.num_boxes)
    main()

