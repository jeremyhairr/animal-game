
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
conversation_history = [
    {
        "role": "system",
        "content": """
You are running a fun animal guessing game for kids.

Rules:
- The player asks yes/no questions.
- Answer briefly.
- Do NOT reveal the animal unless guessed.
- If the user asks for a hint, give a helpful clue.
- Keep answers fun and simple.
"""
    }
]

question_count = 0


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/game", methods=["POST"])
def game():

    global question_count

    data = request.get_json()
    user_question = data["question"]

    question_count += 1

    conversation_history.append(
        {"role": "user", "content": user_question}
    )

    # keep only last 15 messages
    if len(conversation_history) > 15:
        conversation_history.pop(1)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    answer = response.choices[0].message.content

    conversation_history.append(
        {"role": "assistant", "content": answer}
    )

    return jsonify({
        "answer": answer,
        "count": question_count
    })


@app.route("/hint")
def hint():

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history + [
            {
                "role": "user",
                "content": "Give me a helpful hint about the animal but do not reveal it."
            }
        ]
    )

    hint = response.choices[0].message.content

    return jsonify({"hint": hint})


if __name__ == "__main__":
    app.run(debug=True)