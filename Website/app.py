from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

def prediction(lst):
    filename = 'model/model.pkl'
    with open(filename, 'rb') as file:
        model_dict = pickle.load(file)  # Load the dictionary
    
    # Extract the model and feature names
    model = model_dict['model']
    feature_names = model_dict['features_names']
    
    # Ensure the input list has the same order as the feature names
    if len(lst) != len(feature_names):
        raise ValueError(f"Expected {len(feature_names)} features, but got {len(lst)}")
    
    pred_value = model.predict([lst])
    return pred_value[0]

@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = -1  # Default value for pred_value (invalid state)

    if request.method == 'POST':
        # Use .get() to avoid KeyError if a key is missing
        pressure = request.form.get('pressure')
        dewpoint = request.form.get('dewpoint')
        humidity = request.form.get('humidity')
        cloud = request.form.get('cloud')
        sunshine = request.form.get('sunshine')
        winddirection = request.form.get('winddirection')
        windspeed = request.form.get('windspeed')

        try:
            feature_list = [
                int(pressure),
                int(dewpoint),
                int(humidity),
                int(cloud),
                int(sunshine),
                int(winddirection),
                int(windspeed)
            ]
        except (ValueError, TypeError) as e:
            print(f"Error converting form data to integers: {e}")
            feature_list = [0, 0, 0, 0, 0, 0, 0]  # Default values or handle the error appropriately

        pred_value = prediction(feature_list)
        print(f"Prediction: {pred_value}")

    return render_template('index.html', pred_value=pred_value)

if __name__ == '__main__':
    app.run(debug=True)