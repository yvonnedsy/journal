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

# --- 常量定义 ---
# 定义北京时间时区 (UTC+8)
BEIJING_TZ = datetime.timezone(datetime.timedelta(hours=8))

# 初始数据模板
def get_initial_data():
    return [
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
            "options": "松川,makkey,大宇人,som,青空亭,熊猫,tai,文字"
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
            "options": ""
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
            "id": "1764167983.683707",
            "template": "使用第【】张一笔笺",
            "type": "range",
            "options": "A,B",
            "min": 1,
            "max": 50
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
            "options": "松川,makkey,大宇人,som,青空亭,熊猫,tai,文字"
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
            "options": ""
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
          }
        ]
      }
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
    }
    .card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
    }
    .result-box {
        background-color: #ffffff;
        color: #333333 !important;
        padding: 15px 20px; 
        border-radius: 12px;
        border-left: 5px solid #6366f1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-top: 15px;
    }
    .result-box h3 {
        color: #333333 !important;
        margin-top: 0;
    }
    .result-box strong {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 数据管理函数 ---
def load_profiles():
    data = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            pass
    
    if not data:
        # 为用户 ddd 和 lulu 初始化不同的数据
        data = [
            {"id": "user_1", "name": "ddd", "password": "981003", "data": get_initial_data()},
            {"id": "user_2", "name": "lulu", "password": "981003", "data": get_initial_data()}
        ]
    
    # 数据迁移：确保老数据也有 password 字段
    for p in data:
        if "password" not in p:
            p['password'] = "981003"  # 使用统一密码作为示例
    
    return data

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

# 解锁状态存储：格式为 {"user_id": True/False}
if 'unlocked_status' not in st.session_state:
    st.session_state.unlocked_status = {}

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
        st.session_state.result = None 
        st.session_state.unlocked_status = {}
        st.rerun()

    current_profile = st.session_state.profiles[st.session_state.active_user_index]
    current_uid = current_profile['id']

    st.divider()

    # 添加新用户
    with st.expander("➕ 添加新用户"):
        new_user_name = st.text_input("新用户名称")
        new_user_pass = st.text_input("设置6位数字密码", max_chars=6, type="password")
        
        if st.button("创建用户"):
            if new_user_name and new_user_pass:
                if len(new_user_pass) != 6 or not new_user_pass.isdigit():
                    st.error("密码必须是6位数字！")
                else:
                    new_profile = {
                        "id": f"user_{datetime.datetime.now().timestamp()}",
                        "name": new_user_name,
                        "password": new_user_pass,
                        "data": get_initial_data()  # 新用户的数据使用初始模板
                    }
                    st.session_state.profiles.append(new_profile)
                    save_profiles()
                    st.session_state.active_user_index = len(st.session_state.profiles) - 1
                    st.success(f"用户 {new_user_name} 创建成功！")
                    st.rerun()
            else:
                st.error("名称和密码不能为空")
    
    # 删除用户 (需要先解锁)
    if len(st.session_state.profiles) > 1:
        if st.session_state.unlocked_status.get(current_uid, False):
             with st.expander("🗑️ 删除用户"):
                 st.warning("删除后无法恢复！")
                 if st.button("确认删除当前用户", type="primary"):
                    st.session_state.profiles.pop(st.session_state.active_user_index)
                    st.session_state.active_user_index = 0
                    st.session_state.unlocked_status = {}
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
        
        if is_daily:
            # 使用北京时间作为种子
            beijing_now = datetime.datetime.now(BEIJING_TZ)
            seed_str = beijing_now.strftime("%Y%m%d")
            random.seed(seed_str)
            time_display = beijing_now.strftime("%Y-%m-%d")
        else:
            random.seed(None)
            time_display = datetime.datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M")
            
        active_categories = current_profile['data']
        results = []
        
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
            else: 
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
    if st.session_state.result:
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

# === TAB 2: 栏目维护 (带密码锁) ===
with tab2:
    is_unlocked = st.session_state.unlocked_status.get(current_uid, False)

    if not is_unlocked:
        st.warning("🔒 该区域受密码保护")
        col_pwd_1, col_pwd_2 = st.columns([3, 1])
        input_pwd = col_pwd_1.text_input("请输入密码进行编辑", type="password", key="unlock_input")
        if col_pwd_2.button("🔓 解锁编辑", key="btn_unlock"):
            if input_pwd == current_profile.get('password'):
                st.session_state.unlocked_status[current_uid] = True
                st.rerun()
            else:
                st.error("密码错误！")
    else:
        st.success(f"🔓 已解锁编辑权限")
        st.caption("⚠️ 修改后会自动保存。刷新页面需重新解锁。")
        
        categories = current_profile['data']
        
        for i, cat in enumerate(categories):
            with st.expander(f"📁 {cat['name']} ({len(cat['items'])}条规则)"):
                
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
                
                for j, item in enumerate(cat['items']):
                    c1, c2, c3, c4 = st.columns([2, 1.5, 2, 0.5])
                    
                    new_tmpl = c1.text_input("语句模板", item['template'], key=f"t_{i}_{j}", placeholder="例如: 使用【】色系")
                    if new_tmpl != item['template']:
                        item['template'] = new_tmpl
                        save_profiles()

                    type_map = {"list": "文字列表", "range": "数字范围", "fixed": "固定语句"}
                    rev_map = {v: k for k, v in type_map.items()}
                    
                    curr_type_display = type_map.get(item['type'], "文字列表")
                    new_type_display = c2.selectbox("类型", list(type_map.values()), index=list(type_map.values()).index(curr_type_display), key=f"sel_{i}_{j}")
                    new_type = rev_map[new_type_display]
                    
                    if new_type != item['type']:
                        item['type'] = new_type
                        if new_type == 'range':
                            item['min'] = 1
                            item['max'] = 10
                        elif new_type == 'list':
                            item['options'] = ""
                        save_profiles()
                        st.rerun()

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

                    if c4.button("x", key=f"del_item_{i}_{j}"):
                        cat['items'].pop(j)
                        save_profiles()
                        st.rerun()

                if st.button("➕ 添加一条规则", key=f"add_item_{i}"):
                    cat['items'].append({
                        "id": str(datetime.datetime.now().timestamp()), 
                        "template": "使用【】", 
                        "type": "list", 
                        "options": "A,B"
                    })
                    save_profiles()
                    st.rerun()

        st.divider()
        if st.button("✨ 添加一个新素材栏目 (例如: 贴纸/特殊任务)", use_container_width=True):
            categories.append({
                "id": str(datetime.datetime.now().timestamp()),
                "name": "新栏目",
                "items": [{"id": "new", "template": "使用【】", "type": "list", "options": "选项1,选项2"}]
            })
            save_profiles()
            st.rerun()
