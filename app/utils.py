from app.business_logic.llm_chain import ContextQNAChain

async def answer_generator(content: str, query: str) -> str:
    if len(content) == 0 or len(query) == 0:
        raise ValueError("Content or the Query can not be empty. Please Check it.")
    else:
        chain = ContextQNAChain().create()
        answer: str = chain.invoke({
            "context":content,
            "query": query
        })
        return answer.__dict__