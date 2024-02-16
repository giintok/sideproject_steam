import pandas as pd
import requests

# 스팀 API 키
steam_api_key = "api_key"

# 스팀 API를 통해 게임의 리뷰 긍정 및 부정 투표수를 가져오는 함수
def get_review_counts(app_id):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&filter=recent&language=all&review_type=all&key={steam_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('success', False):
            return data['query_summary'].get('total_positive', 0), data['query_summary'].get('total_negative', 0)
    return 0, 0

# 스팀 API를 통해 게임의 Peak CCU를 가져오는 함수
def get_peak_ccu(app_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}&key={steam_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['response'].get('player_count', 0)
    return 0

# 게임 아이디를 읽어옴
app_ids_df = pd.read_csv('app_ids.csv')  # app_ids.csv 파일에 따라 경로 설정 필요

# 데이터를 나누어서 가지고 옴
chunk_size = 100  # 100개씩 가져옴
for i in range(0, len(app_ids_df), chunk_size):
    chunk = app_ids_df['AppID'].iloc[i:i+chunk_size]

    # 파워셀에서 실행하기 위한 print로 확인
    for app_id in chunk:
        positive, negative = get_review_counts(app_id)
        peak_ccu = get_peak_ccu(app_id)
        print(f"AppID: {app_id}, Positive: {positive}, Negative: {negative}, Peak CCU: {peak_ccu}")

    # 결과를 CSV 파일에 저장
    chunk_df = pd.DataFrame({
        'AppID': chunk,
        'Positive': [get_review_counts(app_id)[0] for app_id in chunk],
        'Negative': [get_review_counts(app_id)[1] for app_id in chunk],
        'Peak CCU': [get_peak_ccu(app_id) for app_id in chunk]
    })
    chunk_df.to_csv(f'app_review_peak_ccu_{i+1}-{i+chunk_size}.csv', index=False)

