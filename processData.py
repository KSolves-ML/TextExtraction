import time
import spacy
from flask import Flask, render_template, request,json

app = Flask(__name__)

model_path_01 = 'results (1)/models'


@app.route('/')
def index():
    return render_template('index.html')


def predict_entities(text, sentiment):
    selected_texts = []
    model = spacy.load(model_path_01 + '/model_pos')
    if model_path_01 is not None:
        print("Loading Models  from ", model_path_01)
        if sentiment == "positive":
            print("Loading positive model")
            model = spacy.load(model_path_01 + '/model_pos')
        if sentiment == "negative":
            print("Loading negative model")
            model = spacy.load(model_path_01 + '/model_neg')
        if sentiment == "neutral":
            print("Loading neutral model ")
            model = spacy.load(model_path_01 + '/model_neu')
    else:
        print("model is not present ? seems like something went wrong")

    doc = model(text)
    ent_array = []
    for ent in doc.ents:
        start = text.find(ent.text)
        end = start + len(ent.text)
        new_int = [start, end, ent.label_]
        if new_int not in ent_array:
            ent_array.append([start, end, ent.label_])

    selected_text = text[ent_array[0][0]: ent_array[0][1]] if len(ent_array) > 0 else text
    print(selected_texts)
    return selected_text


@app.route('/predict', methods=['POST'])
def predict():
    prediction = ""
    if request.method == 'POST':
        raw_text = request.form["comment"]
        sentiment = request.form["sentiment"]
        prediction = predict_entities(raw_text, sentiment)
        response = app.response_class(
            response=json.dumps(prediction),
            status=200,
            mimetype='application/json'
        )
    return response
    #return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=80)
