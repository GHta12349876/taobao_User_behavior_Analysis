# 部署指南

## 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 确保 `UserBehavior.csv` 文件位于项目根目录

3. 启动应用：
```bash
streamlit run app.py
```

4. 在浏览器中打开 http://localhost:8501

## 部署到 Hugging Face Spaces

### 方法一：使用 Git 推送

1. 创建 Hugging Face Spaces 账号并新建 Space（选择 Streamlit 模板）

2. 克隆你的 Space 仓库：
```bash
git clone https://huggingface.co/spaces/<your-username>/<space-name>
cd <space-name>
```

3. 将本项目文件复制到 Space 目录（排除 UserBehavior.csv）

4. 提交并推送：
```bash
git add .
git commit -m "Deploy Taobao User Behavior Analysis"
git push
```

### 方法二：直接在 Hugging Face UI 上传

1. 在 Hugging Face Spaces 创建新 Space（选择 Streamlit 模板）
2. 点击 "Files" 标签
3. 上传以下文件：
   - `app.py`
   - `data_loader.py`
   - `rfm_engine.py`
   - `visuals.py`
   - `ai_insights.py`
   - `requirements.txt`
   - `Procfile`
   - `.streamlit/config.toml`
   - `README.md`

**注意：** 由于数据文件较大，建议使用较小的演示数据集或修改 `data_loader.py` 中的 `nrows` 参数。

## 部署到 Streamlit Cloud

1. 将代码推送到 GitHub 仓库

2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)

3. 连接你的 GitHub 账号并选择仓库

4. 设置主文件为 `app.py`

5. 点击 "Deploy!"

**注意：** Streamlit Cloud 免费版有内存限制，建议减小 `nrows` 参数或使用完整数据集的抽样。

## 性能优化建议

1. **减少数据加载量**：修改 `data_loader.py` 中的 `nrows` 参数
   ```python
   # 默认加载前 100,000 行
   raw_df = load_raw_data(nrows=100000)
   ```

2. **使用缓存**：应用已使用 `@st.cache_data` 装饰器缓存数据加载

3. **启用压缩**：在 `.streamlit/config.toml` 中配置

## 故障排查

### 问题：内存不足
**解决方案：** 减小 `nrows` 参数或使用更小的数据集

### 问题：图表不显示
**解决方案：** 检查 `plotly` 是否正确安装，尝试 `pip install --upgrade plotly`

### 问题：数据加载缓慢
**解决方案：** 首次加载需要时间，后续会使用缓存加速
