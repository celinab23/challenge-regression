# challenge-regression

### Description

This repository corresponds to the machine learning stage or a larger data project: immo-eliza. <br>
The objective of this part of the project is to train a neural network regression model to predict the price of a property. <br><br>

The following steps have been taken towards this goal: <br> 
 - Prepare the data for machine learning (Data Pre-processing).<br>
 - Build, train and evaluate the machine learning model.
 - Hyperparameter tuning<br><br>

 In the repository you will find two versions of the work: Jupyter notebooks and python files.<br>
 For a detailed step by step guide of the projects, please consult the files in the "notebooks" folder. <br>
 For a straight forward version of the python code used for data pre-processing and machine learning, <br>
 please refer to the files on the main page of the repository.

### Installation<br>
- 1. Clone the repo: ```git clone https://github.com/celinab23/challenge-regression.git``` <br>
- 2. Install the necessary libraries (requirements.txt). <br>
- 3. You are ready to run the code.

### Usage

- Start with data-preprocessing.ipynb and then proceed with model.ipynb<br>

If using via Jupyter notebooks:<br>
- Execute the code cells in order from top to bottom.<br><br>

If using via python files:<br>
- Execute ```python <file_name (data-preprocess.py or ml_model.py)>``` on your console.<br>

(visuals)

### Contributors<br>
- Celina Bolaños<br><br>

### Timeline<br>
- Day 1: <br>
    - Short search about options for neural networks regression models. <br>
        Found two options: Sklearn and TensorFlow. <br>
    - Follow introduction chapter to TensorFlow on DataCamp. <br>
    - Started the date pre-processing under data-preprocessing.ipynb .<br><br>

- Day 2: <br>
    - Finished data preprocessing. <br>
        Formated the preprocessing notebook with markdown. <br>
        Created the data-preprocessing.py file containing the functions used during such process.<br>
    - Feature engineering <br>
        Calculated the distance of each property to the capital of the province it is situated in. <br><br>

- Day 3: <br>
    - Followed part of the Introduction to Deep Learning with Keras course in DataCamp.<br>
    - Read about how to create a neural network regression model.<br>
    - From there, a very basic model was built. However, was unable to measure its accuracy.<br>
    - Part of the pre-processing had to be remade, to appropiately handle type of property<br><br>

- Day 4:<br>
    - Model was completed but returning very high Root Mean Squared Error (299880).<br>
    - Data preprocessing notebook transferred to .py file.<br>
    - encode_kitchen function defined and transferred to utils file.<br><br>

- Day 5:<br>
    - Measure model's performance.<br>
    - Hyperparameter tuning. <br>
    - Test with different versions of the data set.<br><br>


### Personal situation<br>
Data preprocessing took a significant amount of time. <br>
Feature engineering was also a time-consuming challege. <br>
However, not as long as the pre-processing step. <br>
There was a huge gap of knowledge about neural networks models,<br>
not theorical, but rather of the actual coding steps to be taken in other<br>
to build the model, evaluate its performance and tune it.<br><br>
Additional time must also be invested in learning more about the mathematical<br>
calculations that take place behind the scenes when using the model and<br>
evaluating its performance.<br>

