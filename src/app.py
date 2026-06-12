import streamlit as st
import pandas as pd
from src.data_loader import load_raw_data, filter_and_clean_data
from src.rfm_engine import calculate_rfm
from src.visuals import plot_funnel_chart, plot_weekly_trend, plot_hourly_activity, plot_rfm_distribution
from src.ai_insights import generate_basic_insights

# Page Configuration
st.set_page_config(
    page_title="淘宝用户行为分析决策系统",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛒 淘宝用户行为分析决策系统")
st.markdown("基于 Vibe Coding 趋势构建的交互式数据看板，支持实时筛选与 RFM 策略模拟。")

# --- Sidebar: Global Filters ---
st.sidebar.header("🔍 全局筛选器")

# Load Raw Data Once (Cached)
with st.spinner("正在加载原始数据..."):
    raw_df = load_raw_data()

if raw_df.empty:
    st.stop()

# Date Filter
min_date = raw_df['datetime'].min().date()
max_date = raw_df['datetime'].max().date()
selected_dates = st.sidebar.date_input("日期范围", [min_date, max_date], min_value=min_date, max_value=max_date)

# Behavior Type Filter
behavior_options = ['点击', '加购', '收藏', '购买']
selected_behaviors = st.sidebar.multiselect("行为类型", behavior_options, default=behavior_options)

# Apply Filters Dynamically
if len(selected_dates) == 2:
    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1]) + pd.Timedelta(days=1)
    df_filtered = filter_and_clean_data(raw_df, start_date, end_date, selected_behaviors)
else:
    df_filtered = filter_and_clean_data(raw_df, None, None, selected_behaviors)

if df_filtered.empty:
    st.warning("当前筛选条件下没有数据，请调整筛选条件。")
    st.stop()

# --- Main Dashboard ---

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
total_users = df_filtered['user_id'].nunique()
pv_count = len(df_filtered[df_filtered['behavior_type'] == 'pv'])
cart_count = len(df_filtered[df_filtered['behavior_type'] == 'cart'])
conversion_rate = (cart_count / pv_count * 100) if pv_count > 0 else 0

col1.metric("活跃用户数", f"{total_users:,}")
col2.metric("总浏览量 (PV)", f"{pv_count:,}")
col3.metric("加购数量", f"{cart_count:,}")
col4.metric("浏览-加购转化率", f"{conversion_rate:.2f}%")

st.divider()

# Row 1: Funnel & Weekly Trend
c1, c2 = st.columns([1, 2])
with c1:
    st.plotly_chart(plot_funnel_chart(df_filtered), width='stretch')
with c2:
    st.plotly_chart(plot_weekly_trend(df_filtered), width='stretch')

# Row 2: RFM Strategy Simulator
st.subheader("📊 RFM 策略模拟器")
st.markdown("拖动滑块调整 R（最近购买时间）和 F（购买频次）的分层阈值，实时观察用户结构变化。")

# RFM Parameter Controls
rfm_col1, rfm_col2, rfm_col3, rfm_col4 = st.columns(4)
with rfm_col1:
    r_boundary_high = st.slider("R高分阈值 (天)", 0, 7, 2, help="距今天数≤此值获得高R分")
with rfm_col2:
    r_boundary_low = st.slider("R低分阈值 (天)", 3, 15, 6, help="距今天数>此值获得低R分")
with rfm_col3:
    f_boundary_low = st.slider("F低分阈值 (次)", 1, 5, 3, help="购买次数≤此值获得低F分")
with rfm_col4:
    f_boundary_high = st.slider("F高分阈值 (次)", 4, 15, 7, help="购买次数≥此值获得高F分")

# Calculate RFM with dynamic parameters
rfm_result = calculate_rfm(
    df_filtered, 
    r_boundary_high=r_boundary_high,
    r_boundary_low=r_boundary_low,
    f_boundary_low=f_boundary_low,
    f_boundary_high=f_boundary_high
)

# Display RFM Results
if not rfm_result.empty:
    rf1, rf2 = st.columns([2, 1])
    
    with rf1:
        st.plotly_chart(plot_rfm_distribution(rfm_result), width='stretch')
        
        st.dataframe(
            rfm_result.groupby('Segment').agg(
                用户数=('Recency', 'count'),
                平均距今天数=('Recency', 'mean'),
                平均购买频次=('Frequency', 'mean')
            ).round(2),
            use_container_width=True
        )
    
    with rf2:
        st.plotly_chart(plot_hourly_activity(df_filtered), width='stretch')
        st.caption("💡 提示：活跃时段可安排营销活动")
else:
    st.warning("当前筛选条件下没有购买数据，无法计算RFM指标。")
    st.plotly_chart(plot_hourly_activity(df_filtered), width='stretch')

# AI Insights Section
st.divider()
generate_basic_insights(df_filtered, rfm_result)

# Footer
st.markdown("---")
st.caption("数据来源：天池 UserBehavior 数据集 | 技术栈：Streamlit + Plotly + Pandas")
