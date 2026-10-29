from fastapi import FastAPI
from model.predict import predict_output,model,Model_version
from fastapi.responses import JSONResponse
from schema.User_input import userInput
from schema.prediction_response import PredictionResponse

app=FastAPI()

@app.get('/')
def home():
    return {'message':'Insurance Premium Prediction API'}

@app.get('/health')
def health_check():
    return {'status':'OK',
            'version': Model_version,
            'model_loaded': model is not None
            }


@app.post('/predict',response_model=PredictionResponse)
def predict_premium(data:userInput):
    user_input={
        'bmi':data.bmi,
        'age_group':data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier':data.city_tier,
        'income_lpa':data.income_lpa,
        'occupation':data.occupation
    }
    try:
        prediction=predict_output(user_input)
        return JSONResponse(status_code=200,content={'response':prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
