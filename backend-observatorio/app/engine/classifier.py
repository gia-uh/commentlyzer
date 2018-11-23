"""Módulo para la extración de opiniones."""
import os
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from math import floor, ceil

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""


Classifier = joblib.load(
    os.path.join(MODULE, 'serialized', 'serialized_opinion_classifier'))
Vectorizer = joblib.load(
    os.path.join(MODULE, 'serialized', 'serialized_opinion_vectorizer'))


def roundx(number):
    """Método que redondea o aproxima un número."""
    #first = int(int((number - floor(number)) >= 0.5) * (floor(number) + 1))
    #second = int(int((number - floor(number)) < 0.5) * (floor(number)))
    #return first + second
    fn = floor(number)
    v = int(number-fn>=0.5)
    return ceil(number)*v + (1-v)*fn


def extract_opinion(text):
    """
    Explicación:
        Método que recibe un str o una lista de str y devuelve sus clasificaciones.
    Argumentos:
        text: Str o lista de str.
    Retorno:
        answer: str o lista de str con las clasificaciones.
    """
    text = text if isinstance(text, list) else [text]
    data = Vectorizer.transform(text)
    prediction = Classifier.predict(data)
    answers = []
    for item in prediction:
        item = roundx(item)
        if item == 1:
            answers.append('Positive')
        elif item == -1:
            answers.append('Negative')
        else:
            answers.append('Neutral')
    answers = answers[0] if len(answers) == 1 else answers
    return answers


if __name__ == '__main__':
    res1,res2=extract_opinion(['el perro es malo', 'la comida esta buena'])
    assert res1=='Negative'
    assert res2 == 'Positive'
