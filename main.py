from dotenv import load_dotenv

from dependency_injector.wiring import Provide, inject
import uvicorn

from api.server import APIBuilder
from nexus_agent.graph.nodes.naver_news_searcher import NaverNewsSearcherNode
from nexus_agent.graph.nodes.report_assistant import ReportAssistantNode
from nexus_agent.graph.nodes.yahoo_finance_searcher import YahooFinanceSearcherNode
from nexus_agent.utils.logger import setup_logger
from nexus_agent.graph.builder import SupervisorGraphBuilder
from startup import Container
from rich.console import Console

console = Console()
load_dotenv(override=True)
logger = setup_logger("nexus_agent")
logo = """
[cyan]
==============================================================================================
                                                                                              
  ███    ██ ███████ ██   ██ ██    ██ ███████      █████   ██████  ███████ ███    ██ ████████  
  ████   ██ ██       ██ ██  ██    ██ ██          ██   ██ ██       ██      ████   ██    ██     
  ██ ██  ██ █████     ███   ██    ██ ███████     ███████ ██   ███ █████   ██ ██  ██    ██     
  ██  ██ ██ ██       ██ ██  ██    ██      ██     ██   ██ ██    ██ ██      ██  ██ ██    ██     
  ██   ████ ███████ ██   ██  ██████  ███████     ██   ██  ██████  ███████ ██   ████    ██     
                                                                                              
----------------------------------------------------------------------------------------------
                                                    Since 2025.03.04, Let's study together!
==============================================================================================
"""


@inject
def main(
    graph_builder: SupervisorGraphBuilder = Provide[Container.supervisor_graph],
):
    console.print(logo)
    logger.info("Starting Nexus Agent service...")

    ## 그래프 빌더
    graph_builder.add_node(NaverNewsSearcherNode())
    graph_builder.add_node(ReportAssistantNode())
    graph_builder.add_node(YahooFinanceSearcherNode())
    # graph_builder.add_node(GoogleFinanceSearcherNode())
    graph_builder.build()

    ## API 서버 빌더
    api_builder = APIBuilder()
    app = api_builder.create_app()
    for node in graph_builder.get_nodes():
        app.add_api_route(
            f"/api/{node.__class__.__name__.lower().replace('node', '')}",
            methods=["POST"],
            endpoint=node.invoke,
        )

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=["api.routes"])
    container.wire(modules=[__name__])
    main()
