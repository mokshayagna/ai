import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    project="genai-432214",
    location="us-central1",
)

response = llm.invoke("Hello")

print(response.content)
