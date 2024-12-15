from flask import Flask, request, jsonify
from db_control.crud import add_reflection, update_reflection
import openai

app = Flask(__name__)
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/chat', methods=['POST'])
def submit_chat():
    data = request.json
    feeling = data.get('feeling')
    event = data.get('event')
    emotion = data.get('emotion')

    if not (feeling and event and emotion):
        return jsonify({"error": "All questions must be answered"}), 400

    # ChatGPTで価値観を生成
    prompt = f"以下の回答内容から読み取れる価値観を200文字程度で挙げてください。\n\n1. {feeling}\n2. {event}\n3. {emotion}\n"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None
    )
    values = response.choices[0].text.strip()

    # データベースに保存
    add_reflection(feeling, event, emotion, values)
    return jsonify({"message": "Reflection submitted successfully.", "values": values}), 200

@app.route('/values', methods=['POST'])
def submit_values():
    data = request.json
    userid = data.get('userid')
    assess = data.get('assess')
    awareness = data.get('awareness')

    if not userid or assess is None or not awareness:
        return jsonify({"error": "All fields are required"}), 400

    update_reflection(userid, assess, awareness)
    return jsonify({"message": "Feedback submitted successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
