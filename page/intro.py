import streamlit as st
from streamlit_chat import message
from utils import project1_desc as p1d
import hashlib
import hmac
import base64
import time
import requests
import json
import re
from utils.Word2Vec import client, module
class ChatbotMessageSender:

    # chatbot api gateway url
    # chatbot api gateway url
    ep_path = 'https://vlwcrxrqz5.apigw.ntruss.com/maia_chatbot_api/beta/'
    # chatbot custom secret key
    secret_key = 'd3Bjb01OY3poYmp6YmpVcW14YmVZQ2VaY1NZVWpyb1U='

    def req_message_send(self, i_text='안녕'):

        timestamp = self.get_timestamp()
        request_body = {
            'version': 'v2',
            'userId': 'instructor3',
            'timestamp': timestamp,
            'bubbles': [
                {
                    'type': 'text',
                    'data': {
                        'description': i_text
                    }
                }
            ],
            'event': 'send'
        }

        ## Request body
        encode_request_body = json.dumps(request_body).encode('UTF-8')

        ## make signature
        signature = self.make_signature(self.secret_key, encode_request_body)

        ## headers
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        print("## Timestamp : ", timestamp)
        print("## Signature : ", signature)
        print("## headers ", custom_headers)
        print("## Request Body : ", encode_request_body)

        ## POST Request
        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response

    @staticmethod
    def get_timestamp():
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def make_signature(secret_key, request_body):

        secret_key_bytes = bytes(secret_key, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())

        return signing_key


if __name__ == '__main__':
    input_text = '안녕'
    res_obj = ChatbotMessageSender()
    res = res_obj.req_message_send(input_text)

    print(res.status_code)
    if(res.status_code == 200):
        #print(res.text)
        dict_res = res.json()
        print(dict_res['bubbles'][0]['data']['description'])
        #print(res.read().decode("UTF-8"))

def desc():
    '''
    st.text_input('input : ', key='input_texts')
    if st.session_state.input_texts:
        res_obj = ChatbotMessageSender()
        res = res_obj.req_message_send(st.session_state.input_texts)

        if(res.status_code == 200):
            #print(res.text)
            dict_res = res.json()
            message(dict_res['bubbles'][0]['data']['description'])
    '''
    if 'past' not in st.session_state: # 내 입력채팅값 저장할 리스트
        st.session_state['past'] = [] 

    if 'generated' not in st.session_state: # 챗봇채팅값 저장할 리스트
        st.session_state['generated'] = []
    

    placeholder = st.empty() # 채팅 입력창을 아래위치로 내려주기위해 빈 부분을 하나 만듬
    
    with st.form('form', clear_on_submit=True): # 채팅 입력창 생성
        user_input = st.text_input('User: ', '') # 입력부분
        submitted = st.form_submit_button('Send') # 전송 버튼
 
    
    if submitted and user_input:
        user_input1 = user_input.strip() # 채팅 입력값 및 여백제거
        if not re.match(r'^태그', user_input1):  # ^태그로 시작하지 않는 경우
            res = ChatbotMessageSender().req_message_send(user_input1)
            chatbot_output1 = res.json()['bubbles'][0]['data']['description']
            st.session_state.past.append(user_input1) # 입력값을 past 에 append -> 채팅 로그값 저장을 위해
            st.session_state.generated.append(chatbot_output1)
            
        elif re.match(r'^태그', user_input1):
            korean_to_target_list, target_to_korean_dict = module.show_tag('ko')
            # "태그" 다음의 문자열을 쉼표로 분할하여 리스트로 만듭니다.
            tag_removed = user_input1.split('태그 ')[1].split(',')
            s_boxes = [tag.strip() for tag in tag_removed]
            #s_boxes = re.findall(r'(?!태그)\b\w+\b', user_input1)
            print(s_boxes)
            # res = ChatbotMessageSender().req_message_send('선택태그')
            # chatbot_output1 = res.json()['bubbles'][0]['data']['description']
            # st.session_state.past.append(user_input1)
            # st.session_state.generated.append(s_boxes) 
            
        # else:
            st.session_state.past.append(user_input1)
            
            user_data = [tag for tag in s_boxes if not 'X' in tag]
            place_df = client.app0(user_data)
            near_hotel_df, near_food_df = client.app1(place_df.iloc[0])
            
            rec_string = '선택한 태그에 가장 적합한 목적지입니다.\n['+place_df.name[0] + '](' + place_df.link[0]+')\n\n다음은 목적지 주변 호텔입니다.\n['+near_hotel_df.name[0] + '](' +near_hotel_df.link[0]+') , ['+near_hotel_df.name[1] + '](' +near_hotel_df.link[1]+') , ['+near_hotel_df.name[2] + '](' +near_hotel_df.link[2]+')\n\n다음은 목적지 주변 맛집입니다.\n['+near_food_df.name[0] + '](' +near_food_df.link[0]+') , ['+near_food_df.name[1] + '](' +near_food_df.link[1]+') , ['+near_food_df.name[2] + '](' +near_food_df.link[2]+')\n'
            #rec_string = 'This is the best destination for the tag you selected\n['+place_df.name[0] + '](' + place_df.link[0]+')\n\nthe followings are hotels close to the '+place_df.name[0] + '\n['+near_hotel_df.name[0] + '](' +near_hotel_df.link[0]+') , ['+near_hotel_df.name[1] + '](' +near_hotel_df.link[1]+') , ['+near_hotel_df.name[2] + '](' +near_hotel_df.link[2]+')\n\nthe followings are some of the best places to eat near the '+place_df.name[0] + '\n['+near_food_df.name[0] + '](' +near_food_df.link[0]+') , ['+near_food_df.name[1] + '](' +near_food_df.link[1]+') , ['+near_food_df.name[2] + '](' +near_food_df.link[2]+')\n'

            res = ChatbotMessageSender().req_message_send('태그 '+ place_df.name[0])
            chatbot_output1 = res.json()['bubbles'][0]['data']['description']
            st.session_state.generated.append(rec_string +'\n'+ chatbot_output1)

    
    with placeholder.container(): # 리스트에 append된 채팅입력과 로봇출력을 리스트에서 꺼내서 메세지로 출력
        for i in range(len(st.session_state['past'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

            if len(st.session_state['generated']) > i:
                message(st.session_state['generated'][i], key=str(i) + '_bot')
                
  


def app():
    desc()
