import streamlit as st
import random
import json
import os

st.set_page_config(page_title="靈感抽籤機", layout="wide")

MAX_BOXES = 15

if "num_boxes" not in st.session_state:
    st.session_state.num_boxes = 5

def load_draw_log():
    if os.path.exists("draw_log.json"):
        with open("draw_log.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_draw_log(log):
    with open("draw_log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def init_boxes(n):
    if "boxes" not in st.session_state or len(st.session_state.boxes) != n:
        st.session_state.boxes = []
        for i in range(n):
            st.session_state.boxes.append({
                "title": f"籤盒 {i+1}",
                "contents": "",
                "draw_count": 1
            })

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

def recommend_titles_from_results(results):
    all_picks = []
    for picks in results.values():
        all_picks.extend(picks)
    if not all_picks:
        return ["無抽籤結果，無法推薦標題"]

    picks_sample = random.sample(all_picks, min(3, len(all_picks)))

    titles = [
        f"關於{'、'.join(picks_sample)}的故事",
        f"探索{'與'.join(picks_sample)}的冒險",
        f"{picks_sample[0]}與{picks_sample[-1]}的傳說"
    ]
    return titles

def main():
    st.title("✨ 靈感抽籤機 ✨")

    render_input_area()

    if st.button("🎲 抽靈感！"):
        results = draw_sticks()
        st.success("抽籤結果：")
        for box_title, picks in results.items():
            st.write(f"**{box_title}**: {', '.join(picks) if picks else '未抽取'}")

        titles = recommend_titles_from_results(results)

        st.info("AI 推薦故事標題：")
        for t in titles:
            st.write(f"- {t}")

        draw_log = load_draw_log()
        draw_log.insert(0, {"result": results, "titles": titles})
        draw_log = draw_log[:5]
        save_draw_log(draw_log)

    st.markdown("---")
    st.header("🎴 最近5筆抽籤紀錄")
    draw_log = load_draw_log()
    for i, entry in enumerate(draw_log):
        st.write(f"第 {i+1} 次抽籤：")
        for box_title, picks in entry["result"].items():
            st.write(f"- **{box_title}**: {', '.join(picks) if picks else '未抽取'}")
        titles = entry.get("titles", [])
        st.write("推薦標題： " + ", ".join(titles))
        st.markdown("---")

if __name__ == "__main__":
    init_boxes(st.session_state.num_boxes)
    main()
