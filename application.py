from flask import Flask, request, render_template
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_data():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender = request.form.get('gender'),
            race_enthnicity = request.form.get('race_enthnicity'),
            parental_level_of_education = request.form.get('parental_level_of_education'), 
            lunch = request.form.get('lunch'),
            test_preparation_course = request.form.get('test_preparation_course'),
            reading_score = request.form.get('reading_score'),
            writing_score = request.form.get('writing_score')  # Corrected the typo here
        )
        
        data_df = data.get_data_as_dataframe()
        print(data_df)
        
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(data_df)
        return render_template('home.html', results=round(results[0]))

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
