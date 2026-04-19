from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate

load_dotenv()

SYSTEM_PROMPT = """Você é um assistente especialista em programação Python.
Responda de forma clara, com exemplos de código quando necessário.
Foque exclusivamente em dúvidas sobre Python."""

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])

llm = ChatOpenAI(model="gpt-4", temperature=0.3)

memory = ConversationBufferMemory(return_messages=True)

chain = ConversationChain(llm=llm, prompt=prompt, memory=memory, verbose=False)


def chat(pergunta: str) -> str:
    return chain.predict(input=pergunta)


if __name__ == "__main__":
    print("Chatbot Python — digite 'sair' para encerrar\n")
    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() in ("sair", "exit", "quit"):
            break
        if not pergunta:
            continue
        resposta = chat(pergunta)
        print(f"\nAssistente: {resposta}\n")
