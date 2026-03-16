from openai import OpenAI

# paste your API key between the quotes
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def main():

    print("\n🐘 Welcome to the Animal Guessing Game!")
    print("I am thinking of an animal.")
    print("Ask up to 20 yes/no questions.")
    print("You can also guess the animal anytime.\n")

    messages = [
        {
            "role": "system",
            "content": (
                "You are running a 20 questions game about animals. "
                "Choose ONE random animal and remember it for the entire game. "
                "Only answer questions with 'yes', 'no', or 'maybe'. "
                "If the player guesses the animal correctly say 'Correct!' "
                "but do NOT reveal the animal early."
            )
        },
        {
            "role": "user",
            "content": "Start the game and secretly choose an animal."
        }
    ]

    questions_left = 20

    while questions_left > 0:

        print(f"\nQuestions remaining: {questions_left}")

        question = input("Ask a question or guess the animal: ")

        messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        answer = response.choices[0].message.content.strip()

        print("\nAI:", answer)

        messages.append({"role": "assistant", "content": answer})

        if "correct" in answer.lower():
            print("\n🎉 You guessed correctly!")
            return

        questions_left -= 1

    print("\nGame over! You've used all 20 questions.")

    reveal = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages + [
            {"role": "user", "content": "Reveal the animal you chose."}
        ]
    )

    print("\nThe animal was:")
    print(reveal.choices[0].message.content)


if __name__ == "__main__":
    main()