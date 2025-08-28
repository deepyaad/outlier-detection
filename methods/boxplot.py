"""
@date: created on ues aug 26 2025 @ 4:24pm est
@author: Ananda Francis
@file: tukey_boxplot.py: implementation of Tukey's Boxplot Method for Outlier Detection
"""

import pandas as pd
import numpy as np

class Boxplot:
    def __init__(self, data):
        self.data = data

        self.Q1 = None
        self.Q2 = None
        self.Q3 = None
        self.IQR = None

        self.lower_bound = None
        self.upper_bound = None

        self.outliers = None

        self.boxplot_types = ['tukey_extreme', 'tukey_potential', 'semi_iqr_kimber', 'semi_iqr_adapted']

    def _calculate_iqr(self):
        
        # calculate interquartile range (IQR)
        self.Q1 = self.data.quantile(0.25)
        self.Q2 = self.data.median()
        self.Q3 = self.data.quantile(0.75)
        self.IQR = self.Q3 - self.Q1


    def detect_outliers(self, type='tukey_extreme'):
        """
        Detect outliers in the dataset using Tukey's Boxplot method.
        Outliers are defined as points outside 1.5 * IQR from the first and third quartiles.
        """

        self._calculate_iqr()

        if type == 'tukey_extreme':
            # extreme outliers using Tukey's method
            self.lower_bound = self.Q1 - 3 * self.IQR
            self.upper_bound = self.Q3 + 3 * self.IQR

        elif type == 'tukey_potential':
            # potential outliers using Tukey's method
            self.lower_bound = self.Q1 - 1.5 * self.IQR
            self.upper_bound = self.Q3 + 1.5 * self.IQR

        elif type == 'semi_iqr_kimber':
            # outliers using Kimber's Semi-IQR Boxplot method
            siqr_upper = 2 * (self.Q3 - self.Q2)
            siqr_lower = 2 * (self.Q2 - self.Q1)
            self.lower_bound = self.Q1 - (1.5 * siqr_lower)
            self.upper_bound = self.Q3 + (1.5 * siqr_upper)

        elif type == 'semi_iqr_adapted':
            # outliers using Kimber's Semi-IQR Boxplot method with adaptations from Dastjerdy et al. (2023), Saleem et al. (2021), Hubert and Vandervieren (2008), and Walker et al. (2018)
            siqr_upper = self.Q3 - self.Q2
            siqr_lower = self.Q2 - self.Q1
            self.lower_bound = self.Q1 - (3 * siqr_lower)
            self.upper_bound = self.Q3 + (3 * siqr_upper)

        else:
            raise ValueError(f"type must be one of {self.boxplot_types}")
        

        # find values of outliers
        self.outliers = self.data[(self.data < self.lower_bound) | (self.data > self.upper_bound)]
        return self.outliers

    def remove_outliers(self):
        """
        Remove outliers from the dataset using Tukey's Boxplot method.
        Returns a cleaned dataset without potential and extreme outliers.
        """

        if self.outliers is None:
            self.detect_outliers()

        cleaned_data = self.data[(self.data >= self.lower_bound) & (self.data <= self.upper_bound)]
        return cleaned_data
        

    def get_bounds(self):
        """
        Get the calculated bounds for potential and extreme outliers.
        Returns a dictionary with inner and outer bounds.
        """
        # ensure the bounds are calculated
        self.detect_outliers()
        
        return {
            'lower_bound': self.lower_bound,
            'upper_bound': self.upper_bound,
        }