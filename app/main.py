from llm import ask_llm


def main():
    question = input("You: ")

    answer = ask_llm(question)

    print("\nQwen:")
    print(answer)


if __name__ == "__main__":
    main()