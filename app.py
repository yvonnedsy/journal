#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 17:23:18 2025

@author: shuyuandai
"""

import streamlit as st
import random
import datetime
import pytz

# 设置时区
BEIJING_TZ = pytz.timezone('Asia/Shanghai')

# 用户数据
user_profiles = [
    {
        "id": "user_1",
        "name": "ddd",
        "password": "981003",
        "data": [
            {
                "id": "color",
                "name": "颜色",
                "items": [
                    {
                        "id": "c1",
                        "template": "使用【】色系",
                        "type": "list",
                        "options": "蓝,绿,红,黄,橙,黑,紫,蓝黄,紫黄,蓝红,绿黄,灰,低饱和,荧光,蓝黑,绿黑,黑红,黄黑"
                    }
                ]
            },
            {
                "id": "tape",
                "name": "胶带",
                "items": [
                    {
                        "id": "t1",
                        "template": "使用第【】个分装版",
                        "type": "range",
                        "min": 1,
                        "max": 90
                    }
                ]
            },
            {
                "id": "release_book",
                "name": "离型本",
                "items": [
                    {
                        "id": "r1",
                        "template": "使用【】离型本",
                        "type": "list",
                        "options": "橙色,粉色,白色,小黄,小绿,小红"
                    }
                ]
            },
            {
                "id": "stamp",
                "name": "印章",
                "items": [
                    {
                        "id": "s1",
                        "template": "使用【】号印章盒",
                        "type": "range",
                        "min": 1,
                        "max": 16
                    },
                    {
                        "id": "s2",
                        "template": "使用【】印章",
                        "type": "list",
                        "options": "松川,makkey,大宇人,som,青空亭,熊猫,tai,文字,熊猫日志"
                    }
                ]
            },
            {
                "id": "note",
                "name": "便签",
                "items": [
                    {
                        "id": "n1",
                        "template": "本页不使用便签",
                        "type": "fixed",
                    },
                    {
                        "id": "n2",
                        "template": "至少使用【】张便签",
                        "type": "range",
                        "min": 1,
                        "max": 4
                    },
                    {
                        "id": "n3",
                        "template": "使用【】便签",
                        "type": "list",
                        "options": "古川纸工,表现社,4legs,一笔笺,小方,papier,便签卷"
                    },
                    {
                        "id": "n4",
                        "template": "使用第【】张一笔笺",
                        "type": "range",
                        "min": 1,
                        "max": 50,
                    }
                ]
            }
        ]
    },
    {
        "id": "user_2",
        "name": "lulu",
        "password": "981003",
        "data": [
            {
                "id": "color",
                "name": "颜色",
                "items": [
                    {
                        "id": "c1",
                        "template": "使用【】色系",
                        "type": "list",
                        "options": "蓝,绿,红,黄,橙,黑,紫,蓝黄,紫黄,蓝红,绿黄,灰,低饱和,荧光,蓝黑,绿黑,黑红,黄黑"
                    }
                ]
            },
            {
                "id": "tape",
                "name": "胶带",
                "items": [
                    {
                        "id": "t1",
                        "template": "使用第【】个分装版",
                        "type": "range",
                        "min": 1,
                        "max": 15
                    }
                ]
            },
            {
                "id": "release_book",
                "name": "离型本",
                "items": [
                    {
                        "id": "r1",
                        "template": "使用【】离型本",
                        "type": "list",
                        "options": "绿色,护照,标准"
                    }
                ]
            },
            {
                "id": "stamp",
                "name": "印章",
                "items": [
                    {
                        "id": "s1",
                        "template": "使用【】号印章盒",
                        "type": "range",
                        "min": 1,
                        "max": 3
                    },
                    {
                        "id": "s2",
                        "template": "使用【】印章",
                        "type": "list",
                        "options": "松川,makkey,熊猫,7uly,文字"
                    }
                ]
            },
            {
                "id": "note",
                "name": "便签",
                "items": [
                    {
                        "id": "n1",
                        "template": "本页不使用便签",
                        "type": "fixed",
                    },
                    {
                        "id": "n2",
                        "template": "至少使用【】张便签",
                        "type": "range",
                        "min": 1,
                        "max": 4
                    },
                    {
                        "id": "n3",
                        "template": "使用【】便签",
                        "type": "list",
                        "options": "表现社,一笔笺,小方,便签卷"
                    }
                ]
            }
        ]
    }
]

# 获取用户资料
def get_user_profile(username):
    for user in user_profiles:
        if user["name"] == username:
            return user
    return None

# 选择用户
selected_user = st.sidebar.selectbox("选择用户", options=[user['name'] for user in user_profiles])
current_profile = get_user_profile(selected_user)

# 主页面逻辑
st.header(f"✨ 手帐挑战: {current_profile['name']}")

tab1, tab2 = st.tabs(["🎲 挑战抽取", "⚙️ 栏目维护"])

# === TAB 1: 挑战抽取 ===
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📅 每日挑战\n(固定命题)", use_container_width=True):
            st.session_state.generate_type = "daily"
            st.session_state.trigger_gen = True
            
    with col2:
        if st.button("🎲 手气一下\n(完全随机)", use_container_width=True):
            st.session_state.generate_type = "random"
            st.session_state.trigger_gen = True

    # 执行生成逻辑
    if st.session_state.get("trigger_gen"):
        is_daily = st.session_state.generate_type == "daily"
        
        if is_daily:
            # 使用北京时间作为种子
            beijing_now = datetime.datetime.now(BEIJING_TZ)
            seed_str = beijing_now.strftime("%Y%m%d")
            random.seed(seed_str)
            time_display = beijing_now.strftime("%Y-%m-%d")
        else:
            random.seed(None)
            time_display = datetime.datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M")
        
        # 从当前选择的用户中取数据
        active_categories = current_profile['data']
        results = []
        
        # 找到胶带类别
        tape_cat = next((c for c in active_categories if c['id'] == 'tape' or '胶带' in c['name']), None)
        if not tape_cat and active_categories: tape_cat = active_categories[0]
        
        others = [c for c in active_categories if c != tape_cat]
        count = min(random.randint(1, 2), len(others))
        selected_others = random.sample(others, count)
        final_cats = ([tape_cat] if tape_cat else []) + selected_others
        
        for cat in final_cats:
            if not cat['items']: continue
            item = random.choice(cat['items'])
            text = item['template']
            
            val_str = ""
            if item['type'] == 'fixed':
                val_str = ""
            elif item['type'] == 'range':
                val = random.randint(int(item.get('min', 1)), int(item.get('max', 10)))
                val_str = str(val)
            elif item['type'] == 'list':
                opts = [x.strip() for x in item.get('options', '').replace('，', ',').split(',') if x.strip()]
                val_str = random.choice(opts) if opts else "???"
                
            if '【】' in text:
                text = text.replace('【】', f" **{val_str}** ")
            
            results.append({"cat": cat['name'], "text": text})
            
        st.session_state.result = {
            "type": "每日挑战" if is_daily else "随机挑战",
            "time": time_display,
            "items": results
        }
        st.session_state.trigger_gen = False 
        if is_daily: random.seed(None)

    # 显示结果
    if "result" in st.session_state:
        res = st.session_state.result
        st.markdown(f"""
        <div class="result-box">
            <h3>{res['type']} <span style="font-size:0.6em;color:#666">{res['time']}</span></h3>
            <hr style="margin: 10px 0; border-top: 1px solid #eee;">
        """, unsafe_allow_html=True)
        
        for item in res['items']:
            st.markdown(f"**🔵 {item['cat']}**: {item['text']}")
            
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👈 点击上方按钮开始抽取")
