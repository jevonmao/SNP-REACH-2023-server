from flask import Flask, jsonify, request
import os
import openai


app = Flask(__name__)

@app.route("/parseRaw", methods=['POST'])
def parseRawText():
    rawContent = request.form.get("content")
    systemPrompt = """
    summarize this content into an overall summary, and a bullet list of special need accommodations, and whether it is TRUE available or FALSE unavailable at this school. make the list comprehensive, not just ones at the school. Always output in JSON format
    """
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": systemPrompt},
        {"role": "user", "content": rawContent}
    ]
    )
    response = completion.choices[0].message.content
    return response


openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    app.run()