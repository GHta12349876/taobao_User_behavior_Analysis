import streamlit as st
import pandas as pd

def generate_basic_insights(df: pd.DataFrame, rfm_df: pd.DataFrame) -> None:
    """
    Generate comprehensive rule-based business insights.

    Covers four dimensions based on README analysis conclusions:
    1. Conversion funnel diagnosis (pv→cart bottleneck, cart→buy, fav→buy)
    2. Time dimension insights (dual peaks, weekend effect)
    3. RFM user segmentation with differentiated strategies
    4. Comprehensive business recommendations
    """
    st.subheader("🤖 AI 业务洞察")

    # ---- Pre-compute shared metrics ----
    pv_count = len(df[df['behavior_type'] == 'pv'])
    cart_count = len(df[df['behavior_type'] == 'cart'])
    fav_count = len(df[df['behavior_type'] == 'fav'])
    buy_count = len(df[df['behavior_type'] == 'buy'])

    # ================================================================
    # Section 1: Conversion Funnel Diagnosis
    # ================================================================
    with st.expander("📊 转化漏斗诊断", expanded=True):
        if pv_count > 0:
            pv_to_cart_rate = (cart_count / pv_count) * 100
            cart_to_buy_rate = (buy_count / cart_count * 100) if cart_count > 0 else 0
            fav_to_buy_rate = (buy_count / fav_count * 100) if fav_count > 0 else 0
            cart_no_buy_rate = 100 - cart_to_buy_rate if cart_count > 0 else 0

            # --- 1a: pv → cart (core pain point) ---
            st.markdown("##### 🔴 浏览 → 加购（核心痛点）")
            st.progress(min(pv_to_cart_rate / 15, 1.0), text=f"转化率 {pv_to_cart_rate:.2f}%")
            if pv_to_cart_rate < 10:
                st.warning(
                    f"⚠️ **浏览到加购转化率偏低 ({pv_to_cart_rate:.2f}%)**，"
                    f"这是用户流失最严重的环节，绝大多数用户在浏览后未采取进一步行动。\n\n"
                    f"> **建议**：优化商品详情页展示质量（图文内容、评价权重、价格锚点设计），"
                    f"增加个性化推荐模块，降低用户决策成本，提升加购意愿。"
                )
            else:
                st.success(
                    f"✅ **浏览到加购转化率正常 ({pv_to_cart_rate:.2f}%)**：用户对当前选品兴趣较高。"
                )

            # --- 1b: cart → buy (cart abandonment) ---
            if cart_count > 0:
                st.markdown("##### 🟡 加购 → 购买（付款流失）")
                st.progress(min(cart_to_buy_rate / 80, 1.0), text=f"转化率 {cart_to_buy_rate:.2f}%")
                if cart_no_buy_rate > 25:
                    st.warning(
                        f"⚠️ **加购未付款率 {cart_no_buy_rate:.1f}%**，高于行业平均水平（~25%），"
                        f"约 1/3 的加购行为在付款环节流失。\n\n"
                        f"> **建议**：通过购物车提醒推送（站内消息或 App 通知）、限时优惠券触发、"
                        f"库存紧张提示等策略，对加购未付款用户进行定向召回，缩短从加购到付款的决策周期。"
                    )
                else:
                    st.info(
                        f"ℹ️ **加购未付款率 {cart_no_buy_rate:.1f}%**，处于合理范围。"
                        f"建议持续关注此指标，维持购物车提醒推送机制。"
                    )

            # --- 1c: fav → buy (efficient conversion path) ---
            if fav_count > 0:
                st.markdown("##### 🟢 收藏 → 购买（高效转化路径）")
                st.progress(min(fav_to_buy_rate / 80, 1.0), text=f"转化率 {fav_to_buy_rate:.2f}%")
                st.success(
                    f"✅ **收藏到购买转化率 ({fav_to_buy_rate:.2f}%)**："
                    f"一旦用户将商品加入收藏夹，其购买意愿强烈且流失率较低，"
                    f"收藏行为是重要的购买前置信号。\n\n"
                    f"> **建议**：引导用户收藏商品（如收藏即享专属优惠），"
                    f"并将收藏夹作为精准营销触达渠道，对收藏未购用户推送限时提醒。"
                )

    # ================================================================
    # Section 2: Time Dimension Insights
    # ================================================================
    with st.expander("🕒 时间维度洞察", expanded=True):
        if not df.empty:
            hourly_active = df.groupby('hour')['user_id'].nunique()
            peak_hour = hourly_active.idxmax()
            peak_users = hourly_active.max()

            # Identify evening secondary peak (18:00-23:00)
            evening_data = hourly_active[hourly_active.index >= 18]
            secondary_hour = evening_data.idxmax() if not evening_data.empty else None

            # --- 2a: Intraday dual peaks ---
            st.markdown("##### 🌞 日内流量双高峰")
            peak_desc = f"午间主高峰 **{peak_hour}:00**（{peak_users:,} 活跃用户）"
            if secondary_hour is not None and secondary_hour != peak_hour:
                peak_desc += (
                    f"，夜间次高峰 **{secondary_hour}:00**"
                    f"（{hourly_active[secondary_hour]:,} 活跃用户）"
                )
            st.info(f"📈 {peak_desc}")
            st.caption(
                "> **建议**：将重要营销活动、新品上线、优惠券发放集中在 "
                "**11:00–14:00** 和 **20:00–23:00** 两个黄金时段，以实现最大曝光与转化效益。"
            )

            # --- 2b: Weekend effect ---
            st.markdown("##### 📅 周末效应")
            df_temp = df.copy()
            df_temp['is_weekend'] = df_temp['weekday'].isin([5, 6])
            weekend_pv = len(df_temp[(df_temp['is_weekend']) & (df_temp['behavior_type'] == 'pv')])
            weekday_pv = len(df_temp[(~df_temp['is_weekend']) & (df_temp['behavior_type'] == 'pv')])
            weekend_days = df_temp[df_temp['is_weekend']]['datetime'].dt.date.nunique()
            weekday_days = df_temp[~df_temp['is_weekend']]['datetime'].dt.date.nunique()

            if weekday_days > 0 and weekend_days > 0:
                avg_weekend_pv = weekend_pv / weekend_days
                avg_weekday_pv = weekday_pv / weekday_days
                weekend_ratio = avg_weekend_pv / avg_weekday_pv if avg_weekday_pv > 0 else 0
                st.info(
                    f"📈 周末日均浏览量是工作日的 **{weekend_ratio:.1f} 倍**"
                    f"（周末日均 {avg_weekend_pv:,.0f} vs 工作日日均 {avg_weekday_pv:,.0f}）。\n\n"
                    f"> **建议**：所有用户行为在周末（尤其是周六）显著增加，"
                    f"应将重大促销活动、广告投放和新品首发集中在周末执行。"
                )

    # ================================================================
    # Section 3: RFM User Segmentation Insights
    # ================================================================
    with st.expander("👥 RFM 用户分层洞察", expanded=True):
        if not rfm_df.empty:
            total_users = len(rfm_df)
            segment_counts = rfm_df['Segment'].value_counts()

            # --- 3a: 重要价值客户 (High-value) ---
            high_value_ratio = segment_counts.get('重要价值客户', 0) / total_users
            st.markdown("##### ⭐ 重要价值客户")
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.metric("占比", f"{high_value_ratio*100:.1f}%")
            with col_b:
                st.info(
                    f"平台核心收入来源（目标占比 ≥25%）。这部分用户贡献了较高的购买频率，"
                    f"是平台的忠实用户。\n\n"
                    f"> **建议**：提供专属权益（会员积分、优先客服、新品优先购），"
                    f"提升忠诚度与复购频率，并通过推荐机制扩大该群体规模。"
                )

            # --- 3b: 潜力客户 (Potential) ---
            potential_ratio = segment_counts.get('潜力客户', 0) / total_users
            st.markdown("##### 🌱 潜力客户")
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.metric("占比", f"{potential_ratio*100:.1f}%")
            with col_b:
                st.info(
                    f"近期有过购买但频次较低，具备较高转化潜力，"
                    f"是重要价值客户的「蓄水池」。\n\n"
                    f"> **建议**：通过个性化推荐和定向满减活动刺激二次购买，"
                    f"可有效将潜力客户转化为重要价值客户。"
                )

            # --- 3c: 高流失风险客户 (Churn risk) ---
            churn_risk_ratio = segment_counts.get('高流失风险客户', 0) / total_users
            st.markdown("##### 🚨 高流失风险客户")
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.metric("占比", f"{churn_risk_ratio*100:.1f}%")
            with col_b:
                if churn_risk_ratio > 0.05:
                    st.error(
                        f"⚠️ 占比 {churn_risk_ratio*100:.1f}%，高于警戒线（5%）。"
                        f"这部分用户曾为高频购买者，近期活跃度下降，挽回价值极高。\n\n"
                        f"> 🚨 **紧急建议**：通过专属折扣、一对一触达或客服回访进行重点召回，"
                        f"投入产出比远高于唤醒沉睡流失用户。"
                    )
                else:
                    st.success(
                        f"占比较低 ({churn_risk_ratio*100:.1f}%)，用户留存状况良好。"
                    )

            # --- 3d: 流失客户 (Lost) ---
            churn_ratio = segment_counts.get('流失客户', 0) / total_users
            st.markdown("##### ❄️ 流失客户")
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.metric("占比", f"{churn_ratio*100:.1f}%")
            with col_b:
                st.info(
                    f"占比最高 ({churn_ratio*100:.1f}%)，整体唤回成本较大，"
                    f"投入产出比相对较低。\n\n"
                    f"> **建议**：以低成本的内容推送为主（平台资讯、活动预告），"
                    f"不宜投入过重营销资源，优先聚焦中高价值群体。"
                )

            # --- 3e: Summary table ---
            st.markdown("##### 📋 分层数据汇总")
            summary_rows = []
            for seg in ['重要价值客户', '潜力客户', '高流失风险客户', '流失客户']:
                cnt = segment_counts.get(seg, 0)
                seg_df = rfm_df[rfm_df['Segment'] == seg]
                summary_rows.append({
                    '分层': seg,
                    '用户数': cnt,
                    '占比': f'{cnt/total_users*100:.1f}%',
                    '平均R(天)': f"{seg_df['Recency'].mean():.1f}" if cnt > 0 else '-',
                    '平均F(次)': f"{seg_df['Frequency'].mean():.1f}" if cnt > 0 else '-',
                })
            st.dataframe(
                pd.DataFrame(summary_rows),
                use_container_width=True,
                hide_index=True,
            )

    # ================================================================
    # Section 4: Comprehensive Business Recommendations
    # ================================================================
    with st.expander("📋 综合业务建议（五维策略）", expanded=False):
        st.markdown(
            """
        基于以上数据洞察，建议从以下五个方向推进运营优化：

        **① 优化浏览→加购转化路径（最高优先级）**
        - 改进商品详情页图文质量，突出评价权重和价格锚点设计
        - 部署个性化推荐模块，降低用户决策成本
        - 目标：将 pv→cart 转化率提升至 10% 以上

        **② 降低加购未付款流失率**
        - 建立购物车提醒推送机制（站内消息 + App 通知）
        - 设计限时优惠券触发策略，配合库存紧张提示
        - 目标：将加购未付款率从 ~27% 降至 20% 以下

        **③ 把握周末与双高峰时段**
        - 营销活动集中在周末（尤其是周六）执行
        - 每日 11:00–14:00 和 20:00–23:00 安排重要运营动作
        - 最大化曝光与转化效益

        **④ 提升中长期用户留存**
        - 在用户首访后第 5–7 天触发互动机制（个性化推荐、签到奖励、购后好评激励）
        - 延缓第 8 天左右的留存断崖下跌
        - 首周留存目标：稳定在 75% 以上

        **⑤ RFM 分层差异化运营**
        - **重要价值客户**：专属权益 + 会员体系强化 → 提升忠诚度与复购
        - **潜力客户**：定向满减 + 个性化推荐 → 刺激二次购买
        - **高流失风险客户**：专属折扣 + 一对一召回 → 挽回高价值用户
        - **流失客户**：低成本内容触达 → 保持品牌曝光，不过度投入
        """
        )
