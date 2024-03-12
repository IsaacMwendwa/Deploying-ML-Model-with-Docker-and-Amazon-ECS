# Imports for Data Preparation and Modeling
import numpy as np  
import pandas as pd
import pickle
from pandas import read_csv, get_dummies
from numpy import concatenate
from math import sqrt
from pandas import DataFrame
from pandas import concat
from category_encoders import BinaryEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer


# Imports for model deployment
from flask import Flask, render_template, request, redirect, url_for, current_app, send_from_directory
import os
from os.path import join, dirname, realpath


# Imports for model monitoring
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *
from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import DataStabilityTestPreset, NoTargetPerformanceTestPreset
from evidently.tests import *



def model_monitoring(current_dataset, reference_dataset):

    # setting current and reference datasets
    current= current_dataset
    reference = reference_dataset

    # Running Data Stability Tests & Data Drift  and Data Quality Reports
    suite = TestSuite(tests=[
        NoTargetPerformanceTestPreset(),
    ])

    suite.run(reference_data=reference, current_data=current)

    return suite




# Full Pipeline Transformer for Numerical and Categorical Data
def pipeline_transformer(data):
    '''
    Complete transformation pipeline for both
    categorical data (Binary Encoding) and 
    numerical data (Passthrough - no transformation)
    
    Argument:
        data: original dataframe 
    Returns:
        data: transformed data, ready to use
    '''
    cat_attrs = ["Industry"]
    
    full_pipeline = ColumnTransformer([
        # transform the categorical data and pass through the numerical columns unchanged
        ("cat", BinaryEncoder(), cat_attrs)], remainder = 'passthrough')    #
    
    transformed_data = full_pipeline.fit_transform(data)
    
    return transformed_data

# function to get predictions from input dataframe
def get_predictions(input_df, model):

    
    #Removing skewness from data
    input_df['Contribution_to_GDP'] = input_df["Contribution_to_GDP"].map(
                                        lambda i: np.log(i) if i > 0 else 0)
    
    # Preparing data using pipeline_transformer()
    prepared_df = pipeline_transformer(input_df)
    
    # Getting Predictions from Model
    pred_results = model.predict(prepared_df)
    
    # Reversing log transform to get actual results
    pred_results = np.exp(pred_results)
    
    # Creating list of predictions
    pred_list = pred_results.tolist()
    pred_list = list(map(int, pred_list))
    #pred_list.sort(reverse = True)

    industry_cols = ['Agriculture, Forestry And Fishing',
                        'Mining And Quarrying',
                        'Manufacturing',
                        'Electricity, Gas, Steam And Air Conditioning Supply',
                        'Water Supply; Sewerage, Waste Management And Remediation Activities',
                        'Construction',
                        'Wholesale And Retail Trade; Repair Of Motor Vehicles And Motorcycles',
                        'Transportation And Storage',
                        'Accommodation And Food Service Activities',
                        'Information And Communication',
                        'Financial And Insurance Activities',
                        'Real Estate Activities',
                        'Professional, Scientific And Technical Activities',
                        'Administrative And Support Service Activities',
                        'Public Administration And Defence; Compulsory Social Security',
                        'Education',
                        'Human Health And Social Work Activities',
                        'Arts, Entertainment And Recreation',
                        'Other Service Activities',
                        'Activities Of Households As Employers; Undifferentiated Goods- And Services-Producing Activities Of Households For Own Use',
                        'Activities Of Extraterritorial Organizations And Bodies'
                    ]
    
    # Create Dictionary of Industry and Predicted Values
    pred_dict = {industry_cols[i]: pred_list[i] for i in range(len(industry_cols))}
    
    # Return Dictionary of Industry and Predicted Values
    return pred_dict, pred_list

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
    keys = list(dict.keys())
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
    percent_dict = percent_list_rounded
    
    # Create Dictionary of Industry and Predicted Values
    percent_dict = {keys[i]: percent_dict[i] for i in range(len(keys))}

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

# LOADING THE MODELS
with open("working_poor_model.bin", 'rb') as f_in:
    working_poor_model = pickle.load(f_in)

with open("total_number_in_employment_model.bin", 'rb') as f_in:
    total_number_in_employment_model = pickle.load(f_in)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

# Model Monitoring Report URL
@app.route('/model_monitoring_report')
def model_monitoring_report():
    return render_template('model_monitoring.html')



@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    #return send_from_directory(directory=uploads, filename=filename)  
    return send_from_directory(uploads, filename)  


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
    
    #else: 
    #    print("Enter a CSV File")    

    


@app.route('/prediction/<path:filePath>')
def prediction(filePath):

    # CSV Column Names
    col_names = ['Industry', 'Contribution_to_GDP']

    #READING DATASET FOR WORKING POOR & TOTAL EMPLOYMENT
    # Use Pandas to parse the CSV file

    try: 
        working_poor_df = read_csv(filePath, names = col_names, header=0)
        total_employment_df = read_csv(filePath, names = col_names, header=0)
    except BaseException as e:
        print("Invalid File Format") 
        return render_template('index.html')

    
    #predictions for working poor
    working_poor_dict_pred_unsorted, pred_list = get_predictions(input_df = working_poor_df, 
                                           model = working_poor_model)
    
    #predictions for total employment
    total_employment_dict_pred_unsorted, t_pred_list = get_predictions(input_df = total_employment_df,
                                               model = total_number_in_employment_model)

    #sorting dict in descending order
    working_poor_dict_pred = sort_dict(dict = working_poor_dict_pred_unsorted)
    total_employment_dict_pred = sort_dict(dict = total_employment_dict_pred_unsorted)

    #computing percentage contribution by sector
    working_poor_percent_dict_unsorted = compute_percent(dict = working_poor_dict_pred)
    total_employment_percent_dict_unsorted = compute_percent(dict = total_employment_dict_pred)
    
    #sorting percent in descending order
    working_poor_percent_dict = sort_dict(dict = working_poor_percent_dict_unsorted)
    total_employment_percent_dict = sort_dict(dict = total_employment_percent_dict_unsorted)

    #computing percentage of working poor
    total_working_poor = compute_total(dict = working_poor_dict_pred)
    total_employment_total = compute_total(dict = total_employment_dict_pred)
    percent = (total_working_poor/total_employment_total)*100
    working_poor_percent = round(percent, 2)

    
    # MODEL MONITORING
    # Setting paths of current and reference datasets
    file_path_reference = os.path.join(app.config['UPLOAD_FOLDER'], "Working_Poor_Model_Dataset.csv")
    
    # Reference dataset (Training)
    reference_dataset = pd.read_csv(file_path_reference, header=0) 
    reference_dataset.rename(columns={'Wage_bracket_0_to_9999': 'target'}, inplace=True)
    reference_dataset['prediction'] = reference_dataset['target'].values + np.random.randint(0, 5, reference_dataset.shape[0])
   

    # Current Dataset (Production)
    current_dataset = working_poor_df   
    current_dataset['Wage_bracket_0_to_9999'] = list(map(int, pred_list))
    current_dataset.rename(columns={'Wage_bracket_0_to_9999': 'target'}, inplace=True)

    final_year_dataset = reference_dataset[147:]

    current_dataset['prediction'] = final_year_dataset['target'].values + np.random.randint(0, 5, final_year_dataset.shape[0])
   

    # Calling Model Monitoring Function
    suite = model_monitoring(current_dataset, reference_dataset)
    report_file_path = os.path.join("templates", 'model_monitoring.html')
    suite.save_html(report_file_path)

    
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