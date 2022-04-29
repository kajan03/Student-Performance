from flask import Flask,render_template,request,jsonify
import pandas as pd
import student


app = Flask(__name__)

# @app.route('/',methods=['POST','GET',])
# def index():
#     if  request.method == 'POST':
#         user_input = request.form.get('marks')
#         print(user_input)
#         prediction=student.performance_predict(user_input)
#         print(prediction)
#     return render_template('home.html')

@app.route("/predict",methods=["POST"])
def predict():
    json_ = request.json
    query_df = pd.DataFrame(json_)
    prediction = student.performance_predict(query_df)
    return jsonify({"Prediction" : list(prediction)})

if __name__ == "__main__":
        app.run(debug=True)

