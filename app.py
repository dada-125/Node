import os
from flask import Flask, request, jsonify
import google.generativeai as genai
import pandas as pd

app = Flask(__name__)
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

CSV_PATH = 'data.csv'
try:
    df = pd.read_csv(CSV_PATH, encoding='cp949')
    csv_context = df.to_string(index=False)
except:
    csv_context = '데이터 파일 로드 실패'

system_instruction = f'당신은 [FORENSIC_CASE_ANALYSIS_FRAMEWORK v1.0]에 따라 판례와 데이터를 분석하는 법률 포렌식 전문가입니다.\n[참조 데이터] CSV DATA: {csv_context}'

model = genai.GenerativeModel(model_name='gemini-2.0-flash', system_instruction=system_instruction)

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<body style='background:#000; color:#fff; font-family:sans-serif; padding:20px;'>
    <h2>VERITAS NODE</h2>
    <div id='chat' style='height:300px; overflow-y:auto; border:1px solid #333; padding:10px;'></div>
    <input id='msg' style='width:80%; background:#222; color:#fff; border:1px solid #555; padding:10px;'>
    <button onclick='send()' style='padding:10px;'>SEND</button>
    <script>
        async function send() {
            const msg = document.getElementById('msg');
            const chat = document.getElementById('chat');
            chat.innerHTML += '<div><b>USER:</b> ' + msg.value + '</div>';
            const res = await fetch('/ask', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({query: msg.value})
            });
            const data = await res.json();
            chat.innerHTML += '<div style="color:#58a6ff;"><b>BOT:</b> ' + data.response + '</div>';
            msg.value = '';
        }
    </script>
</body>
</html>'''

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    try:
        response = model.generate_content(user_query)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
