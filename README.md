# Insurance Premium Prediction API

A FastAPI service that predicts a user's insurance premium category (for example **Low**, **Medium** or **High**) from basic personal details. A pre-trained scikit-learn classifier does the prediction; the API validates the input and derives the model's features from it.

## Features

- REST API built with **FastAPI**, with interactive docs at `/docs`
- Input validation with **Pydantic v2**
- Derived features computed from the raw input:
  - **BMI**: `weight / height²`
  - **Age group**: `young` (<25), `adult` (25–44), `middle_aged` (45–59), `senior` (60+)
  - **Lifestyle risk**: `high` (smoker and BMI > 30), `medium` (smoker or BMI > 27), otherwise `low`
  - **City tier**: 1, 2 or 3, based on the city lists in `config/city_tier.py`
- Returns the predicted class, a confidence score and the probability of each class
- Docker image for deployment

## Project structure

```
insurance_premium/
├── app.py                        # FastAPI app and endpoints
├── config/
│   └── city_tier.py              # Tier 1 and tier 2 city lists
├── model/
│   ├── model.pkl                 # Trained scikit-learn model
│   └── predict.py                # Loads the model and runs predictions
├── schema/
│   ├── User_input.py             # Request schema and derived features
│   └── prediction_response.py    # Response schema
├── requirements.txt
└── dockerfile
```

## Getting started

### Prerequisites

- Python 3.11
- pip

### Run locally

```bash
python -m venv .venv
```

Activate the environment (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` on macOS/Linux), then:

```bash
pip install -r requirements.txt
```

```bash
uvicorn app:app --reload
```

The API is then available at http://127.0.0.1:8000, with interactive docs at http://127.0.0.1:8000/docs.

> Start the server from the project root: `model/predict.py` opens `model/model.pkl` with a relative path.

### Run with Docker

```bash
docker build -t insurance-premium-api -f dockerfile .
```

```bash
docker run -p 8000:8000 insurance-premium-api
```

## API reference

### `GET /`

Returns a welcome message.

```json
{ "message": "Insurance Premium Prediction API" }
```

### `GET /health`

Health check, with the model version and whether the model loaded.

```json
{ "status": "OK", "version": "1.0.0", "model_loaded": true }
```

### `POST /predict`

Predicts the premium category for one user.

**Request body**

| Field        | Type    | Constraints                                                                                                  | Description                 |
|--------------|---------|--------------------------------------------------------------------------------------------------------------|-----------------------------|
| `age`        | integer | 0 < age < 120                                                                                                | Age in years                |
| `weight`     | float   | > 0                                                                                                          | Weight in kg                |
| `height`     | float   | 0 < height < 2.5                                                                                             | Height in metres            |
| `income_lpa` | float   | > 0                                                                                                          | Annual income in lakhs (LPA)|
| `smoker`     | boolean |                                                                                                              | Whether the user smokes     |
| `city`       | string  | Trimmed and title-cased                                                                                      | City of residence           |
| `occupation` | string  | One of `retired`, `freelancer`, `student`, `government_job`, `business_owner`, `unemployed`, `private_job` | Occupation                  |

**Example request**

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" -d "{\"age\": 30, \"weight\": 72.5, \"height\": 1.75, \"income_lpa\": 12, \"smoker\": false, \"city\": \"Mumbai\", \"occupation\": \"private_job\"}"
```

**Example response**

```json
{
  "response": {
    "predicted_category": "Low",
    "confidence": 0.8432,
    "class_probabilities": { "Low": 0.8432, "Medium": 0.1401, "High": 0.0167 }
  }
}
```

If prediction fails, the API returns HTTP 500 with the error message.

## Model

- Pickled scikit-learn classifier, stored at `model/model.pkl`
- Features passed to the model: `bmi`, `age_group`, `lifestyle_risk`, `city_tier`, `income_lpa`, `occupation`
- Model version: `1.0.0` (set in `model/predict.py`)

## Tech stack

FastAPI · Uvicorn · Pydantic · scikit-learn · pandas · Docker
