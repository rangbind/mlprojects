import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.logger import logging
from src.exception import CustomException

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')
    
class DataTransformation:
    def __init__(self):
        self.data_transformation = DataTransformationConfig()
    
    def get_data_transformer_obj(self):
        try:
            numerical_features = ['readingScore', 'writingScore']
            categorical_features = ['gender', 'raceEthnicity', 'parentaLevelOfEducation', 'lunch', 'testPreparationCourse']

            num_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="median")),
                    ("Scaler", StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("Imputer", SimpleImputer(strategy="most_frequent")),
                    ("OneHotEncoder", OneHotEncoder())
                ]
            )

            logging.info("Handled missing values for both numerical and categorical features")
            logging.info("Numerical features are scaled")
            logging.info("Categorical features are encoded using OneHotEncoder")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features)
                ]
            )

            return preprocessor
        except Exception as e:
            logging.error(f"Error in get_data_transformer_obj: {str(e)}")
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            preprocessing_obj = self.get_data_transformer_obj()
            
            target_column_name = 'mathScore'

            input_features_train = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train = train_df[target_column_name]

            input_features_test = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test = test_df[target_column_name]
            
            logging.info("Applying preprocessor object on training and testing dataframe")

            train_features = preprocessing_obj.fit_transform(input_features_train)
            test_features = preprocessing_obj.transform(input_features_test)

            logging.info(f"Processed train data shape: {train_features.shape}")
            logging.info(f"Processed test data shape: {test_features.shape}")

            train_data = np.c_[train_features, np.array(target_feature_train)]
            test_data = np.c_[test_features, np.array(target_feature_test)]

            os.makedirs(os.path.dirname(self.data_transformation.preprocessor_obj_file_path), exist_ok=True)
            
            save_object(
                file_path=self.data_transformation.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Saved Preprocessing object successfully")

            return (
                train_data,
                test_data,
                self.data_transformation.preprocessor_obj_file_path
            )
        except Exception as e:
            logging.error(f"Error in initiate_data_transformation: {str(e)}")
            raise CustomException(e, sys)
