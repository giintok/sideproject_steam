import streamlit as st
import math
from utils import utils_recommendation_by_tags_select as ur_tags

def app():

    st.subheader("저희가 선택한 테그 30개를 활용한 게임 추천 시스템")

    # 태그 선택 섹션
    st.markdown("선호하는 **태그**를 최대 3개까지 클릭해주세요")

    tags = ['Indie', 'Action', 'Adventure', 'Early Access', 'Simulation',
            'Multiplayer', 'Singleplayer', 'Strategy', 'Sports', 'Open World',
            'Exploration', 'First-Person', 'Third Person', '2D', '3D',
            'Survival', 'PvP', 'Puzzle', 'Story Rich', 'Horror',
            'Crafting', 'Soulslike', 'RPG', 'Realistic', 'Cute']

    # 사용자가 현재 보고 있는 화면의 너비에 따라 열의 개수를 조정합니다.
    columns_per_row = 5

    # 총 태그 수에 맞춰 행의 개수를 계산합니다.
    rows = math.ceil(len(tags) / columns_per_row)

    # 선택된 태그들을 저장할 리스트입니다.
    selected_tags = []

    # 그리드 형태로 체크박스를 배치합니다.
    for row in range(rows):
        cols = st.columns(columns_per_row)  # 동적으로 컬럼을 생성합니다.
        for col in range(columns_per_row):
            tag_index = row * columns_per_row + col
            if tag_index < len(tags):  # 태그 리스트의 범위를 벗어나지 않도록 합니다.
                with cols[col]:
                    # 체크박스를 생성하고 선택된 경우 selected_tags에 추가합니다.
                    if st.checkbox(tags[tag_index], key=tags[tag_index]):
                        selected_tags.append(tags[tag_index])

    # 선택된 태그의 개수가 3개를 초과하는 경우 알림을 표시합니다.
    if len(selected_tags) > 3:
        st.warning("최대 3개의 태그만 선택할 수 있습니다.")
        st.stop()  # 추가적인 처리를 멈춥니다.

    # 가격을 설정하는 슬라이더를 추가합니다.
    min_price, max_price = st.slider("가격 범위를 선택하세요", 0.0, 70.0, (0.0, 70.0), 0.1)

    if st.button('다음 게임 추천'):
        if 'page_number' not in st.session_state:
            st.session_state.page_number = 1
            
        if 'recommendation_index' not in st.session_state:
            st.session_state.recommendation_index = 0

        # 선택된 태그와 가격 범위에 기반한 게임 추천
        recommendations = ur_tags.recommend_games(selected_tags, page_number=st.session_state.page_number, games_per_page=5)
        recommendations = recommendations[(recommendations['Price'] >= min_price) & (recommendations['Price'] <= max_price)]  # 가격 범위 필터링

        if st.session_state.recommendation_index >= len(recommendations):
            st.session_state.recommendation_index = 0
        
        if recommendations.empty:
            st.warning("선택한 태그에 해당하는 게임이 없습니다.")
        else:
            # 페이지 매김을 위한 변수
            page_number = st.session_state.recommendation_index // 5 + 1
            start_idx = (page_number - 1) * 5
            end_idx = min(len(recommendations), page_number * 5)
            page_games = recommendations.iloc[start_idx:end_idx]

            # 선택된 태그에 기반한 게임 출력 
            for _, game in page_games.iterrows():
                st.text('---' * 15)
                # 이미지 가져오기
                image_url = ur_tags.get_steam_game_image(game['AppID'])
                # 이미지 출력
                if image_url:
                    st.image(image_url, caption=f"{game['Name']} 이미지", use_column_width=True)
                else:
                    st.warning(f"{game['Name']}의 이미지를 가져올 수 없습니다.")
                # 게임 정보 출력
                st.text(f"게임 이름: {game['Name']}")
                st.text(f"게임 ID: {game['AppID']}")
                st.text(f"가격: {game['Price']}")
                st.text(f"장르: {game['Genres']}")
                st.text(f"개발사: {game['Developers']}")
                st.text(f"출판사: {game['Publishers']}")
                st.text(f"태그: {game['Tags']}")

        # 페이지 번호 증가
        st.session_state.page_number += 1
