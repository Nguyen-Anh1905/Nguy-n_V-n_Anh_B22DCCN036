# Nguyễn Văn Anh - B22DCCN036

from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import time
import random

# bắt đầu lấy dữ liệu web
link='https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats'
r=requests.get(link)
soup=bs(r.content, 'html.parser')
# tìm bảng chứa các câu lạc bộ
soup=soup.find('table',{'id':'stats_squads_standard_for'})
# lưu các link href câu lạc bộ vòa danh sách
club=soup.find_all('th',{'scope':'row'})

data=[]
data_play={}

# bắt đầu lấy dữ liệu của từng CLB
for item in club:
    # hàm chờ thời gian
    time.sleep(random.uniform(3,4))
    url='https://fbref.com' + item.a.get('href')
    tem=item.a.text.strip()
    print(tem)
    response = requests.get(url)

    # tìm các bảng liên quan
    soup=bs(response.text,'html.parser')
    table=soup.find("table",{"id":"stats_standard_9"})
    Goalkeeping  = soup.find("table", {"id": "stats_keeper_9"})
    Shooting= soup.find("table",{"id":"stats_shooting_9"})
    Passing=soup.find("table",{"id":"stats_passing_9"})
    Pass_Types=soup.find("table",{"id":"stats_passing_types_9"})
    Goal_and_Shot_Creation=soup.find("table",{"id":"stats_gca_9"})
    Defensive_Actions=soup.find("table",{"id":"stats_defense_9"})
    Possession=soup.find("table",{"id":"stats_possession_9"})
    Playing_Time=soup.find("table",{"id":"stats_playing_time_9"})
    Miscellaneous_Stats=soup.find("table",{"id":"stats_misc_9"})
    
    # kiểm tra xem có tìm thấy bẳng table không
    if table is None:
        print ('Không tim thấy bảng') 
    else:
        print ("đang lấy dữ liệu cầu thủ trong bảng:",tem)
    
    the_tbody=table.find("tbody").find_all("tr")

    for tbody in the_tbody:
        # hàm lấy giá trị ô trong bảng
        def get_stat(data_stat,tbody):
            if data_stat=="nationality":
                cell = tbody.find("td", {"data-stat": data_stat})
                return cell.text.strip()[-3:] if cell else "N/a"
            
            elif data_stat=="player":
                cell=tbody.find("th")
                return cell.text.strip() if cell else "N/a"

            else: 
                cell = tbody.find("td", {"data-stat": data_stat})
                return cell.text.strip() if cell and cell.text.strip() != "" else "N/a"
            
        name=get_stat("player",tbody)
        
        data_play={
            "name": get_stat("player", tbody),
            "Nation": get_stat("nationality", tbody),
            "Team": tem,
            "Position": get_stat("position", tbody),
            "Age": get_stat("age", tbody),

            # Playing time
            "Matches": get_stat("games", tbody),
            "Starts": get_stat("games_starts", tbody),
            "minutes_90s": get_stat("minutes_90s", tbody),

            # Performance
            "Non-Penalty Goals": get_stat("goals", tbody),
            "Penalty Goals": get_stat("pens_made", tbody),
            "Assists": get_stat("assists", tbody),
            "Yellow Cards": get_stat("cards_yellow", tbody),
            "Red Cards": get_stat("cards_red", tbody),

            # Expected
            "xG(Ex)": get_stat("xg", tbody),
            "npxG(Ex)": get_stat("npxg", tbody),
            "xAG(Ex)": get_stat("xg_assist", tbody),

            # Progression
            "PrgC": get_stat("progressive_carries", tbody),
            "PrgP": get_stat("progressive_passes", tbody),
            "PrgP Received": get_stat("progressive_passes_received", tbody),

            # Per 90 minutes_90s
            "Gls": get_stat("goals_per90", tbody),
            "Ast": get_stat("assists_per90", tbody),
            "G+A": get_stat("goals_assists_per90", tbody),
            "G-PK": get_stat("goals_pens_per90", tbody),
            "G+A-PK": get_stat("goals_assists_pens_per90", tbody),
            "xG": get_stat("xg_per90", tbody),
            "xAG": get_stat("xg_assist_per90", tbody),
            "xG + xAG": get_stat("xg_xg_assist_per90", tbody),
            "npxG": get_stat("npxg_per90", tbody),
            "npxG + xA": get_stat("npxg_xg_assist_per90", tbody),

            # Goalkeeping
            "GA": get_stat("ga", tbody),
            "GA90": get_stat("ga90", tbody),
            "SoTA": get_stat("sota", tbody),
            "Saves": get_stat("saves", tbody),
            "Save%": get_stat("save_pct", tbody),
            "W": get_stat("wins", tbody),
            "D": get_stat("draws", tbody),
            "L": get_stat("losses", tbody),
            "CS": get_stat("clean_sheets", tbody),
            "CS%": get_stat("clean_sheet_pct", tbody),
            "PKatt": get_stat("gk_pens_att", tbody),
            "PKA": get_stat("gk_pens_allowed", tbody),
            "PKsv": get_stat("gk_pens_saved", tbody),
            "PKm": get_stat("gk_pens_missed", tbody),
            "Save2%": get_stat("gk_pens_save_pct", tbody),
        }
        # chỉ lấy cầu thủ thi đấu trên 90 phút
        if get_stat("minutes_90s", tbody) != "N/a":
            minutes_90s = float(get_stat("minutes_90s", tbody))
            if minutes_90s > 1:
                data.append(data_play)

        # lấy dữ liệu Goalkeeping:
        
        tbody_goalkeeping = Goalkeeping.find("tbody").find_all("tr")
        for row in tbody_goalkeeping:
            if get_stat("player",row)==name:
            # Cập nhật thêm các thống kê Goalkeeping vào từ điển cầu thủ
                data_play.update({
                    # Performance
                    "GA": get_stat("gk_goals_against", row),
                    "GA90": get_stat("gk_goals_against_per90", row),
                    "SoTA": get_stat("gk_shots_on_target_against", row),
                    "Saves": get_stat("gk_saves", row),
                    "Save%": get_stat("gk_save_pct", row),
                    "W": get_stat("gk_wins", row),
                    "D": get_stat("gk_ties", row),
                    "L": get_stat("gk_losses", row),
                    "CS": get_stat("gk_clean_sheets", row),
                    "CS%": get_stat("gk_clean_sheets_pct", row),
                    # Penalty Kicks
                    "PKatt": get_stat("gk_pens_att", row),
                    "PKA": get_stat("gk_pens_allowed", row),
                    "PKsv": get_stat("gk_pens_saved", row),
                    "PKm": get_stat("gk_pens_missed", row),
                    "Save2%": get_stat("gk_pens_save_pct", row)
                })

    tbody_shooting = Shooting.find("tbody").find_all("tr")
    for row in tbody_shooting:
        player_name = get_stat("player", row)  # Lấy tên cầu thủ từ bảng Shooting
        # Tìm cầu thủ trong danh sách dữ liệu hiện tại
        for player_data in data:
            if player_data["name"] == player_name:  # Nếu tên cầu thủ trùng nhau
                # Cập nhật các thông số bổ sung từ bảng Shooting vào từ điển `player_data`
                player_data.update({
                    # Standard
                    "Gls(shoot)": get_stat("goals", row),
                    "Sh": get_stat("shots", row),
                    "SoT": get_stat("shots_on_target", row),
                    "SoT%": get_stat("shots_on_target_pct", row),
                    "Sh/90": get_stat("shots_per90", row),
                    "SoT/90": get_stat("shots_on_target_per90", row),
                    " G/Sh": get_stat("goals_per_shot", row),
                    "G/SoT": get_stat("goals_per_shot_on_target", row),
                    "Dist": get_stat("average_shot_distance", row),
                    "FK": get_stat("shots_free_kicks",row),
                    "PK": get_stat("pens_made", row),
                    "PKatt": get_stat("pens_att",row),
                    # Expected
                    "xG(shoot)": get_stat("xg", row),
                    "npxG(shoot)": get_stat("npxg", row),
                    " npxG/Sh": get_stat("npxg_per_shot", row),
                    " G-xG": get_stat("xg_net",row),
                    "np:G-xG": get_stat("npxg_net", row)
                })
                break 

    tbody_Passing=Passing.find("tbody").find_all("tr")  
    for row in tbody_Passing:
        player_name = get_stat("player", row)
        for player_data in data:
            if player_data["name"]==player_name:
                player_data.update({
                    # Total
                    "Cmp(total)": get_stat("passes_completed",row),
                    "Att(total)": get_stat("passes",row),
                    "Cmp%(total)": get_stat("passes_pct",row),
                    "TotDist": get_stat("passes_total_distance", row),
                    "PrgDist": get_stat("passes_progressive_distance", row),
                    # Short
                    "Cmp(short)": get_stat("passes_completed_short",row),
                    "Att(short)": get_stat("passes_short",row),
                    "Cmp%(short)": get_stat("passes_pct_short",row),
                    # Medium
                    "Cmp(Medium)": get_stat("passes_completed_medium",row),
                    "Att(Medium)": get_stat("passes_medium",row),
                    "Cmp%(Medium)": get_stat("passes_pct_medium",row),
                    # Long
                    "Cmp(Long)": get_stat("passes_completed_long",row),
                    "Att(Long)": get_stat("passes_long",row),
                    "Cmp%(Long)": get_stat("passes_pct_long",row),
                    # Expected
                    "Ast(passing)": get_stat("assists",row),
                    "xAG(passing)": get_stat("xg_assist",row),
                    "xA(passing)": get_stat("pass_xa",row),
                    "A-xAG": get_stat("xg_assist_net",row),
                    "KP": get_stat("assisted_shots",row),
                    "`1/3": get_stat("passes_into_final_third",row),
                    "PPA": get_stat("passes_into_penalty_area",row),
                    "CrsPA": get_stat("crosses_into_penalty_area",row),
                    "PrgP(passing)": get_stat("progressive_passes",row)
                })
    tbody_Pass_Type=Pass_Types.find("tbody").find_all("tr")
    for row in tbody_Pass_Type:
        player_name=get_stat("player",row)   
        for player_data in data:
            if player_data["name"]==player_name:
                player_data.update({
                    # Pass Types
                    "Live": get_stat("passes_live",row),
                    "Dead": get_stat("passes_dead",row),
                    "FK(passtype)": get_stat("passes_free_kicks",row),
                    "TB":  get_stat("through_balls",row),
                    "Sw": get_stat("passes_switches",row),
                    "Crs(passtype)": get_stat("crosses",row),
                    "TI": get_stat("throw_ins",row),
                    "CK": get_stat("corner_kicks",row),
                    # Corner Kicks
                    "In": get_stat("corner_kicks_in",row),
                    "Out": get_stat("corner_kicks_out",row),
                    "Str": get_stat("corner_kicks_straight",row),
                    # Outcomes
                    "Cmp(passtype)": get_stat("passes_completed",row),
                    "Off": get_stat("passes_offsides",row),
                    "Blocks": get_stat("passes_blocked",row)
                })

    tbody_Goal_and_Shot_Creation=Goal_and_Shot_Creation.find("tbody").find_all("tr")
    for row in tbody_Goal_and_Shot_Creation:
        player_name=get_stat("player",row)   
        for player_data in data:
            if player_data["name"]==player_name:
                player_data.update({
                    # SCA
                    "SCA": get_stat("sca",row),
                    "SCA90": get_stat("sca_per90",row),
                    # SCA Types
                    "PassLive(SCA)": get_stat("sca_passes_live",row),
                    "PassDead(SCA)": get_stat("sca_passes_dead",row),
                    "TO(SCA)": get_stat("sca_take_ons",row),
                    "Sh(SCA)": get_stat("sca_shots",row),
                    "Fld(SCA)": get_stat("sca_fouled",row),
                    "Def(SCA)": get_stat("sca_defense",row),
                    # GCA
                    "GCA": get_stat("gca",row),
                    "GCA90": get_stat("gca_per90",row),
                    # GCA Types
                    "PassLive(GCA)": get_stat("gca_passes_live",row),
                    "PassDead(GCA)": get_stat("gca_passes_dead",row),
                    "TO(GCA)": get_stat("gca_take_ons",row),
                    "Sh(GCA)": get_stat("gca_shots",row),
                    "Fld(GCA)": get_stat("gca_fouled",row),
                    "Def(GCA)": get_stat("gca_defense",row)
                })
    tbody_Defensive_Actions=Defensive_Actions.find("tbody").find_all("tr")
    for row in tbody_Defensive_Actions:
        player_name=get_stat("player",row)   
        for player_data in data:
            if player_data["name"]==player_name:
                player_data.update({
                    # Tackles
                    "Tkl(Tackles)": get_stat("tackles",row),
                    "TklW": get_stat("tackles_won",row),
                    "Def 3rd": get_stat("tackles_def_3rd",row),
                    "Mid 3rd": get_stat("tackles_mid_3rd",row),
                    "Att 3rd": get_stat("tackles_att_3rd",row),
                    # Challenges
                    "Tkl(Challenges)": get_stat("challenge_tackles",row),
                    "Att(Challenges)": get_stat("challenges",row),
                    "Tkl%": get_stat("challenge_tackles_pct",row),
                    "Lost": get_stat("challenges_lost",row),
                    # Blocks
                    "`Blocks": get_stat("blocks",row),
                    "Sh(Blocks)": get_stat("blocked_shots",row),
                    "Pass(Blocks)": get_stat("blocked_passes",row),
                    "Int(Blocks)": get_stat("interceptions",row),
                    "Tkl + Int": get_stat("tackles_interceptions",row),
                    "Clr": get_stat("clearances",row),
                    "Err": get_stat("errors",row)
                })

    tbody_Possession=Possession.find("tbody").find_all("tr")
    for row in tbody_Possession:
        player_name=get_stat("player",row)
        for player_data in data:
            if player_name==player_data["name"]:
                player_data.update({
                    # Touches
                    "Touches": get_stat("touches",row),
                    "Def Pen": get_stat("touches_def_pen_area",row),
                    "Def 3rd(Touches)": get_stat("touches_def_3rd",row),
                    "Mid 3rd(Touches)": get_stat("touches_mid_3rd",row),
                    "Att 3rd(Touches)": get_stat("touches_att_3rd",row),
                    "Att Pen(Touches)": get_stat("touches_att_pen_area",row),
                    "Live(Touches)": get_stat("touches_live_ball",row),
                    # Taek-Ons
                    "Att(Taek-Ons)": get_stat("take_ons",row),
                    "Succ": get_stat("take_ons_won",row),
                    "Succ%": get_stat("take_ons_won_pct",row),
                    "Tkld": get_stat("take_ons_tackled",row),
                    "Tkld%": get_stat("take_ons_tackled_pct",row),
                    # Carries
                    "Carries": get_stat("carries",row),
                    "TotDist(Carries)": get_stat("carries_distance",row),
                    "ProDist": get_stat("carries_progressive_distance",row),
                    "ProgC": get_stat("progressive_carries",row),
                    "1/3`": get_stat("carries_into_final_third",row),
                    "CPA": get_stat("carries_into_penalty_area",row),
                    "Mis": get_stat("miscontrols",row),
                    "Dis": get_stat("dispossessed",row),
                    # Receiving
                    "Rec": get_stat("passes_received",row),
                    "PrgR": get_stat("progressive_passes_received",row)
                })
    tbody_PlayingTime=Playing_Time.find("tbody").find_all("tr")
    for row in tbody_PlayingTime:
        player_name=get_stat("player",row)
        for player_data in data:
            if player_name==player_data["name"]:
                player_data.update({
                    # Starts
                    "`Starts": get_stat("games_starts",row),
                    "Mn/Start": get_stat("minutes_per_start",row),
                    "Compl": get_stat("games_complete",row),
                    # Subs
                    "Subs": get_stat("games_subs",row),
                    "Mn/Sub": get_stat("minutes_per_sub",row),
                    "unSub": get_stat("unused_subs",row),
                    # Team Success
                    "PPM": get_stat("points_per_game",row),
                    "onG": get_stat("on_goals_for",row),
                    "onGA": get_stat("on_goals_against",row),
                    # Team Success xG
                    "onxG": get_stat("on_xg_for",row),
                    "onxGA": get_stat("on_xg_against",row)
                })
    
    tbody_MiscellaneousStats=Miscellaneous_Stats.find("tbody").find_all("tr")
    for row in tbody_MiscellaneousStats:
        player_name=get_stat("player",row)
        for player_data in data:
            if player_name==player_data["name"]:
                player_data.update({
                    # Performance
                    "Fls": get_stat("fouls",row),
                    "`Fld": get_stat("fouled",row),
                    "`Off": get_stat("offsides",row),
                    "Crs": get_stat("crosses",row),
                    "OG": get_stat("own_goals",row),
                    "Recov": get_stat("ball_recoveries",row),
                    #  Aerial Duels
                    "Won": get_stat("aerials_won",row),
                    "`Lost": get_stat("aerials_lost",row),
                    "Won%": get_stat("aerials_won_pct",row)
                })

# Lưu DataFrame vào file CSV
df = pd.DataFrame(data)
df = df.sort_values(by=["name", "Age"], ascending=[True, False])
df.to_csv('result.csv', index=False,encoding='utf-8-sig')  # Lưu vào file result.csv, bỏ cột index
print("Dữ liệu đã được lưu vào file result.csv.")
print(df)
# with open('html.txt','w',encoding='utf-8') as file:
#     file.write(soup.prettify())




    
    

