게임 데이터를 전처리 후 분석 및 시각화 과정을 정리해서 스티림릿에 구현

utils_N, Page_N은 분석을 위해서 여러가지 형태로 막 만들어본 파일들

2024-02-19일

전처리 과정

실질적 사용 칼럼 
#App ID​                   게임 고유 ID​​
#Name​                     게임 명​
#Price​                    가격​
#Developers​               개발사​
#Publishers​               공급사​
#Required age​             권장 연령​
#About the game​           게임 설명​
#Supported language​       지원 언어​
#DLC count​                DLC 개수​
#Positive​                 유저 긍정적 평가 수​
#Negative​                 유저 부정적 평가 수​
#Metacritic score​         메타크리틱 점수​
#Peak CCU​                 최대 동시 접속자 수​
#Genres​                   개발사가 등록한 장르​
#Tags​                     유저가 등록한 태그​
#Average playtime Forever​ 누적 플레이타임 평균값 ​
#Median playtime forever​  누적 플레이타임 중앙값  

총 85102개의 데이터​

1. 2024-01-18일자 스팀 '최고 인기 제품' 4016개의AppID를 기준 비교​

2. 양 데이터 간 겹치는 행 2260개 기준으로 전처리 : 최종 데이터 2243개​

 1) 분석 및 시각화 하기 위한 컬럼을 선택​

  - 주관적 및 객관적으로 게임 선택 시 고려할 사항을 기준으로 18개의 컬럼 선택​
AppID, Name, Peak CCU, Estimated owners, Required age, Price, DLC count, About the game, Supported languages, Metacritic Score, Positive, Negative, Average playtime forever, Median playtime forever, Developers, Publishers, Genres, Tags​​

  2) 각 데이터의 이상치 및 결측치 확인​

​Peak CCU : 24시간 평균치, 최근 최대 접속인원이 아닌 측정 당시의 접속 인원수로 0인 값이 많았음​
Estimated Owners : 게임 소유자가 범위로 표시되어있는 형태로 편차가 너무 심한 칼럼임을 확인​
Required age : N세 이하로만 나와 있어 새로운 라벨링을 하기로 함​
개발사, 공급사,  장르, 태그 컬럼에서 총 null값 180개 발견​
긍정, 부정 수가 무료게임인 경우 0인 데이터가 총 189개 발견​

  3) 이상 데이터 및 결측치 해결​
Peak CCU : 스팀 API 및 크롤잉을 불러올 수 없는 데이터 수동으로 해결​
Null값 새롭게 크롤링을 하여 AppID를 기준으로 그룹화​
DLC, SoundTrack으로 게임이 아닌 열은 삭제​

3. 게임 Rank 열 추가​

4. Tags 컬럼 비슷한 의미의 태그 통합​

"Local Co-Op", "Multiplayer"
"Online Co-Op", "Multiplayer"
"Massively Multiplayer", "Multiplayer"
"Co-op", "Multiplayer"
"Co-Op", "Multiplayer"
"Shooter", "FPS"
"Sandbox", "Openworld"
"Openworld", "Open World"
"Building", "Crafting"
"Craftin", "Crafting"
"Basketball", "Sports"
"Football (Soccer)", "Sports"
"Racing", "Sports"
"Basketball", "Sports"
"Cartoony", "Cartoon"
"Comic Book", "Cartoon"
"Comedy", "Funny"
"Roguelike", "Rogue-like"
"Roguelite", "Rogue-lite"
"Trading Card Game", "Card Game"
"Card Battler", "Card Game"

5. 스팀에서 사라진 APPID 및 리메이크 판의 가격 수정​

7670, 8850, 50130, 271590, 1577120, 916440 리메이크 게임 0의 가격표시 오류 수정​
261570 사라진 게임데이터 동명의 게임 387290으로 수정​

6. 개발사 및 공급사 데이터 수정​

, Inc., Ltd. : 쉼표로 구분되어 데이터 분리시 따로 카운트되는 현상이 발생하여 회사 부분 삭제​
​​
데이터 분석

EDA결과 부족한 데이터가 많아 추가적으로 크롤링을 다시하는 케이스가 많았음
Peak CCU : stream api로는 현재 접속자만 가지고 올 수 있고 StreamDB에는 24시간중 최대 접속자가 있으나 크롤링이 막혀있는 상태 2천개정도니 수동도 고민 중
Positive : 2024-02-16일자로 다시 크롤링
Negative : 2024-02-16일자로 다시 크롤링
Tags​​ : 비어있는 태그가 많아서 새롭게 크롤링

추천 시스템

상위 태그 30개를 이용해서 사용자가 태그를 최대 3개를 선택하고 보여주는 방식의 추천시스템
