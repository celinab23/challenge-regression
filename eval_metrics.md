## Model evaluation report - Neural network <br>

#### The final dataset

The data set used was the same from the previuos state of this project: data analysis. <br>
For the pre-processing, these fields were removed: <br><br>

- Unecessary colums: swimming_pool, furnished, open_fire, sub_property_group_encoded, plot surface <br>
- Columns which have high correlation with others: bedroom_nr <br>
- Properties of type "other" and "mixed used building". <br>
- Apartments with more than 4 facades <br><br>

Further in data preparations, the following steps were taken: <br>
- Encoded the sub-type of the property from 1 to 20 according to the average price per property sub-type.<br>
- Encoded building condition and kitchen status. <br>
- Checked for duplicates <br>
- Removed outliers.<br>
- Scaling/Normalizing all features.<br><br>

Feature engineering: <br>
- Added: <br>
        - Latitude and longitude of the zipcode where the property is located.<br>
        - Calculated the distance of the property's zip code to the capital of the province where it is located.<br><br>


The final data set had 16600 observations and 13 variables (12 features + 1 target). <br>


#### Model instantiation and parameters: <br><br>

```
model = Sequential()
model.add(Dense(128, input_shape=(len(features),), activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.1))
model.add(Dense(32, activation="relu"))
model.add(Dense(1))

optimizer = Adam(learning_rate=0.001)

model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])
```
<br>

#### Feature that were used:
-   Type of property (house or apartment) <br>
-   Subtype of the property (kot, studio, bungallow, villa...) <br>
-   Building_condition (to restore, to renovate, good)<br>
-   Facade number <br>
-   Living area (in square meters)<br>
-   Equipped kitchen (unistalled, installed, equipped)<br>
-   Terrace (area in square meters)<br>
-   Garden (area in square meters)<br>
-   Zip code of the commune where the property is located <br>
-   Latitude (of the zip code) <br>
-   Longitude (of the zip code) <br>
-   Distance from the property's zip code to the province's capital <br><br>


#### Accuracy 

Data as split into 80% for training and 20% for testing.<br>
Test data was split into two batches:<br>
    - One for testing during hyperparameters tuning<br>
    - Another for final test once the model was completed.
Finally, the test data was put back into one batch for the final verion of the model file.


Accurary for both training and test set was around 20% as per the below MAPE.<br><br>

#### Efficiency

Training and predictions take less than a mitue each.<br><br>

#### Evaluation of the model:

MAE training set: 76834 <br>
MAE test set: 84285         <br>                                                  
RMSE on train set: 128355  <br>                                                                             
RMSE on test set: 137309       <br>                                                                         
Train R^2 on training set: 0.752    <br>                                                                    
Test R^2 on test set: 0.73    <br>                                                                          
MAPE on train set: 18.36 %    <br>                                                                          
MAPE on test set: 19.85 %    <br>                                                                           
sMAPE train: 17.37%      <br>                                                                                     
sMAPE test: 18.69% <br><br>


How could you improve this result?<br>
- Spliting the test further per house or apartment could yield a better result.<br><br>

Which part of the process has the most impact on the results?<br><br>
- Data preparation and feature engineering. <br>
As trials were done adding and removing different features, there was a noticeable improvement in the model's accuracy.<br>
When latitude, longitude and distance to the capital were added, the performance was significantly improved.<br>
Hoewever, this does not rest importance to the model creation. A model created with further knowledge and experience could 
produce even better results than the current one.<br><br>

How should you divide your time working on this kind of project?<br>
Probably 60-65% in data preparation and 40-35 percent in building, training, evaluating and tunning the model, as per this first experience.<br>
