import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from scipy.interpolate import CubicSpline
import numpy as np

def plot_funnel_chart(df: pd.DataFrame) -> go.Figure:
    """Plot the user behavior conversion funnel."""
    behavior_order = ['点击', '加购', '收藏', '购买']
    counts = df['behavior_cn'].value_counts()
    
    # Ensure all categories exist even if count is 0
    data = [counts.get(b, 0) for b in behavior_order]
    
    fig = go.Figure(go.Funnel(
        y=behavior_order,
        x=data,
        textposition="inside",
        textinfo="value+percent initial",
        marker={"color": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]},
        connector={"line": {"color": "royalblue", "dash": "dash", "width": 3}}
    ))
    fig.update_layout(title="用户行为转化漏斗", height=400)
    return fig

def plot_weekly_trend(df: pd.DataFrame) -> go.Figure:
    """Plot weekly behavior trends with smoothing."""
    weekday_labels = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}
    weekly_data = df.groupby(['weekday', 'behavior_type']).size().reset_index(name='count')
    
    fig = go.Figure()
    
    behaviors = df['behavior_type'].unique()
    colors = px.colors.qualitative.Set1
    
    for i, behavior in enumerate(behaviors):
        subset = weekly_data[weekly_data['behavior_type'] == behavior]
        x = subset['weekday'].values
        y = subset['count'].values
        
        # Apply Cubic Spline smoothing as in original notebook
        if len(x) > 3:
            cs = CubicSpline(x, y, bc_type='natural')
            x_smooth = np.linspace(x.min(), x.max(), 100)
            y_smooth = cs(x_smooth)
            # Map smooth x back to labels for display (approximate)
            x_labels = [weekday_labels.get(int(round(val)), str(val)) for val in x_smooth]
            fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name=behavior, line=dict(color=colors[i])))
        else:
            fig.add_trace(go.Bar(x=[weekday_labels[val] for val in x], y=y, name=behavior, marker_color=colors[i]))

    fig.update_layout(title="周内用户行为趋势分析", xaxis_title="星期", yaxis_title="行为次数")
    return fig

def plot_hourly_activity(df: pd.DataFrame) -> go.Figure:
    """Plot hourly user activity."""
    hourly_active = df.groupby('hour')['user_id'].nunique().reset_index(name='active_users')
    
    fig = px.line(hourly_active, x='hour', y='active_users', markers=True, 
                  title="24小时活跃用户分布", labels={'hour': '小时', 'active_users': '活跃人数'})
    fig.update_traces(line_color='#ff7f0e', line_width=3)
    return fig

def plot_rfm_distribution(rfm_df: pd.DataFrame) -> go.Figure:
    """Plot RFM user segmentation distribution."""
    if rfm_df.empty:
        return go.Figure()
        
    segment_counts = rfm_df['Segment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Count']
    
    fig = px.pie(segment_counts, values='Count', names='Segment', 
                 title="RFM 用户价值分层占比",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    return fig
