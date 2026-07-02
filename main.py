import os
import asyncio
import glob
from ragas.llms import llm_factory
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from langchain_chroma import Chroma
from langchain_openai import AzureChatOpenAI
from ragas.embeddings import embedding_factory
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ragas.metrics.collections import AnswerRelevancy, Faithfulness

load_dotenv()
directory = "D:/PCB/dataset"
pattern = "*.pdf"
chunk_size = 500
chunk_overlap = 100
#llm = ChatOpenAI(model = os.getenv("CHAT_MODEL"), api_key= os.getenv("OPENAI_API_KEY"))
llm = AzureChatOpenAI(
    azure_deployment="gpt-4.1", 
    temperature=0
)
embedding = AzureOpenAIEmbeddings(
    azure_deployment="text-embedding-3-large",

)


azure_client = AsyncAzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

ragas_embedding = embedding_factory(
    "openai",
    model="text-embedding-3-large",
    client=azure_client,
    interface="modern",
)

ragas_llm = llm_factory(
    "gpt-4.1",
    client=azure_client
)

answer_relevancy = AnswerRelevancy(
    llm=ragas_llm,
    embeddings=ragas_embedding
)

faithfulness = Faithfulness(
    llm=ragas_llm
)

def populate_vector_db(embedding):

    search_path = os.path.join(directory, pattern)
    file_path = glob.glob(search_path)

    all_docs = []
    for file in file_path:
        loader = PyPDFLoader(
            file_path=file,
            mode="page",
        )

        docs = loader.load()
        all_docs.extend(docs)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = text_splitter.split_documents(all_docs)

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory="./chroma_db"
    )

    return vector_store


def retrieve_context(query: str, k: int = 2):
    
    if os.path.exists("./chroma_db"):
        vector_db = Chroma(embedding_function=embedding, persist_directory="./chroma_db")
    else:
        vector_db = populate_vector_db(embedding)

    docs = vector_db.similarity_search(query, k=k)
    context = "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}" for doc in docs
    )

    return context, docs

def generate_answer(question: str, context: str):

        prompt = f"""You are a helpful assistant that answers questions based ONLY on the provided context.

                INSTRUCTIONS:
                1. Answer the question using ONLY the information from the context below
                2. If the context does not contain enough information to answer the question, explicitly state: "I cannot find sufficient information in the provided context to answer this question."
                3. Do NOT use external knowledge or make assumptions beyond what's in the context
                4. Stay faithful to the context - do not hallucinate or invent information
                5. Provide a concise but complete answer (2-4 sentences)
                6. If you're uncertain about any part, acknowledge it
                    

                Context:
                {context}

                Question: 
                {question}

                Answer:
                """
        
        response = llm.invoke(prompt)
        return response.content

async def evaluate( 
            question: str,
            answer: str,
            context: str
        ):
        faithfulness_result = await faithfulness.ascore(
            user_input = question,
            response = answer,
            retrieved_contexts = [context]
        )

        answer_relevancy_result = await answer_relevancy.ascore(
            user_input = question,
            response = answer
        )

        return {
            "faithfulness": faithfulness_result.value,
            "answer_relevancy": answer_relevancy_result.value,
        }





async def query_rag(question: str):

    context, doc = retrieve_context(question)

    answer = generate_answer(
        question,
        context
    )

    scores = await evaluate(
        question,
        answer,
        context
    )

    return {
        "question": question,
        "answer": answer,
        "context": context,
        "doc": doc,
        **scores
    }
   