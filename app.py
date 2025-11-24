#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 21:32:36 2025

@author: shuyuandai
"""


import streamlit as st
import json
import random
import datetime
import os
import copy

# --- 页面配置 ---
st.set_page_config(
    page_title="手帐灵感生成器",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- 初始默认数据 (复刻 React 版) ---
INITIAL_DATA = [
    {
        "id": "color", "name": "颜色",
        "items": [{"id": "c1", "template": "使用【】色系", "type": "list", "options": "蓝,绿,红,黄,橙,黑,紫,蓝黄,紫黄,蓝红,绿黄,灰,低饱和,荧光,蓝黑,绿黑,黑红,黄黑"}]
    },
    {
        "id": "tape", "name": "胶带",
        "items": [{"id": "t1", "template": "使用第【】个分装版", "type": "range", "min": 1, "max": 90}]
    },
    {
        "id": "release_book", "name": "离型本",
        "items": [{"id": "r1", "template": "使用【】离型本", "type": "list", "options": "橙色,粉色,白色,小黄,小绿,小红"}]
    },
    {
        "id": "stamp", "name": "印章",
        "items": [
            {"id": "s1", "template": "使用【】号印章盒", "type": "range", "min": 1, "max": 16},
            {"id": "s2", "template": "使用【】印章", "type": "list", "options": "松川,makkey,大宇人,som,青空亭,熊猫,tai,文字"}
        ]
    },
    {
        "id": "note", "name": "便签",
        "items": [
            {"id": "n1", "template": "本页不使用便签", "type": "fixed", "options": ""},
            {"id": "n2", "template": "至少使用【】张便签", "type": "range", "min": 1, "max": 4},
            {"id": "n3", "template": "使用【】便签", "type": "list", "options": "古川纸工,表现社,4legs,一笔笺,小方,papier,便签卷"}
        ]
    }
]

DATA_FILE = "journal_profiles.json"

# --- 自定义 CSS 美化 ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
    }
    .big-btn {
        font-size: 20px !important;
        padding: 20px !important;
    }
    .card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    .result-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #6366f1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- 数据管理函数 ---
def load_profiles():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    # 默认初始化
    return [{"id": "user_1", "name": "默认用户", "data": copy.deepcopy(INITIAL_DATA)}]

def save_profiles():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.profiles, f, ensure_ascii=False, indent=2)

# --- 初始化 Session State ---
if 'profiles' not in st.session_state:
    st.session_state.profiles = load_profiles()

if 'active_user_index' not in st.session_state:
    st.session_state.active_user_index = 0

if 'result' not in st.session_state:
    st.session_state.result = None

# --- 侧边栏：用户管理 ---
with st.sidebar:
    st.title("👤 用户管理")
    
    # 用户选择
    user_names = [p['name'] for p in st.session_state.profiles]
    selected_name = st.selectbox(
        "当前用户", 
        user_names, 
        index=st.session_state.active_user_index
    )
    
    # 更新 active_index
    new_index = user_names.index(selected_name)
    if new_index != st.session_state.active_user_index:
        st.session_state.active_user_index = new_index
        st.session_state.result = None # 切换用户清除结果
        st.rerun()

    current_profile = st.session_state.profiles[st.session_state.active_user_index]

    # 添加新用户
    with st.expander("➕ 添加新用户"):
        new_user_name = st.text_input("新用户名称")
        if st.button("创建用户"):
            if new_user_name:
                new_profile = {
                    "id": f"user_{datetime.datetime.now().timestamp()}",
                    "name": new_user_name,
                    "data": copy.deepcopy(INITIAL_DATA)
                }
                st.session_state.profiles.append(new_profile)
                save_profiles()
                st.session_state.active_user_index = len(st.session_state.profiles) - 1
                st.rerun()
    
    # 修改/删除用户
    with st.expander("✏️ 编辑当前用户"):
        edit_name = st.text_input("修改名称", value=current_profile['name'])
        if st.button("保存名称"):
            current_profile['name'] = edit_name
            save_profiles()
            st.rerun()
            
        if len(st.session_state.profiles) > 1:
            if st.button("🗑️ 删除此用户", type="primary"):
                st.session_state.profiles.pop(st.session_state.active_user_index)
                st.session_state.active_user_index = 0
                save_profiles()
                st.rerun()

# --- 主页面逻辑 ---
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
        
        # 设置随机种子
        if is_daily:
            seed_str = datetime.date.today().strftime("%Y%m%d")
            random.seed(seed_str)
        else:
            random.seed(None) # 真正的随机
            
        active_categories = current_profile['data']
        results = []
        
        # 1. 找胶带 (ID为tape或名字含胶带)
        tape_cat = next((c for c in active_categories if c['id'] == 'tape' or '胶带' in c['name']), None)
        # 如果没找到胶带，强制用第一个
        if not tape_cat and active_categories: tape_cat = active_categories[0]
        
        # 2. 其他栏目
        others = [c for c in active_categories if c != tape_cat]
        
        # 3. 随机选 1-2 个其他
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
            else: # list
                opts = [x.strip() for x in item.get('options', '').replace('，', ',').split(',') if x.strip()]
                val_str = random.choice(opts) if opts else "???"
                
            if '【】' in text:
                text = text.replace('【】', f" **{val_str}** ")
            
            results.append({"cat": cat['name'], "text": text})
            
        st.session_state.result = {
            "type": "每日挑战" if is_daily else "随机挑战",
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "items": results
        }
        st.session_state.trigger_gen = False # 重置触发器
        if is_daily: random.seed(None) # 恢复随机状态

    # 显示结果
    if st.session_state.result:
        res = st.session_state.result
        st.markdown(f"""
        <div class="result-box">
            <h3>{res['type']} <span style="font-size:18pt;color:gray">{res['time']}</span></h3>
            <hr style="margin: 10px 0;">
        """, unsafe_allow_html=True)
        
        for item in res['items']:
            st.markdown(f"**🔵 {item['cat']}**: {item['text']}")
            
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("👈 点击上方按钮开始抽取")


# === TAB 2: 栏目维护 ===
with tab2:
    st.caption("这里可以修改属于你的规则库。修改后会自动保存。")
    
    # 遍历分类
    categories = current_profile['data']
    
    for i, cat in enumerate(categories):
        with st.expander(f"📁 {cat['name']} ({len(cat['items'])}条规则)"):
            
            # 修改栏目名
            col_name, col_del = st.columns([3, 1])
            new_cat_name = col_name.text_input("栏目名称", cat['name'], key=f"cat_name_{i}")
            if new_cat_name != cat['name']:
                cat['name'] = new_cat_name
                save_profiles()
                
            if col_del.button("🗑️ 删除栏目", key=f"del_cat_{i}"):
                if cat['id'] == 'tape':
                    st.error("核心胶带栏目不能删除！")
                else:
                    categories.pop(i)
                    save_profiles()
                    st.rerun()
            
            st.divider()
            
            # 遍历规则
            for j, item in enumerate(cat['items']):
                c1, c2, c3, c4 = st.columns([2, 1.5, 2, 0.5])
                
                # 1. 模板
                new_tmpl = c1.text_input("语句模板", item['template'], key=f"t_{i}_{j}", placeholder="例如: 使用【】色系")
                if new_tmpl != item['template']:
                    item['template'] = new_tmpl
                    save_profiles()

                # 2. 类型
                type_map = {"list": "文字列表", "range": "数字范围", "fixed": "固定语句"}
                rev_map = {v: k for k, v in type_map.items()}
                
                curr_type_display = type_map.get(item['type'], "文字列表")
                new_type_display = c2.selectbox("类型", list(type_map.values()), index=list(type_map.values()).index(curr_type_display), key=f"sel_{i}_{j}")
                new_type = rev_map[new_type_display]
                
                if new_type != item['type']:
                    item['type'] = new_type
                    # 重置数据结构以防报错
                    if new_type == 'range':
                        item['min'] = 1
                        item['max'] = 10
                    elif new_type == 'list':
                        item['options'] = ""
                    save_profiles()
                    st.rerun()

                # 3. 内容
                if item['type'] == 'list':
                    new_opt = c3.text_input("选项 (逗号隔开)", item.get('options', ''), key=f"opt_{i}_{j}")
                    if new_opt != item.get('options', ''):
                        item['options'] = new_opt
                        save_profiles()
                elif item['type'] == 'range':
                    rc1, rc2 = c3.columns(2)
                    new_min = rc1.number_input("小", value=int(item.get('min', 1)), key=f"min_{i}_{j}")
                    new_max = rc2.number_input("大", value=int(item.get('max', 10)), key=f"max_{i}_{j}")
                    if new_min != item.get('min') or new_max != item.get('max'):
                        item['min'] = new_min
                        item['max'] = new_max
                        save_profiles()
                else:
                    c3.text("无随机内容")

                # 4. 删除规则
                if c4.button("x", key=f"del_item_{i}_{j}"):
                    cat['items'].pop(j)
                    save_profiles()
                    st.rerun()

            # 添加新规则按钮
            if st.button("➕ 添加一条规则", key=f"add_item_{i}"):
                cat['items'].append({
                    "id": str(datetime.datetime.now().timestamp()), 
                    "template": "使用【】", 
                    "type": "list", 
                    "options": "A,B"
                })
                save_profiles()
                st.rerun()

    # 添加新栏目
    st.divider()
    if st.button("✨ 添加一个新素材栏目 (例如: 贴纸/特殊任务)", use_container_width=True):
        categories.append({
            "id": str(datetime.datetime.now().timestamp()),
            "name": "新栏目",
            "items": [{"id": "new", "template": "使用【】", "type": "list", "options": "选项1,选项2"}]
        })
        save_profiles()
        st.rerun()
