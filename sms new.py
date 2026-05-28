# ========================================
# 사상고등학교 양심 우산 대여 관리 시스템 (Streamlit 웹앱 수정 버전)
# ========================================

import streamlit as st
from datetime import datetime

# ========== 페이지 설정 ==========
st.set_page_config(
    page_title="🌂 사상고 양심 우산 대여 시스템",
    page_icon="🌂",
    layout="wide"
)

# ========== 세션 상태 초기화 ==========
if "umbrellas" not in st.session_state:
    st.session_state.umbrellas = [
        {
            "번호": i,
            "상태": "대여가능",
            "컨디션": "정상",
            "대여자_학번": None,
            "대여자_이름": None,
            "대여시간": None
        }
        for i in range(1, 11)  # 1번부터 10번까지 우산 생성
    ]

if "rental_history" not in st.session_state:
    st.session_state.rental_history = []


# ========== 함수 1: 대여 가능한 우산 조회 ==========
def get_available_umbrellas():
    available = []
    for umbrella in st.session_state.umbrellas:
        if umbrella["상태"] == "대여가능" and umbrella["컨디션"] == "정상":
            available.append(umbrella["번호"])
    return available


# ========== 함수 2: 특정 우산 정보 가져오기 ==========
def get_umbrella_by_number(umbrella_num):
    for umbrella in st.session_state.umbrellas:
        if umbrella["번호"] == umbrella_num:
            return umbrella
    return None


# ========== 함수 3: 우산 상태 업데이트 ==========
def update_umbrella(umbrella_num, state, condition):
    for umbrella in st.session_state.umbrellas:
        if umbrella["번호"] == umbrella_num:
            umbrella["상태"] = state
            umbrella["컨디션"] = condition
            return True
    return False


# ========== 함수 4: 연체 벌점 계산 ==========
def calculate_penalty(overdue_days):
    if overdue_days > 7:
        penalty = overdue_days - 7
    else:
        penalty = 0
    return penalty


# ========== UI: 메인 페이지 ==========
st.title("🌂 사상고등학교 양심 우산 대여 관리 시스템")
st.divider()

# 탭 3개 생성
tab1, tab2, tab3 = st.tabs(["📋 대여 가능 우산 조회", "🔄 우산 반납", "📊 현황 조회"])


# ========== 탭 1: 대여 가능한 우산 조회 ==========
with tab1:
    st.header("📋 대여 가능한 우산")
    available = get_available_umbrellas()
    
    if available:
        st.success(f"✅ 대여 가능: {available}")
        st.info(f"📊 총 {len(available)}개 우산 대여 가능")
        
        st.subheader("🌂 우산 대여하기")
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("📝 학번을 입력하세요:", key="rent_sid")
        with col2:
            student_name = st.text_input("📝 이름을 입력하세요:", key="rent_sname")
        
        selected_umbrella = st.selectbox("🔢 대여할 우산 번호를 선택하세요:", available)
        
        st.warning("⚠️ 중요한 안내사항")
        st.markdown("""
        📌 **7일 뒤 반납 미이행 시 하루당 벌점 1점이 추가됩니다.**
        📌 **우산 반납 시 상태를 확인합니다 (정상/수리필요).**
        📌 **수리가 필요한 우산은 수리 중 상태로 변경됩니다.**
        """)
        
        agree = st.checkbox("위 조건에 동의합니다.")
        
        if st.button("✅ 우산 대여하기", use_container_width=True):
            if not student_id or not student_name:
                st.error("❌ 학번과 이름을 모두 입력하세요.")
            elif not agree:
                st.error("❌ 약관에 동의해야 합니다.")
            else:
                umbrella = get_umbrella_by_number(selected_umbrella)
                if umbrella:
                    umbrella["상태"] = "대여중"
                    umbrella["대여자_학번"] = student_id
                    umbrella["대여자_이름"] = student_name
                    umbrella["대여시간"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    st.session_state.rental_history.append({
                        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "이벤트": "대여",
                        "우산번호": selected_umbrella,
                        "학번": student_id,
                        "이름": student_name
                    })
                    
                    st.success(f"✅ 우산 {selected_umbrella}번 대여가 완료되었습니다!")
                    st.balloons() # 축하 풍선 효과 🎉
                    st.rerun() # 즉시 화면 새로고침하여 대여 가능 목록에서 제외
    else:
        st.error("❌ 대여 가능한 우산이 없습니다.")


# ========== 탭 2: 우산 반납 ==========
with tab2:
    st.header("🔄 우산 반납")
    
    renting = [u for u in st.session_state.umbrellas if u["상태"] == "대여중"]
    
    if renting:
        renting_numbers = [u["번호"] for u in renting]
        st.info(f"📋 현재 대여 중인 우산: {renting_numbers}")
        
        selected_return_umbrella = st.selectbox("🔢 반납할 우산 번호를 선택하세요:", renting_numbers)
        selected_umbrella = get_umbrella_by_number(selected_return_umbrella)
        
        st.write("---")
        st.subheader("📋 대여 정보")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**학번:** {selected_umbrella['대여자_학번']}")
            st.write(f"**이름:** {selected_umbrella['대여자_이름']}")
        with col2:
            st.write(f"**대여시간:** {selected_umbrella['대여시간']}")
        
        st.write("---")
        st.subheader("⏰ 대여 기간 입력")
        overdue_days = st.number_input("📅 경과 일수를 입력하세요 (정수):", min_value=0, max_value=365, value=0, step=1)
        
        penalty = calculate_penalty(overdue_days)
        
        st.write("---")
        st.subheader("🚨 연체 상황")
        if penalty > 0:
            st.error(f"⚠️ 연체 알림: **{penalty}점의 벌점이 추가됩니다!**")
        else:
            st.success("✅ 정상 반납입니다. 벌점이 없습니다.")
        
        st.write("---")
        st.subheader("🌂 우산 상태 진단")
        umbrella_condition = st.radio("우산의 상태를 선택하세요:", ["정상", "수리필요"])
        
        if st.button("✅ 우산 반납하기", use_container_width=True):
            # 이력 기록을 위해 기존 대여자 정보 임시 저장
            saved_sid = selected_umbrella['대여자_학번']
            saved_sname = selected_umbrella['대여자_이름']
            
            # 대여자 정보 초기화 및 상태 업데이트
            selected_umbrella["대여자_학번"] = None
            selected_umbrella["대여자_이름"] = None
            selected_umbrella["대여시간"] = None
            
            if umbrella_condition == "정상":
                update_umbrella(selected_return_umbrella, "대여가능", "정상")
            else:
                update_umbrella(selected_return_umbrella, "수리중", "수리필요")
            
            st.session_state.rental_history.append({
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "이벤트": "반납",
                "우산번호": selected_return_umbrella,
                "학번": saved_sid,
                "이름": saved_sname,
                "상태": umbrella_condition,
                "벌점": penalty
            })
            
            st.success(f"✅ {selected_return_umbrella}번 우산 반납이 완료되었습니다.")
            st.rerun() # 즉시 화면 새로고침하여 대여중 목록에서 제외
    else:
        st.error("❌ 반납할 우산이 없습니다.")


# ========== 탭 3: 현황 조회 ==========
with tab3:
    st.header("📊 현황 조회")
    
    st.subheader("🌂 현재 대여 중인 우산")
    renting_umbrellas = [u for u in st.session_state.umbrellas if u["상태"] == "대여중"]
    
    if renting_umbrellas:
        for umbrella in renting_umbrellas:
            col1, col2, col3 = st.columns(3)
            with col1: st.write(f"**우산번호:** {umbrella['번호']}번")
            with col2: st.write(f"**학번:** {umbrella['대여자_학번']}")
            with col3: st.write(f"**이름:** {umbrella['대여자_이름']}")
    else:
        st.info("현재 대여 중인 우산이 없습니다.")
    
    st.divider()
    
    st.subheader("🔧 수리 중인 우산")
    broken_umbrellas = [u["번호"] for u in st.session_state.umbrellas if u["상태"] == "수리중"]
    if broken_umbrellas:
        st.error(f"수리 중: {broken_umbrellas}")
    else:
        st.success("수리 중인 우산이 없습니다.")
    
    st.divider()
    
    st.subheader("📋 전체 우산 상태 요약")
    umbrella_data = []
    for umbrella in st.session_state.umbrellas:
        umbrella_data.append({
            "우산번호": umbrella["번호"],
            "상태": umbrella["상태"],
            "컨디션": umbrella["컨디션"],
            "대여자": umbrella["대여자_이름"] if umbrella["대여자_이름"] else "-"
        })
    st.dataframe(umbrella_data, use_container_width=True)
    
    st.divider()
    
    st.subheader("📜 대여/반납 이력")
    if st.session_state.rental_history:
        for history in reversed(st.session_state.rental_history):
            col1, col2, col3, col4 = st.columns(4)
            with col1: st.write(f"**시간:** {history['시간']}")
            with col2: st.write(f"**이벤트:** {history['이벤트']}")
            with col3: st.write(f"**우산:** {history['우산번호']}번")
            with col4: st.write(f"**학번:** {history['학번']}")
    else:
        st.info("아직 대여/반납 이력이 없습니다.")

st.divider()
st.caption("🌂 사상고등학교 양심 우산 대여 관리 시스템 | 마지막 업데이트: 2026년 5월 18일")