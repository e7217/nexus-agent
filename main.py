from dotenv import load_dotenv

from nexus_agent.models.graph import SupervisorState
from nexus_agent.utils.logger import setup_logger
from nexus_agent.graph.builder import SupervisorGraphBuilder

load_dotenv(override=True)

logger = setup_logger("nexus_agent")



if __name__ == "__main__":
    logger.info("Starting Nexus Agent...")
    builder = SupervisorGraphBuilder()
    app = builder.build()
    import datetime as dt

    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    today = dt.datetime.now().strftime("%Y-%m-%d")
    # answer = app.execute(SimpleState(messages=[("user", f"{today} 일자의 삼성전자 관련 경제 뉴스를 알려줘.")]))
    answer = app.execute(SupervisorState(llm = llm, messages=[("user", f"{today} 일자의 삼정전자와 관련된 주요 뉴스는 무엇이 있을까? 방송사 CNN의 뉴스 페이지를 참고해서 알려줘")]))
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
