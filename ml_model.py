import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
from sklearn.metrics import root_mean_squared_error
from sklearn.metrics import r2_score
from utils.model_utils import Plotter
import shap

df = pd.read_csv("ml_data.csv")

# Select the columns to be usedcls
features = [
    "zip_code",
    "type_of_property",
    "building_condition",
    "facade_number",
    "living_area",
    "equipped_kitchen",
    "terrace",
    "garden",
    "subtype_ecoded",
    "latitude",
    "longitude",
    "km_to_capital",
]

target = "price"

# Apply logarithm to the target col, so larger values are more compressed more than
# small ones, making it easier for the model to handle outliers
df["price"] = np.log1p(df["price"])

# Split the data in features and target columns
X = df[features].values
y = df["price"].values.reshape(-1, 1)

# Normalize the data
scaler_x = StandardScaler()
scaler_y = StandardScaler()
X = scaler_x.fit_transform(X)
y = scaler_y.fit_transform(y)

# Split X and y into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# Build model
model = Sequential()
model.add(Dense(128, input_shape=(len(features),), activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.1))
model.add(Dense(32, activation="relu"))
model.add(Dense(1))  # output layer

# Set an optimizer
optimizer = Adam(learning_rate=0.001)

# Compile the model
model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

# Train the model
monitor = EarlyStopping(
    monitor="val_loss",
    min_delta=0.02,
    patience=15,
    verbose=1,
    mode="auto",
    restore_best_weights=True,
)
history = model.fit(
    X_train,
    y_train,
    validation_data=(X_test[:1000], y_test[:1000]),
    callbacks=[monitor],
    shuffle=False,
    epochs=100,
    batch_size=32,
)

# Predict on train set and convert results into real values.
pred_train = model.predict(X_train)
# Convert to real numbers
pred_train_l = scaler_y.inverse_transform(pred_train)
pred_train_actual = np.expm1(pred_train_l)

# y_ train back to real values
y_train_l = scaler_y.inverse_transform(y_train)
y_train_actual = np.expm1(y_train_l)


# make predictions and convert back to real values
predictions = model.predict(X_test)
predictions_l = scaler_y.inverse_transform(predictions)
predictions_actual = np.expm1(predictions_l)

# convert y_test1 back to real values
y_test1_l = scaler_y.inverse_transform(y_test)
y_test_actual = np.expm1(y_test1_l)


#### Evaluate the model  ###
# MAE train/test sets
mae_train = np.mean(np.abs(y_train_actual - pred_train_actual))
print(f"MAE training set: {round(mae_train)}")

mae_test = np.mean(np.abs(y_test_actual - predictions_actual))
print(f"MAE test set: {round(mae_test)}")


# RMSE training/test
rmse_train = round(root_mean_squared_error(pred_train_actual, y_train_actual))
print("RMSE on train set:", rmse_train)

rmse_test = round(root_mean_squared_error(y_test_actual, predictions_actual))
print("RMSE on test set:", rmse_test)

# R2
r2_train = r2_score(y_train_actual, pred_train_actual)
print(f"Train R^2 on training set: {round(r2_train, 3)}")

r2_test = r2_score(y_test_actual, predictions_actual)
print(f"Test R^2 on test set: {round(r2_test, 3)}")


# MAPE on train/test sets
mape_train = np.mean(
    np.abs((y_train_actual - pred_train_actual) / y_train_actual) * 100
)
mape_train = round(mape_train, 2)
print(f"MAPE on train set: {mape_train} %")


mape_test = np.mean(np.abs((y_test_actual - predictions_actual) / y_test_actual) * 100)
mape_test = round(mape_test, 2)
print(f"MAPE on test set: {mape_test} %")

# sMAPE on train/test sets
smape_train = (100 / len(y_train_actual)) * np.sum(2 * np.abs(y_train_actual - pred_train_actual) / (np.abs(y_train_actual) + np.abs(pred_train_actual)))
print(f"sMAPE: {round(smape_train, 2)}%")

smape_test = (100 / len(y_test_actual)) * np.sum(2 * np.abs(y_test_actual - predictions_actual) / (np.abs(y_test_actual) + np.abs(predictions_actual)))
print(f"sMAPE: {round(smape_test, 2)}%")


# plot train/validation loss vs. epochs
loss_plot_name = "Loss vs epochs"
train_loss = history.history["loss"]
train_legend = "Train loss"
loss_plot_x_label = "Epochs"
val_loss = history.history["val_loss"]
loss_plot_val2_legend = "Validation loss"
loss_plot_y_label = "Loss"
loss_pred_plot = Plotter(
    loss_plot_name,
    train_loss,
    train_legend,
    loss_plot_x_label,
    val_loss,
    loss_plot_val2_legend,
    loss_plot_y_label,
)
loss_pred_plot.make_plot()

# plot predictions vs. actual prices - first batch of test data
plot_name = "Actual vs predicted price"
plot_val1_legend = "Actual Price"
plot_x_label = "Observations"
plot_val2_legend = "Predicted price"
plot_y_label = "Price"
pred_plot = Plotter(
    plot_name,
    y_test_actual,
    plot_val1_legend,
    plot_x_label,
    predictions_actual,
    plot_val2_legend,
    plot_y_label,
)
pred_plot.make_plot()

# Visualize feature importance with shap
explainer = shap.Explainer(model, X_train)
sample = X_train[:250]
shap_values = explainer(sample)
shap_values.feature_names = features
shap.summary_plot(shap_values, sample)
shap.plots.bar(shap_values)
