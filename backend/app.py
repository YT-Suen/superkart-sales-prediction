
# suggested by Gemini
import pickle
import joblib

# Global unpickler patch to catch missing scikit-learn internal classes
_original_find_class = pickle.Unpickler.find_class

def _patched_find_class(self, module, name):
    if module == 'sklearn.compose._column_transformer' and name == '_RemainderColsList':
        class _RemainderColsList(list):
            """Compatibility shim for scikit-learn model unpickling."""
            pass
        return _RemainderColsList
    return _original_find_class(self, module, name)

# Apply the patch globally to Python's unpickler
pickle.Unpickler.find_class = _patched_find_class

# Now safely load your model
model = joblib.load("rf_tuned.joblib")
print("Model loaded successfully!")

# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize Flask app with a name
superkart_api = Flask("SuperKart")

# suggested by Gemini
#import sklearn.compose._column_transformer as ct_module

# Robust compatibility shim for _RemainderColsList
#if not hasattr(ct_module, '_RemainderColsList'):
#    class _RemainderColsList(list):
#        """Compatibility shim for scikit-learn model unpickling."""
#        pass
#    setattr(ct_module, '_RemainderColsList', _RemainderColsList)

# Now safely load your model

# Load the trained model
#model = joblib.load("superkart_model.joblib")
#model = joblib.load("rf_tuned.joblib")




# Define a route for the home page
@superkart_api.get('/')
def home():
    return "Welcome to the SuperKart System"

# Define an endpoint to predict sales for a single product
@superkart_api.post('/v1/predict')
def predict_sales():
    # Get JSON data from the request
    data = request.get_json()

    # Extract relevant features from the input data
    sample = {
    'Product_Weight': data['Product_Weight'],
    'Product_Sugar_Content': data['Product_Sugar_Content'],
    'Product_Allocated_Area': data['Product_Allocated_Area'],
    'Product_MRP': data['Product_MRP'],
    'Store_Size': data['Store_Size'],
    'Store_Location_City_Type': data['Store_Location_City_Type'],
    'Store_Type': data['Store_Type'],
    'Product_Id_char': data['Product_Id_char'],
    'Store_Age_Years': data['Store_Age_Years'],
    'Product_Type_Category': data['Product_Type_Category']
}

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # Make a prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Sales': prediction})

# Define an endpoint to predict sales for a batch of products
@superkart_api.post('/v1/predictbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Create an output dictionary mapping row index to predicted sales
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predictions)}

    return output_dict


# Run the Flask app in debug mode
if __name__ == '__main__':
    superkart_api.run(debug=True)

  #if __name__ == '__main__':
  #  superkart_api.run(host='0.0.0.0', port=7860, debug=True)  
