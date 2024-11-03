import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv', encoding='utf-8-sig')

# Lọc ra các cột có chỉ số (loại bỏ cột không cần thiết như 'name', 'Nation', 'Team', 'Position')
numeric_cols = df.columns.drop(['name', 'Nation', 'Team', 'Position'])

# Chuyển đổi các cột về kiểu số nếu có thể
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

teams = df['Team'].unique()

# Vẽ histogram phân bố của mỗi chỉ số cho toàn giải và từng đội
for attr in numeric_cols:
    plt.figure(figsize=(10, 6))
    
    # Vẽ histogram cho toàn giải
    plt.hist(df[attr].dropna(), bins=15, alpha=0.5, label='All Teams')
    
    # Vẽ histogram cho từng đội
    for team in teams:
        team_data = df[df['Team'] == team]
        plt.hist(team_data[attr].dropna(), bins=15, alpha=0.5, label=team)
    
    plt.title(f'Histogram of {attr}')
    plt.xlabel(attr)
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()
