import sys
import pandas as pd

from src.exception import CustomException
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocesor_path = 'artifacts/preprocessor.pkl'
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocesor_path)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:
    def __init__(self,
            gender: str,
            race_enthnicity: str,
            parental_level_of_education: str,
            lunch: str,
            test_preparation_course: str,
            reading_score: int,
            writing_score: int
        ):
        self.gender = gender
        self.race_enthnicity = race_enthnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score
    
    def get_data_as_dataframe(self):
        try:            
            df = pd.DataFrame({  
                            "gender": [self.gender],
                            "raceEthnicity": [self.race_enthnicity],
                            "parentaLevelOfEducation": [self.parental_level_of_education],
                            "lunch": [self.lunch],
                            "testPreparationCourse": [self.test_preparation_course],
                            "readingScore": [self.reading_score],
                            "writingScore": [self.writing_score],
                        })
            return df
        except Exception as e:
            raise CustomException(e, sys)