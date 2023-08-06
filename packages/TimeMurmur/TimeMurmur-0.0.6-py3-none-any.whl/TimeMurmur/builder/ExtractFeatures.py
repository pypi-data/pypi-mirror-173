# -*- coding: utf-8 -*-
from TimeMurmur.utils.FeatureExtraction import FeatureExtraction


class ExtractFeatures:

    def __init__(self,
                 run_dict):
        self.run_dict = run_dict
        self.id_column = self.run_dict['global']['ID Column']
        self.date_column = self.run_dict['global']['Date Column']
        self.target_column = self.run_dict['global']['Target Column']

    def extract(self, df):
        y = df[self.target_column]
        extractor = FeatureExtraction(y, max(self.seasonal_period))
        features = extractor.extract()
        features[self.id_column] = df[self.id_column].iloc[0]
        return features

    def build_axis(self, dataset):
        dataset = dataset[[self.id_column,
                           self.date_column,
                           self.target_column]]
        extracted_features = dataset.groupby(self.id_column).apply(self.extract)
        self.run_dict['global']['ts_features'] = extracted_features
