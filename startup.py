from dependency_injector import containers, providers
from langchain_openai import ChatOpenAI
from nexus_agent.graph.builder import SupervisorGraphBuilder
from nexus_agent.utils.logger import setup_logger


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    logger = providers.Singleton(setup_logger, "nexus_agent")

    supervisor_graph = providers.Singleton(SupervisorGraphBuilder)

    llm = providers.Singleton(ChatOpenAI, model="gpt-4o-mini", temperature=0)

    # app = providers.Factory(APIBuilder)
    # for node in supervisor_graph.get_nodes():
    #     app.add_route(f"/{node.name.lower().replace('node', '')}", "POST", lambda x: node.invoke(x))
    # app.create_app()
