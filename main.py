import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
from datetime import datetime
import os

# CSV 파일 경로
CSV_FILE = "chat_history.csv"

def load_chat_history():
    """CSV 파일에서 채팅 기록을 불러옵니다."""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["timestamp", "username", "message"])

def save_message(username, message):
    """메시지를 CSV 파일에 저장합니다."""
    df = load_chat_history()
    new_row = pd.DataFrame([{"timestamp": datetime.now(), "username": username, "message": message}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def display_message(username, message, is_own_message):
    """메시지를 화면에 표시합니다. 본인의 메시지는 오른쪽, 다른 사람의 메시지는 왼쪽에 정렬합니다."""
    if is_own_message:
        # 본인의 메시지
        st.markdown(f"<div style='text-align: right; color: gray;'><b>{username}</b>: {message}</div>", unsafe_allow_html=True)
    else:
        # 다른 사람의 메시지
        st.markdown(f"<div style='text-align: left; color: gray;'><b>{username}</b>: {message}</div>", unsafe_allow_html=True)

def main():
    st.title("소민준혁 채팅방")

    # 자동 새로고침을 위한 st_autorefresh
    # 매 1000밀리초(1초)마다 페이지 새로고침
    st_autorefresh(interval=1000, key="chat_autorefresh")

    # 사용자 이름이 세션 상태에 없으면 입력을 요청
    if 'username' not in st.session_state:
        username = st.text_input("사용자 이름을 입력하세요")
        if st.button("시작하기"):
            st.session_state.username = username
            st.experimental_rerun()  # 사용자 이름을 저장한 후 화면을 새로고침
    else:
        # 대화 내용을 불러와서 화면에 표시
        chat_history = load_chat_history()
        for _, row in chat_history.iterrows():
            display_message(row['username'], row['message'], row['username'] == st.session_state.username)

        # 사용자 메시지 입력
        if 'message' not in st.session_state:
            st.session_state.message = ''  # 메시지 세션 상태 초기화
        message = st.text_input("메시지를 입력하세요", key="message", value=st.session_state.message)

        # "보내기" 버튼이 클릭되면 메시지 저장
        if st.button("보내기"):
            save_message(st.session_state.username, message)
            st.session_state.message = ''  # 메시지 보낸 후 입력 필드 비우기

if __name__ == "__main__":
    main()
