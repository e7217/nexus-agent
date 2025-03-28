# 🚀 넥서스 에이전트: 주식 시장의 AI 전문가 연합

> *"혼자서는 주식 시장을 이길 수 없다면, AI 에이전트 군단을 소집하세요!"*

## 🌟 프로젝트 소개

넥서스 에이전트는 주식 시장을 분석하기 위한 AI 에이전트들의 협력 네트워크입니다. 마치 각 분야의 전문가들이 한 회의실에 모여 토론하듯, 우리의 에이전트들은 각자의 전문 영역에서 데이터를 수집하고 분석하여 최적의 투자 인사이트를 도출합니다.

이 프로젝트의 핵심은 **에이전트 간의 협력**입니다. 한 명의 천재보다 여러 전문가의 협업이 더 나은 결과를 만들어내듯, 우리의 에이전트들은 서로의 분석 결과를 공유하고 검증하며 더 정확한 시장 예측을 만들어냅니다.

### 💫 핵심 가치

1. **정확성**: 모든 분석과 예측은 데이터에 기반하며 지속적으로 검증됩니다.
2. **투명성**: 모든 의사결정 과정과 분석 방법론을 명확하게 문서화합니다.
3. **적응성**: 시장 환경 변화에 적응하고 학습합니다.
4. **협력**: 개별 에이전트의 전문성보다 에이전트 간 협력에서 더 큰 가치를 창출합니다.
5. **실용성**: 이론적으로 완벽한 분석보다 실제 투자에 도움이 되는 인사이트를 우선시합니다.

## 🤖 에이전트 소개

넥서스 에이전트 팀은 다음과 같은 특별한 멤버들로 구성되어 있습니다:

### 🕵️ 데이터 수집 에이전트

*"세상의 모든 주식 데이터는 내가 찾아낸다!"*  
뉴스, 주가, 재무제표, 소셜 미디어까지 - 투자에 필요한 모든 데이터를 끊임없이 수집합니다.

### 📊 시장 분석 에이전트

*"숫자 뒤에 숨겨진 패턴을 읽어내는 마법사"*  
거시경제 지표부터 개별 기업 분석까지, 시장의 큰 그림과 세부 사항을 동시에 분석합니다.

** 관련 링크 **
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader) : 주가 정보, 아마 일봉까지만 되었던 것으로 기억 (분봉 단위는 증권사 API 이용)
- [OpenDartReader](https://github.com/FinanceData/OpenDartReader) : 기업 정보, 재무제표 등
- [그외 라이브러리](https://wikidocs.net/230305) : 금융 관련 라이브러리 리스트

### 🔮 패턴 분석 에이전트

*"역사는 반복된다, 그리고 나는 그 패턴을 찾아낸다"*  
과거 데이터에서 주기적 패턴과 변동성을 탐지하여 미래 움직임을 예측합니다.

### 📝 보고서 생성 에이전트

*"복잡한 데이터를 명쾌한 스토리로 바꾸는 작가"*  
다른 에이전트들의 분석 결과를 종합하여 읽기 쉽고 actionable한 보고서를 작성합니다.

### ⚖️ 신뢰도 평가 에이전트

*"냉정한 평가자, 우리의 실수로부터 배운다"*  
과거 예측과 실제 결과를 비교하여 시스템의 신뢰도를 지속적으로 개선합니다.

## 🔄 에이전트 협력 시스템

넥서스 에이전트의 진정한 마법은 이들이 함께 일하는 방식에 있습니다:

1. **데이터 수집 에이전트**가 최신 정보를 수집하면
2. **시장 분석 에이전트**와 **패턴 분석 에이전트**가 병렬로 데이터를 분석합니다
3. 분석 결과는 **보고서 생성 에이전트**에게 전달되어 종합 보고서로 변환됩니다
4. **신뢰도 평가 에이전트**가 결과를 검증하고 피드백을 제공합니다
5. 모든 에이전트가 이 피드백을 바탕으로 지속적으로 학습하고 발전합니다

이 모든 과정은 LangGraph를 기반으로 한 모듈형 네트워크에서 이루어지며, Kafka 이벤트 스트림을 통해 에이전트 간 원활한 커뮤니케이션이 가능합니다.

## 🎯 프로젝트 목표

넥서스 에이전트는 다음과 같은 구체적인 목표를 가지고 있습니다:

### 📐 아키텍처
...

### 📊 성능 목표

| 목표 항목 | 최소 목표 수준 | 현재 수준 | 달성 여부 |
|---------|------------|---------|-----------|
| 예측 정확도 | 60% 이상 | - |  |
| 수익률 | 시장 평균 +5% | - |  |
| 리스크 관리 | 최대 손실 -15% | - |  |
| 데이터 처리 속도 | 장 시작 전 1회 업데이트 | - |  |
| 분석 종목 수 | 10개 | - |  |

### ✅ 개발 로드맵

- [x] 기본 에이전트 아키텍처 설계
- [ ] 데이터 수집 에이전트 구현
- [ ] 시장 분석 에이전트 구현
- [ ] 패턴 분석 에이전트 구현
- [ ] 보고서 생성 에이전트 구현
- [ ] 신뢰도 평가 에이전트 구현
- [ ] 에이전트 간 협력 시스템 구축
- [ ] 실시간 데이터 처리 파이프라인 구축
- [ ] 사용자 인터페이스 개발
- [ ] 백테스팅 시스템 구현
- [ ] 알림 시스템 구현


## 🛠️ 기술 스택

- **에이전트 오케스트레이션**: LangGraph
- **API 서버**: FastAPI
- **이벤트 처리**: Kafka + Redis Streams
- **데이터베이스**: PostgreSQL, MongoDB, Pinecone
- **AI 모델**: OpenAI API
- **배포**: Docker + Kubernetes

## 🚀 시작하기

**using uv(recommended)**
```bash
git clone https://github.com/e7217/nexus-agent

cd nexus-agent

uv sync

uv run main.py
```

**using pip** 
```bash
# 저장소 클론
git clone https://github.com/e7217/nexus-agent

# 디렉토리 이동
cd nexus-agent

# 의존성 설치 (pip 사용)
pip install -r requirements.txt

# 시스템 실행
python main.py
```

## 🛠️ 활용 가능한 도구들
https://wikidocs.net/book/14021

## 🔮 미래 계획

- 더 많은 전문 에이전트 추가 (예: 섹터별 전문가, 기술적 분석 전문가)
- 에이전트 간 토론 기능 강화
- 실시간 알림 시스템 구축
- 사용자 맞춤형 투자 전략 제안

## 🤝 기여하기

새로운 에이전트를 개발하거나 기존 에이전트를 개선하는 데 관심이 있으신가요? 언제든지 PR을 보내주세요! 우리의 에이전트 네트워크는 항상 새로운 멤버를 환영합니다.

## 📜 라이센스

MIT

---

> "주식 시장은 복잡하지만, 우리의 에이전트들은 그 복잡성을 즐깁니다. 함께라면, 우리는 더 스마트하게 투자할 수 있습니다."
