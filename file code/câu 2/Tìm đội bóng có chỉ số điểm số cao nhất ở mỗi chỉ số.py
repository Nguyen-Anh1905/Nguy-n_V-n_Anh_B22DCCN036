import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv', encoding='utf-8-sig')

# Lọc ra các cột có chỉ số (loại bỏ cột không cần thiết như 'name', 'Nation', 'Team', 'Position')
numeric_cols = df.columns.drop(['name', 'Nation', 'Team', 'Position'])

# Chuyển đổi các cột về kiểu số nếu có thể
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Tìm đội bóng có chỉ số điểm số cao nhất ở mỗi chỉ số
best_teams = {}
for attr in numeric_cols:
    best_team = df.groupby('Team')[attr].mean().idxmax()
    best_teams[attr] = best_team

print("Best teams by attribute:")
print(best_teams)
