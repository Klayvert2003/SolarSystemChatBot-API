from flask import Flask, jsonify, request

from bot import Bot

app = Flask(__name__)
bot = Bot()

@app.get('/api/chat-bot')
def chat_bot():
    data = request.get_json()
    if data.get('question'):
        question = data.get('question')
        response = bot.chatbot_response(question)
        if not 'não consegui entender' in response:
            return jsonify({'response': response}), 200
        else:
            return jsonify({'response': response}), 404
    else:
        return jsonify({'error': 'question not found'}), 404

@app.get('/api/verify-danger')
def verify_danger():
    data = request.get_json()
    question = data.get('question')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if question and start_date and end_date:
        if 'verificar perigo entre' in str(question).lower():
            if len(start_date) != 10 or len(end_date) != 10:
                return jsonify({'error': 'invalid date format, correct: YYYY-MM-DD'})
            else:
                response = bot.get_asteroid_info(start_date, end_date)
                list_responses = []
                for item in response:
                    response_dict = {
                        'satelite_name': item.get('name'),
                        'warning_message': 'Este satélite é potencialmente perigoso para a Terra' if item.get('is_potentially_hazardous') else 'Este satélite é não perigoso para a Terra'
                    }
                    list_responses.append(response_dict)
                return jsonify({'response': list_responses}), 200
        else:
            return jsonify({'response': response}), 404
    else:
        return jsonify({'error': 'question not found'}), 404

if __name__ == "__main__":
    app.run('0.0.0.0', 9000, debug=True)