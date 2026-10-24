
from retriever import retrieve_context

question = "What does Windows Event ID 4625 mean?"

context = retrieve_context(question)

print("Question:", question)
print("\nRetrieved security evidence:")
print(context if context else "No relevant evidence found.")
