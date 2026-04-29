import pickle
import numpy as np

# Load model
model = pickle.load(open("model/model.pkl", "rb"))

def predict_diabetes(input_data):
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)

    return "Diabetic" if prediction[0] == 1 else "Not Diabetic"


# Example
if __name__ == "__main__":
    sample = [2,120,70,20,85,30.5,0.5,25]
    print(predict_diabetes(sample))
