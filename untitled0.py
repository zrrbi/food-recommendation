#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 17:10:45 2025

@author: rouren
"""

import streamlit as st
import pandas as pd
import random

# 读取菜单数据
df = pd.read_csv("/Users/rouren/Desktop/Python/food-recommendation/menu.csv")

def recommend_food(max_calories, max_price):
    filtered_df = df[(df["热量(kcal)"] <= max_calories) & (df["价格($)"] <= max_price)]
    
    if not filtered_df.empty:
        return filtered_df.sample(n=min(2, len(filtered_df)))
    else:
        return None

# Streamlit 前端界面
st.title("今天吃什么？")

# 用户输入
max_calories = st.slider("热量上限 (kcal)", min_value=200, max_value=800, value=400, step=50)
max_price = st.slider("预算 ($)", min_value=10, max_value=50, value=30, step=5)

if st.button("💡 获取推荐"):
    result = recommend_food(max_calories, max_price)
    if result is not None:
        st.write("🍜 **推荐外卖选项**：")
        st.dataframe(result)
    else:
        st.warning("⚠️ 没有符合的外卖，请调整热量或预算！")