from flask import Flask, render_template, request, redirect, url_for, current_app, send_from_directory
import os
from os.path import join, dirname, realpath

import numpy as np  
import pandas as pd
import pickle
from pandas import read_csv, get_dummies
from numpy import concatenate
from math import sqrt
from pandas import DataFrame
from pandas import concat

from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


# Pipeline for pre-processing data: Scaling and numerical transformation
def num_pipeline_transformer(data):
    '''
    Function to process numerical transformations
    Argument:
        data: original dataframe 
    Returns:
        num_attrs: numerical dataframe
        num_pipeline: numerical pipeline object
        
    '''
    numerics = ['float64', 'int64']

    num_attrs = data.select_dtypes(include=numerics)

    num_pipeline = Pipeline([
        ('std_scaler', StandardScaler()),
        ])
    return num_attrs, num_pipeline

# Pipeline for pre-processing data: One hot encoding
def pipeline_transformer(data):
    '''
    Complete transformation pipeline for both
    nuerical and categorical data.
    
    Argument:
        data: original dataframe 
    Returns:
        prepared_data: transformed data, ready to use
    '''
    cat_attrs = ["Industry"]
    num_attrs, num_pipeline = num_pipeline_transformer(data)
    full_pipeline = ColumnTransformer([
        ("num", num_pipeline, list(num_attrs)),
        ("cat", OneHotEncoder(), cat_attrs),
        ])
    prepared_data = full_pipeline.fit_transform(data)
    return prepared_data

def return_prediction(model, dataset):
    
    # preparing data using pipeline transformer
    prepared_data = pipeline_transformer(dataset)

    print(prepared_data.shape)
    
    # make a prediction
    predictions = model.predict(prepared_data)

    return predictions


#function to generate a dictionary from two lists
def return_pred_dict(results):
    # Type casting predictions to int
    #results = list(map(int, results))
    list_pred = results
    list_industry_keys = ['Agriculture, Forestry And Fishing', 'Mining And Quarrying',
       'Manufacturing',
       'Electricity, Gas, Steam And Air Conditioning Supply',
       'Water Supply; Sewerage, Waste Management And Remediation Activities',
       'Construction',
       'Wholesale And Retail Trade; Repair Of Motor Vehicles And Motorcycles',
       'Transportation And Storage',
       'Accommodation And Food Service Activities',
       'Information And Communication',
       'Financial And Insurance Activities', 'Real Estate Activities',
       'Professional, Scientific And Technical Activities',
       'Administrative And Support Service Activities',
       'Public Administration And Defence; Compulsory Social Security',
       'Education', 'Human Health And Social Work Activities',
       'Arts, Entertainment And Recreation', 'Other Service Activities',
       'Activities Of Households As Employers; Undifferentiated Goods- And Services-Producing Activities Of Households For Own Use',
       'Activities Of Extraterritorial Organizations And Bodies']
    
    # using dictionary comprehension 
    # to convert lists to dictionary 
    dict_pred = {list_industry_keys[i]: list_pred[i] for i in range(len(list_industry_keys))} 
    
    return dict_pred


#function for sorting dict in descending order
def sort_dict(dict):
    #Sorting dict in descending order
    sorted_dict = {}
    sorted_keys = sorted(dict, key=dict.get, reverse = True)

    for w in sorted_keys:
        sorted_dict[w] = dict[w]

    return sorted_dict

#function for computing percentage contribution of each sector
def compute_percent(dict):
    values = dict.values()
    total= 0
    for v in values:
        total += v
    
    percent_list = []
    for x in values:
        percent = (x/total)*100
        percent_list.append(percent)

    #rounding percentages to 2 decimal places
    percent_list_rounded = [round(num, 2) for num in percent_list]
    percent_dict = return_pred_dict(results = percent_list_rounded)

    return percent_dict

def compute_total(dict):
    values = dict.values()
    total= 0
    for v in values:
        total += v 
    
    return total



app = Flask(__name__, template_folder="templates")

# enable debugging mode
app.config["DEBUG"] = True

# LOADING THE MODEL AND THE SCALER
with open("working_poor_model.bin", 'rb') as f_in:
    working_poor_model = pickle.load(f_in)

with open("total_employment_model.bin", 'rb') as f_in:
    total_employment_model = pickle.load(f_in)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(directory=uploads, filename=filename)    


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           prediction(file_path)
           
      return redirect(url_for("prediction", filePath=file_path))


@app.route('/prediction/<path:filePath>')
def prediction(filePath):

    #READING DATASET FOR WORKING POOR
    # CSV Column Names
    col_names = ['Industry', 'Contribution_by_Gdp', 'Growth_of_GDP']
    # Use Pandas to parse the CSV file
    working_poor_df = read_csv(filePath, names = col_names, header=0)

    #Reorder columns
    cols = ['Contribution_by_Gdp', 'Growth_of_GDP', 'Industry']
    working_poor_df = working_poor_df.reindex(columns=cols)

    #Cleaning dataset
    #cols = ['Wage_bracket_0_to_9999', 'Total_number_in_wage_employment']
    #df[cols] = df[cols].astype(str)  # cast to string

    # Removing special characters
    #df[cols] = df[cols].replace({'\$': '', ',': '', '-': ''}, regex=True)

    #working_poor_df = df

    #READING DATASET FOR TOTAL EMPLOYMENT
    # CSV Column Names
    col_names = ['Industry', 'Contribution_by_Gdp', 'Growth_of_GDP']
    # Use Pandas to parse the CSV file
    total_employment_df = read_csv(filePath, names = col_names, header=0)

    #Reorder columns
    cols = ['Contribution_by_Gdp', 'Growth_of_GDP', 'Industry']
    total_employment_df = total_employment_df.reindex(columns = cols)
    #total_employment_df.head()

    #Cleaning dataset
    #cols = ['Wage_bracket_0_to_9999', 'Total_number_in_wage_employment']
    #df[cols] = df[cols].astype(str)  # cast to string

    # Removing special characters
    #df[cols] = df[cols].replace({'\$': '', ',': '', '-': ''}, regex=True)

    
    #predictions for working poor
    results_working_poor = return_prediction(model = working_poor_model, dataset = working_poor_df)
    #predictions for total employment
    results_total_employment = return_prediction(model = total_employment_model, dataset = total_employment_df)

    #converting array of predictions to list
    working_poor_list = results_working_poor.astype(int).tolist()
    total_employment_list = results_total_employment.astype(int).tolist()
    print(len(working_poor_list))
    print(len(total_employment_list))

    #getting results of prediction as dictionaries
    working_poor_dict_pred_unsorted = return_pred_dict(results = working_poor_list)
    total_employment_dict_pred_unsorted = return_pred_dict(results = total_employment_list)
    
    #sorting dict in descending order
    working_poor_dict_pred = sort_dict(dict = working_poor_dict_pred_unsorted)
    total_employment_dict_pred = sort_dict(dict = total_employment_dict_pred_unsorted)

    #computing percentage contribution by sector
    working_poor_percent_dict_unsorted = compute_percent(dict = working_poor_dict_pred_unsorted)
    total_employment_percent_dict_unsorted = compute_percent(dict = total_employment_dict_pred_unsorted)
    
    #sorting percent in descending order
    working_poor_percent_dict = sort_dict(dict = working_poor_percent_dict_unsorted)
    total_employment_percent_dict = sort_dict(dict = total_employment_percent_dict_unsorted)

    #computing percentage of working poor
    total_working_poor = compute_total(dict = working_poor_dict_pred_unsorted)
    total_employment_total = compute_total(dict = total_employment_dict_pred_unsorted)
    percent = (total_working_poor/total_employment_total)*100
    working_poor_percent = round(percent, 2)
    
    #rendering results
    return render_template('prediction.html', 
        working_poor_dict_pred = working_poor_dict_pred, 
        total_employment_dict_pred = total_employment_dict_pred,
        working_poor_percent_dict = working_poor_percent_dict,
        total_employment_percent_dict = total_employment_percent_dict,
        working_poor_percent = working_poor_percent)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)