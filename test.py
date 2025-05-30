from langchain_ollama import OllamaLLM  
model = OllamaLLM(model="llama3.2", temperature=0.5)  # Add this line
response = model.invoke("Come up with 10 names for a song about parrots")
