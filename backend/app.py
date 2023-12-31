import spacy
import matplotlib.pyplot as plt

from io import BytesIO
from wordcloud import WordCloud
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

from bot import Bot
from sentiment import SentimentAnalisys
from database.db_controller import SqliteController

app = Flask(__name__)
CORS(app)
bot = Bot()
db = SqliteController()
sa = SentimentAnalisys()
nlp = spacy.load("pt_core_news_md")

@app.post('/api/chat-bot')
def chat_bot():
    data = request.get_json()
    if data.get('question'):
        question = data.get('question')
        response = bot.chatbot_response(question)
        if not 'não consegui entender' in response:
            db.insert_word_clouds(response.split())
            return jsonify({'response': response}), 200
        else:
            return jsonify({'response': response}), 404
    else:
        return jsonify({'error': 'question not found'}), 404

@app.post('/api/verify-danger')
def verify_danger():
    data = request.get_json()
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if start_date and end_date:
        if len(start_date) != 10 or len(end_date) != 10:
            return jsonify({'error': 'invalid date format, correct: YYYY-MM-DD'})
        else:
            response = bot.get_asteroid_info(start_date, end_date)
            list_responses = []
            for item in response:
                response_dict = {
                    'satelite_name': item.get('name'),
                    'warning_message': 'Este satélite é potencialmente perigoso para a Terra' if item.get('is_potentially_hazardous') else 'Este satélite não é perigoso para a Terra'
                }
                list_responses.append(response_dict)
            list_responses = [list_responses[0], list_responses[1], list_responses[2]]
            return jsonify({'response': list_responses}), 200
    else:
        return jsonify({'error': 'No data found'}), 404
    
@app.get('/api/generate-word-cloud')
def generate_word_cloud():
    responses = db.return_word_clouds()
    text = "\n".join(responses)
    doc = nlp(text)
    filtered_words = [token.text for token in doc if not token.is_stop]
    
    filtered_text = ' '.join(filtered_words)

    try:
        wordcloud = WordCloud(width=800, height=600, background_color='white').generate(filtered_text)
        
        img_buffer = BytesIO()
        plt.figure(figsize=(8, 4))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0)
        img_buffer.seek(0)

        return send_file(img_buffer, mimetype='image/png'), 201

    except ValueError:
        return jsonify({'error': 'words not found'}), 404

@app.post('/api/sentiment_analisys')
def sentiment_analisys():
    data = request.get_json()
    phrase = data.get('phrase')

    if not phrase:
        return jsonify({'error': 'User phrase not found'}), 404
    
    analisys_message, polaridade, subjetividade = sa.input_phrase(phrase)

    return jsonify({
            'analisys_message': analisys_message,
            'polarity_level': polaridade,
            'subjectivy': subjetividade
        })

if __name__ == "__main__":
    app.run('0.0.0.0', 9000)