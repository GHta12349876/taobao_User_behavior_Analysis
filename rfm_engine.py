import pandas as pd

def calculate_rfm(df: pd.DataFrame, 
                  r_boundary_high: int = 2, 
                  r_boundary_low: int = 6,
                  f_boundary_low: int = 3,
                  f_boundary_high: int = 7) -> pd.DataFrame:
    """
    Calculate RFM metrics and segment users based on dynamic thresholds.
    
    Args:
        df: DataFrame containing user behavior data (must include 'user_id', 'behavior_type', 'datetime')
        r_boundary_high: Days threshold for high R score (days <= this gets score 4)
        r_boundary_low: Days threshold for low R score (days > this gets score 1)
        f_boundary_low: Count threshold for low F score (count <= this gets score 1)
        f_boundary_high: Count threshold for high F score (count > this gets score 4)
        
    Returns:
        DataFrame with Recency, Frequency, scores, and Segment labels.
    """
    # Filter for buy behaviors only
    df_buy = df[df['behavior_type'] == 'buy'].copy()
    if df_buy.empty:
        return pd.DataFrame()
    
    # Reference date (day after the data ends)
    now = pd.to_datetime('2017-12-04')
    
    # Calculate Recency (R)
    last_buy_time = df_buy.groupby('user_id')['datetime'].max()
    days_since_last_buy = (now - last_buy_time).dt.days
    
    # Calculate Frequency (F)
    buy_counts = df_buy.groupby('user_id').size()
    
    # Create RFM DataFrame
    rfm_df = pd.DataFrame({
        'Recency': days_since_last_buy,
        'Frequency': buy_counts
    })
    
    # Dynamic R scoring based on user-adjusted boundaries
    def r_score(days):
        if days <= r_boundary_high:
            return 4  # Very recent
        elif days <= (r_boundary_high + r_boundary_low) / 2:
            return 3  # Recent
        elif days <= r_boundary_low:
            return 2  # Not so recent
        else:
            return 1  # Long time ago
        
    # Dynamic F scoring based on user-adjusted boundaries
    def f_score(count):
        if count >= f_boundary_high:
            return 4  # High frequency
        elif count >= f_boundary_low:
            return 3  # Medium-high frequency
        elif count >= (f_boundary_low + 1) / 2:
            return 2  # Medium-low frequency
        else:
            return 1  # Low frequency
    
    rfm_df['R_score'] = rfm_df['Recency'].apply(r_score)
    rfm_df['F_score'] = rfm_df['Frequency'].apply(f_score)
    
    # Segment users based on R and F scores
    def segment_user(row):
        r_s, f_s = row['R_score'], row['F_score']
        if r_s >= 3 and f_s >= 3:
            return '重要价值客户'
        elif r_s >= 3 and f_s < 3:
            return '潜力客户'
        elif r_s < 3 and f_s >= 3:
            return '高流失风险客户'
        else:
            return '流失客户'
            
    rfm_df['Segment'] = rfm_df.apply(segment_user, axis=1)
    
    return rfm_df
