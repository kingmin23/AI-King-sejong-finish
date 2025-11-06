from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os

#.env 파일 로드 (경로 명시)
load_dotenv(dotenv_path="C:/Users/Gram/Documents/AiKing/AI-King-sejong-main/.env")

#환경변수 테스트 출력
print("환경 변수 확인:", os.environ.get("OPENAI_API_KEY"))

#OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


#Flask 앱 설정
app = Flask(__name__)
CORS(app)

#중세국어 변환 함수 임포트
from replace_old_jamo_dataset2 import load_mapping, replace_text
from compose_hcj_to_hangul_dataset2 import compose_text

#CSV 맵핑 파일 불러오기
mapping = load_mapping("map/combined_old_mapped.csv")

#GPT 번역 함수
def gpt_translate(text):
    response = client.chat.completions.create(
        model="ft:gpt-4.1-nano-2025-04-14:cps:oldhangeul-translator5:CWx0xRHA",
        messages=[
            {"role": "system", "content": "너는 중세국어를 현대국어로 번역하는 AI야."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

#라우트
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

print("🔑 API Key 확인:", os.environ.get("OPENAI_API_KEY"))