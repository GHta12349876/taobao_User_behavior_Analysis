import streamlit as st
import pandas as pd

def generate_basic_insights(df: pd.DataFrame, rfm_df: pd.DataFrame) -> None:
    """Generate rule-based business insights."""
    st.subheader("🤖 AI 业务解读")
    
    # 1. Funnel Insight
    pv_count = len(df[df['behavior_type'] == 'pv'])
    cart_count = len(df[df['behavior_type'] == 'cart'])
    if pv_count > 0:
        pv_to_cart_rate = (cart_count / pv_count) * 100
        if pv_to_cart_rate < 10:
            st.warning(f"⚠️ **浏览到加购转化率偏低 ({pv_to_cart_rate:.2f}%)**：建议优化商品详情页展示，增加个性化推荐模块。")
        else:
            st.success(f"✅ **浏览到加购转化率正常 ({pv_to_cart_rate:.2f}%)**：用户对当前选品兴趣较高。")

    # 2. RFM Insight
    if not rfm_df.empty:
        high_value_ratio = len(rfm_df[rfm_df['Segment'] == '重要价值客户']) / len(rfm_df)
        if high_value_ratio < 0.25:
            st.info(f"💡 **核心用户占比 {high_value_ratio*100:.1f}%**：建议针对“潜力客户”开展定向满减活动，提升其购买频次。")
        
        churn_risk_ratio = len(rfm_df[rfm_df['Segment'] == '高流失风险客户']) / len(rfm_df)
        if churn_risk_ratio > 0.05:
            st.error(f"🚨 **高流失风险预警 ({churn_risk_ratio*100:.1f}%)**：这部分用户曾为高频购买者，建议通过专属折扣进行重点召回。")

    # 3. Time-based Insight
    if not df.empty:
        peak_hour = df.groupby('hour')['user_id'].nunique().idxmax()
        st.markdown(f"🕒 **流量高峰时段**：每日 **{peak_hour}:00** 左右活跃人数最多，建议在此时段安排营销活动或新品上线。")
