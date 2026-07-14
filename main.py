import streamlit as st
import requests

# 페이지 기본 설정
st.set_page_config(
    page_title="MBTI별 포켓몬 추천",
    page_icon="🔮",
    layout="centered"
)

# MBTI 및 포켓몬 데이터 매칭 (공식 포켓몬 이미지 URL 연동)
# 이미지 출처: 포켓몬 공식 도감 고화질 에셋 번호 활용
POKEMON_DATA = {
    "INFP": {
        "name": "이브이",
        "desc": "풍부한 감성과 무한한 가능성을 지닌 INFP는 다양한 모습으로 진화할 수 있는 이브이와 똑 닮았습니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/133.png",
        "type": "노말"
    },
    "INFJ": {
        "name": "뮤",
        "desc": "신비롭고 통찰력 넘치는 INFJ는 전설 속에서 세상을 관조하며 깊은 지혜를 품고 있는 뮤와 어울립니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/151.png",
        "type": "에스퍼"
    },
    "INTP": {
        "name": "후딘",
        "desc": "끊임없이 분석하고 호기심이 왕성한 INTP는 뇌가 계속 자라나 천재적인 두뇌를 지닌 후딘과 완벽히 매칭됩니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/065.png",
        "type": "에스퍼"
    },
    "INTJ": {
        "name": "뮤츠",
        "desc": "독립적이고 철저한 전략가인 INTJ는 압도적인 지능과 냉철한 분석력을 가진 뮤츠의 분위기를 풍깁니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/150.png",
        "type": "에스퍼"
    },
    "ISFP": {
        "name": "메타몽",
        "desc": "예술가적 기질이 있고 평화를 사랑하는 ISFP는 주변 환경에 유연하게 맞춰 변신하는 메타몽과 닮았습니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/132.png",
        "type": "노말"
    },
    "ISFJ": {
        "name": "해피너스",
        "desc": "주변 사람들을 헌신적으로 보살피는 ISFJ는 언제나 타인을 치유하고 행복을 나눠주는 해피너스와 어울립니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/242.png",
        "type": "노말"
    },
    "ISTP": {
        "name": "개굴닌자",
        "desc": "과묵하지만 상황 적응력이 뛰어나고 손재주가 좋은 ISTP는 날렵하고 임기응변에 강한 개굴닌자가 딱입니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/658.png",
        "type": "물/악"
    },
    "ISTJ": {
        "name": "철화구야",
        "desc": "청렴결백하고 원칙주의자인 ISTJ는 묵묵히 자신의 자리를 지키며 단단한 책임감을 보여주는 철화구야와 닮았습니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/797.png",
        "type": "강철/비행"
    },
    "ENFP": {
        "name": "피카츄",
        "desc": "에너지가 넘치고 사람들을 즐겁게 만드는 ENFP는 포켓몬스터의 영원한 마스코트이자 활력소인 피카츄 그 자체입니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png",
        "type": "전기"
    },
    "ENFJ": {
        "name": "토게키스",
        "desc": "타인의 성장을 돕고 따뜻하게 이끄는 ENFJ는 분쟁이 없는 평화로운 곳에 나타나 은혜를 베푸는 토게키스와 닮았습니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/468.png",
        "type": "페어리/비행"
    },
    "ENTP": {
        "name": "팬텀",
        "desc": "재치 있는 변론가이자 장난기 가득한 ENTP는 상대방을 흔들어놓는 유쾌한 트릭스터 팬텀과 환상의 케미를 자랑합니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/094.png",
        "type": "고스트/독"
    },
    "ENTJ": {
        "name": "리자몽",
        "desc": "강력한 리더십과 야망을 지닌 ENTJ는 거침없는 카리스마로 무리를 이끌고 전장을 지배하는 리자몽과 어울립니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png",
        "type": "불꽃/비행"
    },
    "ESFP": {
        "name": "푸린",
        "desc": "어디서나 주목받는 것을 좋아하고 스타성이 있는 ESFP는 마이크를 잡고 노래 부르며 시선을 사로잡는 푸린과 비슷합니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/039.png",
        "type": "노말/페어리"
    },
    "ESFJ": {
        "name": "망나뇽",
        "desc": "친절하고 사교적인 ESFJ는 바다에서 난처한 사람을 보면 그냥 지나치지 못하고 도와주는 친근한 망나뇽과 어울립니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/149.png",
        "type": "드래곤/비행"
    },
    "ESTP": {
        "name": "루카리오",
        "desc": "행동파에 스릴을 즐기고 실전 감각이 뛰어난 ESTP는 파동을 감지하며 역동적으로 전투를 이끄는 루카리오와 닮았습니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/448.png",
        "type": "격투/강철"
    },
    "ESTJ": {
        "name": "괴력몬",
        "desc": "엄격한 관리자이자 조직을 효율적으로 이끄는 ESTJ는 철저한 자기관리와 강력한 실행력을 보여주는 괴력몬과 어울립니다.",
        "img_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/068.png",
        "type": "격투"
    }
}

# 앱 UI 구현
st.title("🔮 나의 MBTI와 어울리는 포켓몬은?")
st.write("당신의 MBTI 성향을 선택하면, 당신과 가장 닮은 포켓몬을 추천해 드립니다.")
st.markdown("---")

# MBTI 선택 박스 (알파벳 정렬)
mbti_list = sorted(list(POKEMON_DATA.keys()))
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요:", mbti_list)

if selected_mbti:
    pokemon = POKEMON_DATA[selected_mbti]
    
    # 레이아웃 분할 (왼쪽: 이미지, 오른쪽: 설명)
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        # 안전한 이미지 로딩을 위해 st.image 사용
        st.image(pokemon["img_url"], use_container_width=True)
        
    with col2:
        st.subheader(f"✨ {selected_mbti}의 포켓몬: **{pokemon['name']}**")
        st.caption(f"**타입:** {pokemon['type']}")
        st.write("")
        st.info(pokemon["desc"])

st.markdown("---")
st.caption("💡 해당 포켓몬 이미지는 공식 포켓몬 도감의 라이브 에셋 주소를 사용하고 있습니다.")
