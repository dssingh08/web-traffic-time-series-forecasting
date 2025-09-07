import pickle
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pickle
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import pandas as pd
from app.schemas import PredictionRequest, UserCreate, User
from app import auth, models, database
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

models = {}

@app.on_event("startup")
async def startup_event():
    with open("model/arima_model.pkl", "rb") as f:
        models["arima"] = pickle.load(f)
    with open("model/arma_model.pkl", "rb") as f:
        models["arma"] = pickle.load(f)
    with open("model/auto_arima_model.pkl", "rb") as f:
        models["auto_arima"] = pickle.load(f)
    with open("model/holt_add_seasonal.pkl", "rb") as f:
        models["holt_add_seasonal"] = pickle.load(f)
    with open("model/holt_add.pkl", "rb") as f:
        models["holt_add"] = pickle.load(f)
    with open("model/simple_exp_smoothing.pkl", "rb") as f:
        models["simple_exp_smoothing"] = pickle.load(f)
    models["cnn"] = load_model("model/cnn_model.keras")
    models["cnn_60"] = load_model("model/cnn_model_60_epochs.keras")


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.get("/login")
async def login():
    return FileResponse('static/login.html')

@app.get("/register")
async def register():
    return FileResponse('static/register.html')

@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = auth.get_user(db, username=user.username)
    if db_user:
        raise auth.HTTPException(status_code=400, detail="Username already registered")
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise auth.HTTPException(status_code=400, detail="Email already registered")
    return auth.create_user(db=db, user=user)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.get_user(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise auth.HTTPException(
            status_code=auth.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/predict")
def predict(request: PredictionRequest, current_user: str = Depends(auth.get_current_user)):
    model_name = request.model_name
    days = request.days
    
    model = models[model_name]
    
    # Load test data
    test_df = pd.read_csv("test.csv")
    test_df["Date"] = pd.to_datetime(test_df["Date"])
    
    if model_name == "arima":
        forecast = model.forecast(steps=days)
        dates = pd.date_range(start=test_df["Date"].iloc[0], periods=days)
        
        plt.figure(figsize=(10, 6))
        plt.plot(test_df["Date"], test_df["Views"], label="Actual")
        plt.plot(dates, forecast, label="Forecast")
        plt.legend()
        plot_path = "static/forecast.png"
        plt.savefig(plot_path)
        return {"plot_path": "static/forecast.png"}
    
    elif model_name == "arma":
        forecast = model.forecast(steps=days)
        dates = pd.date_range(start=test_df["Date"].iloc[0], periods=days)
        
        plt.figure(figsize=(10, 6))
        plt.plot(test_df["Date"], test_df["Views"], label="Actual")
        plt.plot(dates, forecast, label="Forecast")
        plt.legend()
        plot_path = "static/forecast.png"
        plt.savefig(plot_path)
        return {"plot_path": "static/forecast.png"}
    
    elif model_name == "auto_arima":
        forecast = model.predict(n_periods=days)
        dates = pd.date_range(start=test_df["Date"].iloc[0], periods=days)
        
        plt.figure(figsize=(10, 6))
        plt.plot(test_df["Date"], test_df["Views"], label="Actual")
        plt.plot(dates, forecast, label="Forecast")
        plt.legend()
        plot_path = "static/forecast.png"
        plt.savefig(plot_path)
        return {"plot_path": "static/forecast.png"}
    
    elif model_name in ["holt_add_seasonal", "holt_add", "simple_exp_smoothing"]:
        forecast = model.forecast(steps=days)
        dates = pd.date_range(start=test_df["Date"].iloc[0], periods=days)
        
        plt.figure(figsize=(10, 6))
        plt.plot(test_df["Date"], test_df["Views"], label="Actual")
        plt.plot(dates, forecast, label="Forecast")
        plt.legend()
        plot_path = "static/forecast.png"
        plt.savefig(plot_path)
        return {"plot_path": "static/forecast.png"}
    
    elif model_name in ["cnn", "cnn_60"]:
        # Dummy prediction for CNN
        forecast = [0] * days
        dates = pd.date_range(start=test_df["Date"].iloc[0], periods=days)
        
        plt.figure(figsize=(10, 6))
        plt.plot(test_df["Date"], test_df["Views"], label="Actual")
        plt.plot(dates, forecast, label="Forecast")
        plt.legend()
        plot_path = "static/forecast.png"
        plt.savefig(plot_path)
        return {"plot_path": "static/forecast.png"}
