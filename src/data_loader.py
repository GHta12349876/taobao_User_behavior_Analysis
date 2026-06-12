import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

@st.cache_data
def load_raw_data(file_path: str = None, nrows: int = 100000) -> pd.DataFrame:
    """
    Load raw UserBehavior dataset (cached).
    For demo purposes, reads only the first `nrows` rows to avoid memory issues.
    
    Args:
        file_path: Path to the CSV file (defaults to ../UserBehavior.csv)
        nrows: Number of rows to read (default 100,000 for demo)
    """
    if file_path is None:
        # Default path: go up one level from src/ to project root
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "UserBehavior.csv")
    try:
        # Read only the first `nrows` rows for demo purposes
        df = pd.read_csv(file_path, header=None, 
                         names=['user_id', 'item_id', 'category_id', 'behavior_type', 'ts'],
                         nrows=nrows)
        
        # Convert timestamp to Beijing Time (UTC+8)
        df['datetime'] = pd.to_datetime(df['ts'], unit='s') + pd.Timedelta(hours=8)
        
        # Drop duplicates
        df = df.drop_duplicates().reset_index(drop=True)
        
        # Extract features
        df['weekday'] = df['datetime'].dt.weekday
        df['hour'] = df['datetime'].dt.hour
        
        # Map behavior types to Chinese for display
        behavior_map = {
            'pv': '点击',
            'cart': '加购',
            'fav': '收藏',
            'buy': '购买'
        }
        df['behavior_cn'] = df['behavior_type'].map(behavior_map)
        
        return df
    except FileNotFoundError:
        st.error("未找到 UserBehavior.csv 文件。请确保数据文件位于项目根目录。")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"数据加载失败：{str(e)}")
        return pd.DataFrame()


def filter_and_clean_data(raw_df: pd.DataFrame, start_date: pd.Timestamp = None, 
                          end_date: pd.Timestamp = None, behaviors: list = None) -> pd.DataFrame:
    """
    Filter and clean data based on user selections.
    
    Args:
        raw_df: Raw DataFrame from load_raw_data
        start_date: Start date for filtering
        end_date: End date for filtering
        behaviors: List of behavior types to include
        
    Returns:
        Filtered DataFrame
    """
    df = raw_df.copy()
    
    # Apply date filter
    if start_date is not None and end_date is not None:
        df = df[(df['datetime'] >= start_date) & (df['datetime'] < end_date)]
    
    # Apply behavior filter
    if behaviors is not None and len(behaviors) > 0:
        reverse_behavior_map = {'点击': 'pv', '加购': 'cart', '收藏': 'fav', '购买': 'buy'}
        behavior_types = [reverse_behavior_map[b] for b in behaviors if b in reverse_behavior_map]
        df = df[df['behavior_type'].isin(behavior_types)]
    
    return df
