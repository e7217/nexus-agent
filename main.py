from dotenv import load_dotenv
import argparse

from nexus_agent.models.graph import SupervisorState
from nexus_agent.utils import logo
from nexus_agent.utils.logger import setup_logger
from nexus_agent.graph.builder import SupervisorGraphBuilder
from nexus_agent.services.backend import start_server

load_dotenv(override=True)

logger = setup_logger("nexus_agent")


def run_example():
    """예제 쿼리를 실행합니다."""
    logger.info("Starting Nexus Agent example...")
    builder = SupervisorGraphBuilder()
    app = builder.build()
    import datetime as dt

    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    today = dt.datetime.now().strftime("%Y-%m-%d")
    # answer = app.execute(SimpleState(messages=[("user", f"{today} 일자의 삼성전자 관련 경제 뉴스를 알려줘.")]))
    answer = app.execute(
        SupervisorState(
            llm=llm,
            messages=[
                (
                    "user",
                    f"{today} 일자의 삼정전자와 관련된 주요 뉴스는 무엇이 있을까? 방송사 CNN의 뉴스 페이지를 참고해서 알려줘",
                )
            ],
        )
    )
    # answer = app.execute(SupervisorState(messages=[("user", f"3 더하기 2는?")]))

    # answer = app.execute(
    #     SupervisorState(
    #         llm=llm,
    #         messages=[
    #             (
    #                 "user",
    #                 "네이버의 주식 토론 방에서 삼성전자에 대한 긍정적인 의견을 찾아주고, report.txt 파일을 생성하여 참조 링크 목록을 저장해줘",
    #             )
    #         ]
    #     )
    # )
    logger.info(f"Final answer: {answer}")



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(
        description="Nexus Agent - 주식 시장 분석을 위한 AI 에이전트 네트워크"
    )
    parser.add_argument("--server", action="store_true", help="백엔드 서버 모드로 실행")
    parser.add_argument("--example", action="store_true", help="예제 쿼리 실행")

    args = parser.parse_args()
    print(logo.logo)
    if args.server:
        logger.info("Starting Nexus Agent in server mode...")
        start_server()
    elif args.example:
        run_example()
    else:
        # 인자가 없으면 예제 실행
        run_example()
