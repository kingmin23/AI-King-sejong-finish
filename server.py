from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from replace_old_jamo_dataset2 import load_mapping, replace_text
from compose_hcj_to_hangul_dataset2 import compose_text
from openai import OpenAI
import os

openai_api_key = os.getenv("OPEN_API_KEY")
client = OpenAI(api_key=openai_api_key)

def gpt_translate(text):
    response = client.chat.completions.create(
        model="ft:gpt-4.1-nano-2025-04-14:cps:oldhangeul-translator5:CWx0xRHA",
        messages=[
            {"role": "system", "content": "너는 중세국어를 현대국어로 번역하는 AI야."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

app = Flask(__name__)
CORS(app)

mapping = load_mapping("map/combined_old_mapped.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "")
    replaced = replace_text(text, mapping)
    composed = compose_text(replaced)
    translated_text = gpt_translate(composed)
    return jsonify({"result": translated_text})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
