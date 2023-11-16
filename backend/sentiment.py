from textblob import TextBlob
import random
from utils.phrases import frases_felizes, frases_tristes, frases_bravas, frases_ambiguas
from utils.translate_words import translate_word

class SentimentAnalisys():
    def __init__(self) -> None:
        pass

    def analisar_sentimento(self, texto):
        """
            Analisa o sentimento e a subjetividade do texto.
        """
        analise = TextBlob(texto)
        return analise.sentiment.polarity, analise.sentiment.subjectivity

    def escolher_frase(self, sentimento, subjetividade):
        """
            Escolhe uma frase com base no sentimento e na subjetividade.
        """
        if sentimento > 0.2:
            if subjetividade > 0.5:
                return random.choice(frases_felizes)
            else:
                return "um planeta de serenidade, com harmonia e paz"
        elif -0.2 < sentimento <= 0.2:
            return random.choice(frases_ambiguas)
        else:
            if subjetividade > 0.5:
                return random.choice(frases_bravas)
            else:
                return random.choice(frases_tristes)

    def gerar_descricao_planeta(self, frase):
        """
            Gera uma descrição imaginativa de um planeta.
        """
        return f"Em sua jornada, você descobre {frase}."
    
    def input_phrase(self, input_text: str):
        input_text = (translate_word(input_text))
        polaridade, subjetividade = self.analisar_sentimento(input_text)

        frase_escolhida = self.escolher_frase(polaridade, subjetividade)
        descricao_planeta = self.gerar_descricao_planeta(frase_escolhida)

        return descricao_planeta, polaridade, subjetividade