import os
import sqlite3

class SqliteController():
    def __init__(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, 'chatbot_data.db')
        self.db_path = db_path
        
    def return_word_clouds(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            results = cursor.execute('SELECT * FROM wordcloud')
            words = []
            
            for result in results:
                words.append(result[0])
                
            return words
    
    def insert_word_clouds(self, words):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if isinstance(words, list):
                    for word in words:
                        cursor.execute(f"INSERT INTO wordcloud VALUES('{word}')")
                        conn.commit()
                else:
                    cursor.execute(f"INSERT INTO wordcloud VALUES('{words}')")
                    conn.commit()
        except Exception as e:
            print(f"Erro ao inserir dados no banco de dados: {str(e)}")