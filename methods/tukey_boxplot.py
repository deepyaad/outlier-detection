"""
@date: created on ues aug 26 2025 @ 4:24pm est
@author: Ananda Francis
@file: tukey_boxplot.py: implementation of Tukey's Boxplot Method for Outlier Detection
"""

class TukeyBoxplot:
    def __init__(self, data):
        self.data = data

    def detect_outliers(self):
        """
        Detect outliers using Tukey's Boxplot method.
        Outliers are defined as points outside 1.5 * IQR from the first and third quartiles.
        """

        # calculate interquartile range (IQR)
        Q1 = self.data.quantile(0.25)
        Q3 = self.data.quantile(0.75)
        IQR = Q3 - Q1

        # calculate bounds for potential and extreme outliers
        inner_lower_bound = Q1 - 1.5 * IQR
        inner_upper_bound = Q3 + 1.5 * IQR

        outer_lower_bound = Q1 - 3 * IQR
        outer_upper_bound = Q3 + 3 * IQR

        # identify potential and extreme outliers
        potential_outliers = self.data[(self.data < inner_lower_bound) | (self.data > inner_upper_bound)]
        extreme_outliers = self.data[(self.data < outer_lower_bound) | (self.data > outer_upper_bound)]
        
        # return results as a dictionary
        outliers = {
            'potential_outliers': potential_outliers,
            'extreme_outliers': extreme_outliers
        }

        return outliers