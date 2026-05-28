

# ========================================
# 사상고등학교 양심 우산 대여 관리 시스템 (Streamlit 웹앱 버전)
# ========================================
# 개선사항: 
# 1. 날짜 계산 단순화 (사용자가 경과 일수 직접 입력)
# 2. 우산 데이터 구조화 (딕셔너리 리스트로 관리)
# 3. Streamlit 웹앱으로 UI 구현
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
# Streamlit은 페이지가 새로고침될 때마다 변수가 초기화되므로, 
# st.session_state를 사용해 데이터를 유지해야 합니다.
if "umbrellas" not in st.session_state:
    # 우산 데이터: 딕셔너리 리스트로 구조화
    # 각 우산은 다음 정보를 포함합니다.
    # - 우산번호(번호)
    # - 상태(대여가능/대여중/수리중)
    # - 컨디션(정상/수리필요)
    # - 대여자 정보(학번, 이름, 대여시간)
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
    # 대여/반납 이력을 기록하는 리스트
    st.session_state.rental_history = []


# ========== 함수 1: 대여 가능한 우산 조회 ==========
def get_available_umbrellas():
    """
    대여 가능한 우산을 필터링해서 반환하는 함수
    
    조건:
    - 상태가 '대여가능'이어야 함
    - 컨디션이 '정상'이어야 함
    
    반환값: 대여 가능한 우산의 번호 리스트
    """
    # for 반복문으로 모든 우산을 순회
    available = []
    for umbrella in st.session_state.umbrellas:
        # if-else 조건문: 상태와 컨디션 확인
        if umbrella["상태"] == "대여가능" and umbrella["컨디션"] == "정상":
            available.append(umbrella["번호"])
    
    return available


# ========== 함수 2: 특정 우산 정보 가져오기 ==========
def get_umbrella_by_number(umbrella_num):
    """
    우산 번호로 해당 우산의 정보를 찾아서 반환하는 함수
    
    매개변수: umbrella_num (우산 번호)
    반환값: 해당 우산의 딕셔너리 데이터
    """
    # for 반복문으로 모든 우산을 순회
    for umbrella in st.session_state.umbrellas:
        # if 조건문: 우산 번호가 일치하는지 확인
        if umbrella["번호"] == umbrella_num:
            return umbrella
    
    return None


# ========== 함수 3: 우산 상태 업데이트 ==========
def update_umbrella(umbrella_num, state, condition):
    """
    특정 우산의 상태와 컨디션을 변경하는 함수
    
    매개변수:
    - umbrella_num: 우산 번호
    - state: 변경할 상태 (대여가능/대여중/수리중)
    - condition: 변경할 컨디션 (정상/수리필요)
    """
    # for 반복문으로 모든 우산을 순회
    for umbrella in st.session_state.umbrellas:
        # if 조건문: 우산 번호가 일치하면 상태 업데이트
        if umbrella["번호"] == umbrella_num:
            umbrella["상태"] = state
            umbrella["컨디션"] = condition
            return True
    
    return False


# ========== 함수 4: 연체 벌점 계산 ==========
def calculate_penalty(overdue_days):
    """
    경과 일수를 받아서 연체 벌점을 계산하는 함수
    
    규칙: 7일을 초과한 일수만큼 벌점 부여
    예) 10일 경과 → (10 - 7) = 3점
    
    매개변수: overdue_days (경과 일수)
    반환값: 벌점 (0 이상의 정수)
    """
    # if 조건문: 7일을 초과했는지 확인
    if overdue_days > 7:
        penalty = overdue_days - 7
    else:
        penalty = 0
    
    return penalty


# ========== UI: 메인 페이지 ==========
st.title("🌂 사상고등학교 양심 우산 대여 관리 시스템")
st.divider()

# 탭 3개 생성: 대여, 반납, 현황조회
tab1, tab2, tab3 = st.tabs(["📋 대여 가능 우산 조회", "🔄 우산 반납", "📊 현황 조회"])


# ========== 탭 1: 대여 가능한 우산 조회 ==========
with tab1:
    st.header("📋 대여 가능한 우산")
    
    # 대여 가능한 우산 리스트 가져오기
    available = get_available_umbrellas()
    
    # if-else 조건문: 대여 가능한 우산이 있는지 확인
    if available:
        st.success(f"✅ 대여 가능: {available}")
        st.info(f"📊 총 {len(available)}개 우산 대여 가능")
        
        # 사용자가 우산을 선택해서 대여하는 섹션
        st.subheader("🌂 우산 대여하기")
        
        # 3개의 입력 필드 배치
        col1, col2 = st.columns(2)
        
        with col1:
            student_id = st.text_input("📝 학번을 입력하세요:")
        with col2:
            student_name = st.text_input("📝 이름을 입력하세요:")
        
        # 대여할 우산 번호 선택
        selected_umbrella = st.selectbox(
            "🔢 대여할 우산 번호를 선택하세요:",
            available
        )
        
        # 약관 동의 체크박스
        st.warning("⚠️  중요한 안내사항")
        st.markdown("""
        📌 **7일 뒤 반납 미이행 시 하루당 벌점 1점이 추가됩니다.**
        📌 **우산 반납 시 상태를 확인합니다 (정상/수리필요).**
        📌 **수리가 필요한 우산은 수리 중 상태로 변경됩니다.**
        """)
        
        agree = st.checkbox("위 조건에 동의합니다.")
        
        # 대여 버튼
        if st.button("✅ 우산 대여하기", use_container_width=True):
            # if 조건문: 입력값 검증
            if not student_id or not student_name:
                st.error("❌ 학번과 이름을 모두 입력하세요.")
            elif not agree:
                st.error("❌ 약관에 동의해야 합니다.")
            else:
                # 우산 정보 업데이트
                umbrella = get_umbrella_by_number(selected_umbrella)
                
                # if 조건문: 우산 정보 업데이트 성공 여부 확인
                if umbrella:
                    umbrella["상태"] = "대여중"
                    umbrella["대여자_학번"] = student_id
                    umbrella["대여자_이름"] = student_name
                    umbrella["대여시간"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 대여 이력 기록
                    st.session_state.rental_history.append({
                        "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "이벤트": "대여",
                        "우산번호": selected_umbrella,
                        "학번": student_id,
                        "이름": student_name
                    })
                    
                    st.success(f"✅ 우산 {selected_umbrella}번 대여가 완료되었습니다!")
                    st.info(f"📅 반납 예정일: 7일 후")
    
    else:
        st.error("❌ 대여 가능한 우산이 없습니다.")


# ========== 탭 2: 우산 반납 ==========
with tab2:
    st.header("🔄 우산 반납")
    
    # 현재 대여 중인 우산 찾기
    renting = []
    for umbrella in st.session_state.umbrellas:
        # if 조건문: 상태가 "대여중"인 우산 필터링
        if umbrella["상태"] == "대여중":
            renting.append(umbrella)
    
    # if-else 조건문: 대여 중인 우산이 있는지 확인
    if renting:
        st.info(f"📋 현재 대여 중인 우산: {[u['번호'] for u in renting]}")
        
        # 반납할 우산 번호 선택
        renting_numbers = [u["번호"] for u in renting]
        selected_return_umbrella = st.selectbox(
            "🔢 반납할 우산 번호를 선택하세요:",
            renting_numbers
        )
        
        # 선택된 우산의 대여 정보 표시
        selected_umbrella = get_umbrella_by_number(selected_return_umbrella)
        
        st.write("---")
        st.subheader("📋 대여 정보")
        
        # 두 개의 컬럼으로 정보 표시
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**학번:** {selected_umbrella['대여자_학번']}")
            st.write(f"**이름:** {selected_umbrella['대여자_이름']}")
        
        with col2:
            st.write(f"**대여시간:** {selected_umbrella['대여시간']}")
        
        # 경과 일수 입력
        st.write("---")
        st.subheader("⏰ 대여 기간 입력")
        st.caption("💡 팁: 대여한 뒤 며칠이 지났는지 입력하세요. (예: 5일이 지났으면 5 입력)")
        
        overdue_days = st.number_input(
            "📅 경과 일수를 입력하세요 (정수):",
            min_value=0,
            max_value=365,
            value=0,
            step=1
        )
        
        # 벌점 계산
        penalty = calculate_penalty(overdue_days)
        
        # 연체 여부 표시
        st.write("---")
        st.subheader("🚨 연체 상황")
        
        # if-else 조건문: 연체 여부 확인
        if penalty > 0:
            st.error(f"⚠️  연체 알림: **{penalty}점의 벌점이 추가됩니다!**")
        else:
            st.success("✅ 정상 반납입니다. 벌점이 없습니다.")
        
        # 우산 상태 선택
        st.write("---")
        st.subheader("🌂 우산 상태 진단")
        
        umbrella_condition = st.radio(
            "우산의 상태를 선택하세요:",
            ["정상", "수리필요"]
        )
        
        # 반납 버튼
        if st.button("✅ 우산 반납하기", use_container_width=True):
            # 우산 상태 업데이트
            if umbrella_condition == "정상":
                # if 조건문: 우산이 정상이면 대여가능 상태로 변경
                update_umbrella(selected_return_umbrella, "대여가능", "정상")
                st.success(f"✅ {selected_return_umbrella}번 우산이 반납되었습니다.")
            
            else:
                # else 조건: 우산이 수리필요이면 수리중 상태로 변경
                update_umbrella(selected_return_umbrella, "수리중", "수리필요")
                st.warning(f"🔧 {selected_return_umbrella}번 우산이 수리 중 상태로 변경되었습니다.")
            
            # 반납 이력 기록
            st.session_state.rental_history.append({
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "이벤트": "반납",
                "우산번호": selected_return_umbrella,
                "학번": selected_umbrella['대여자_학번'],
                "이름": selected_umbrella['대여자_이름'],
                "상태": umbrella_condition,
                "벌점": penalty
            })
    
    else:
        st.error("❌ 반납할 우산이 없습니다.")


# ========== 탭 3: 현황 조회 ==========
with tab3:
    st.header("📊 현황 조회")
    
    # 섹션 1: 대여 중인 우산
    st.subheader("🌂 현재 대여 중인 우산")
    
    renting_umbrellas = []
    for umbrella in st.session_state.umbrellas:
        # if 조건문: 상태가 "대여중"인 우산 필터링
        if umbrella["상태"] == "대여중":
            renting_umbrellas.append(umbrella)
    
    # if-else 조건문: 대여 중인 우산이 있는지 확인
    if renting_umbrellas:
        # for 반복문으로 모든 대여 중인 우산 표시
        for umbrella in renting_umbrellas:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**우산번호:** {umbrella['번호']}번")
            with col2:
                st.write(f"**학번:** {umbrella['대여자_학번']}")
            with col3:
                st.write(f"**이름:** {umbrella['대여자_이름']}")
    else:
        st.info("현재 대여 중인 우산이 없습니다.")
    
    st.divider()
    
    # 섹션 2: 수리 중인 우산
    st.subheader("🔧 수리 중인 우산")
    
    broken_umbrellas = []
    for umbrella in st.session_state.umbrellas:
        # if 조건문: 상태가 "수리중"인 우산 필터링
        if umbrella["상태"] == "수리중":
            broken_umbrellas.append(umbrella["번호"])
    
    # if-else 조건문: 수리 중인 우산이 있는지 확인
    if broken_umbrellas:
        st.error(f"수리 중: {broken_umbrellas}")
    else:
        st.success("수리 중인 우산이 없습니다.")
    
    st.divider()
    
    # 섹션 3: 대여 가능한 우산
    st.subheader("✅ 대여 가능한 우산")
    
    available_umbrellas = get_available_umbrellas()
    
    # if-else 조건문: 대여 가능한 우산이 있는지 확인
    if available_umbrellas:
        st.success(f"대여가능: {available_umbrellas}")
        st.info(f"📊 총 {len(available_umbrellas)}개")
    else:
        st.warning("대여 가능한 우산이 없습니다.")
    
    st.divider()
    
    # 섹션 4: 전체 우산 상태 요약
    st.subheader("📋 전체 우산 상태 요약")
    
    # 테이블 형식으로 모든 우산 상태 표시
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
    
    # 섹션 5: 대여/반납 이력
    st.subheader("📜 대여/반납 이력")
    
    # if-else 조건문: 이력이 있는지 확인
    if st.session_state.rental_history:
        # 최근 이력부터 표시하기 위해 리스트 역순 정렬
        for history in reversed(st.session_state.rental_history):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.write(f"**시간:** {history['시간']}")
            with col2:
                st.write(f"**이벤트:** {history['이벤트']}")
            with col3:
                st.write(f"**우산:** {history['우산번호']}번")
            with col4:
                st.write(f"**학번:** {history['학번']}")
    else:
        st.info("아직 대여/반납 이력이 없습니다.")


# ========== 페이지 하단 정보 ==========
st.divider()
st.caption("🌂 사상고등학교 양심 우산 대여 관리 시스템 | 마지막 업데이트: 2026년 5월 18일")

