# NGUYỄN VĂN ANH B22DCCN016

import pandas as pd

# Đọc dữ liệu từ file CSV
df = pd.read_csv('result.csv', encoding='utf-8-sig')

# Lọc ra các cột có chỉ số (loại bỏ cột không cần thiết như 'name', 'Nation', 'Team', 'Position')
numeric_cols = df.columns.drop(['name', 'Nation', 'Team', 'Position'])
# Chuyển đổi các cột về kiểu số nếu có thể
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Tìm top 3 cầu thủ có điểm cao nhất và thấp nhất ở mỗi chỉ số
top_3_highest = {}
top_3_lowest = {}
for attr in numeric_cols:
    top_3_highest[attr] = df.nlargest(3, attr).apply(lambda x: f"{x['name']}: {x[attr]}", axis=1).tolist()
    top_3_lowest[attr] = df.nsmallest(3, attr).apply(lambda x: f"{x['name']}: {x[attr]}", axis=1).tolist()

# Chuyển đổi thành DataFrame để lưu vào file CSV
top_3_highest_df = pd.DataFrame.from_dict(top_3_highest, orient='index').transpose()
top_3_lowest_df = pd.DataFrame.from_dict(top_3_lowest, orient='index').transpose()

# Lưu dữ liệu vào file result2_highest.csv và result2_lowest.csv
top_3_highest_df.to_csv('result2_highest.csv', index=False, encoding='utf-8-sig')
top_3_lowest_df.to_csv('result2_lowest.csv', index=False, encoding='utf-8-sig')

print("Dữ liệu top 3 cầu thủ có điểm cao nhất đã được lưu vào file result2_highest.csv.")
print("Dữ liệu top 3 cầu thủ có điểm thấp nhất đã được lưu vào file result2_lowest.csv.")

# Tính trung vị, trung bình và độ lệch chuẩn cho mỗi chỉ số
stats = []
teams = df['Team'].unique()
for attr in numeric_cols:
    all_median = df[attr].median()
    all_mean = df[attr].mean()
    all_std = df[attr].std()
    
    stats.append({'Team': 'all', 'Attribute': attr, 'Median': all_median, 'Mean': all_mean, 'Std': all_std})
    
    for team in teams:
        team_data = df[df['Team'] == team]
        team_median = team_data[attr].median()
        team_mean = team_data[attr].mean()
        team_std = team_data[attr].std()
        
        stats.append({'Team': team, 'Attribute': attr, 'Median': team_median, 'Mean': team_mean, 'Std': team_std})

# Chuyển đổi thành DataFrame và lưu vào file CSV
stats_df = pd.DataFrame(stats)
stats_df_pivot = stats_df.pivot(index='Team', columns='Attribute')
stats_df_pivot.columns = [f'{stat} of {attr}' for attr, stat in stats_df_pivot.columns]
stats_df_pivot.reset_index(inplace=True)
stats_df_pivot.to_csv('results2.csv', index=False, encoding='utf-8-sig')

print("Dữ liệu đã được lưu vào file results2.csv.")
