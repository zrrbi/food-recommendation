# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 17:10:45 2025
@author: rouren
"""

import streamlit as st
import pandas as pd
import random
from itertools import combinations
import os

# 设置页面信息
st.set_page_config(page_title="今天吃什么", page_icon="🍽️", layout="centered")

# 🔥 UI 样式美化
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #FFFAF0, #FFF5EE);  /* 渐变背景 */
    }
    .title {
        font-size: 34px !important;
        font-weight: bold !important;
        color: #2c3e50 !important;
        text-align: center;
        padding: 20px 0;
    }
    .slider-container {
        background: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .slider-label {
        font-size: 18px;
        font-weight: bold;
        color: #D35400;
        margin-bottom: 5px;
    }
    .recommend-box {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
        border-left: 5px solid #FFA500;
    }
    .recommend-box h3 {
        color: #D35400;
        margin-bottom: 5px;
    }
    .recommend-box p {
        font-size: 16px;
        color: #2c3e50;
        margin: 3px 0;
    }
    .summary-box {
        background: #ffefd5;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        text-align: center;
        font-weight: bold;
    }
    .summary-value {
        font-size: 24px;
        font-weight: bold;
        color: #D35400;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 标题
st.markdown('<h1 class="title">What Should I Eat Today?</h1>', unsafe_allow_html=True)

# 读取数据
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "menu.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ 文件未找到: {csv_path}")

df = pd.read_csv(csv_path)

# 推荐算法
def recommend_food(max_calories, max_price):
    # 筛选符合预算要求的菜品
    filtered_df = df[df["价格($)"] <= max_price].copy()

    if filtered_df.empty:
        return pd.DataFrame(columns=["店名", "菜品", "热量(kcal)", "价格($)"]), 0, 0

    possible_combinations = []
    for r in range(2, 5):  # 组合 2 到 4 个菜品
        for combo in combinations(filtered_df.itertuples(index=False, name=None), r):
            total_calories = sum(item[2] for item in combo)  # item[2] 是 热量(kcal)
            total_price = sum(item[3] for item in combo)  # item[3] 是 价格($)
            unique_restaurants = {item[0] for item in combo}  # item[0] 是 店名

            if total_calories <= max_calories and total_price <= max_price and len(unique_restaurants) <= 2:
                possible_combinations.append((combo, total_calories, total_price))

    if not possible_combinations:
        return pd.DataFrame(columns=["店名", "菜品", "热量(kcal)", "价格($)"]), 0, 0

    # 按照总热量最接近 max_calories 排序，选出最优的
    best_combinations = sorted(possible_combinations, key=lambda x: abs(x[1] - max_calories))
    selected_combo, total_calories, total_price = random.choice(best_combinations)

    selected_df = pd.DataFrame(
        [(item[0], item[1], item[2], item[3]) for item in selected_combo],
        columns=["店名", "菜品", "热量(kcal)", "价格($)"]
    )

    return selected_df, total_calories, round(total_price, 2)

# 用户输入
st.markdown('<div class="slider-container">', unsafe_allow_html=True)

st.markdown('<p class="slider-label">🔥 Select Calorie Limit</p>', unsafe_allow_html=True)
max_calories = st.slider(
    "",
    min_value=200,
    max_value=1200,
    value=400,
    step=50,
    format="%d kcal",
    help="Select Your Desired Maximum Calories"
)

st.markdown('<p class="slider-label">💰 Select Budget</p>', unsafe_allow_html=True)
max_price = st.slider(
    "",
    min_value=10,
    max_value=50,
    value=30,
    step=5,
    format="$%d",
    help="Select the Maximum Amount You’re Willing to Pay"
)

st.markdown('</div>', unsafe_allow_html=True)  # 结束滑块容器

st.markdown("<hr>", unsafe_allow_html=True)

# 获取推荐
if st.button("🔍 Get Recommendations"):
    result, total_calories, total_price = recommend_food(max_calories, max_price)

    if not result.empty:
        st.markdown("## Recommended Takeout Options 🍽️")

        # 卡片式显示推荐菜品
        for _, row in result.iterrows():
            st.markdown(
                f"""
                <div class="recommend-box">
                    <h3>{row['店名']}</h3>
                    <p><b>Dish：</b> {row['菜品']}</p>
                    <p><b>Calories：</b> {row['热量(kcal)']} kcal</p>
                    <p><b>Price：</b> ${row['价格($)']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        # 卡片式显示总热量和总价格
        st.markdown(
            f"""
            <div class="summary-box">
            <p class="summary-title">🍽️ Your Selection</p>
            <p class="summary-value">🔥 Total Calories: {total_calories} kcal</p>
            <p class="summary-value">💰 Total Price: ${total_price}</p> 
            </div>
            """,
            unsafe_allow_html=True
            )

    else:
        st.warning("⚠️ 没有符合条件的外卖，请调整热量或预算！")
