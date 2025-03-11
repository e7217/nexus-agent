from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import datetime as dt
from langchain_openai import ChatOpenAI

from nexus_agent.models.graph import SupervisorState
from nexus_agent.graph.builder import SupervisorGraphBuilder
from nexus_agent.utils.logger import setup_logger

# 로거 설정
logger = setup_logger("nexus_agent.backend")

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="Nexus Agent API",
    description="주식 시장 분석을 위한 AI 에이전트 네트워크 API",
    version="0.1.0",
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 환경에서는 특정 도메인으로 제한해야 합니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 그래프 빌더 인스턴스 생성
builder = SupervisorGraphBuilder()
graph = builder.build()


# 요청 모델 정의
class QueryRequest(BaseModel):
    query: str
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.2


# 응답 모델 정의
class QueryResponse(BaseModel):
    answer: str
    timestamp: str


@app.get("/")
async def root():
    """API 상태 확인 엔드포인트"""
    return {"status": "online", "message": "Nexus Agent API is running"}


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    사용자 쿼리를 처리하고 에이전트 네트워크의 응답을 반환합니다.
    """
    try:
        logger.info(f"Received query: {request.query}")

        # LLM 인스턴스 생성
        llm = ChatOpenAI(model=request.model, temperature=request.temperature)

        # 그래프 실행
        state = SupervisorState(llm=llm, messages=[("user", request.query)])
        answer = graph.execute(state)

        logger.info(f"Generated answer for query: {request.query}")

        # 응답 생성
        response = QueryResponse(
            answer=answer["messages"][-1].content,
            timestamp=dt.datetime.now().isoformat(),
        )

        return response

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.get("/api/health")
async def health_check():
    """시스템 상태 확인 엔드포인트"""
    return {
        "status": "healthy",
        "timestamp": dt.datetime.now().isoformat(),
        "version": app.version,
    }


# 미들웨어: 요청 로깅
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """모든 HTTP 요청을 로깅하는 미들웨어"""
    start_time = dt.datetime.now()
    response = await call_next(request)
    process_time = (dt.datetime.now() - start_time).total_seconds() * 1000

    logger.info(
        f"Request: {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Process Time: {process_time:.2f}ms"
    )

    return response


def start_server():
    """서버 시작 함수"""
    import uvicorn

    uvicorn.run(
        "nexus_agent.services.backend:app", host="0.0.0.0", port=8000, reload=True
    )


if __name__ == "__main__":
    start_server()
