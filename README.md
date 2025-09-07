# Forecasting FastAPI Application

This is a FastAPI application that provides a web interface for forecasting using various machine learning models. It includes user authentication, model selection, and visualization of forecast results.

## Features

*   **User Authentication:** Secure user registration and login using OAuth2.
*   **Multiple Forecasting Models:** Supports ARIMA, ARMA, Auto ARIMA, Holt Additive Seasonal, Holt Additive, Simple Exponential Smoothing, and CNN models.
*   **Interactive Web Interface:** A simple HTML/CSS/JavaScript frontend for interacting with the forecasting API.
*   **Forecast Visualization:** Generates plots comparing actual data with model forecasts.
*   **Database Integration:** Uses SQLite for user management.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dssingh08/web-traffic-time-series-forecasting.git
    cd web-traffic-time-series-forecasting

    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    ./venv/Scripts/activate  # On Windows
    source venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```

3.  **Run the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be accessible at `http://127.0.0.1:8000`.

## Usage

1.  **Access the Frontend:** Open your web browser and navigate to `http://127.0.0.1:8000`. You will be redirected to the login page.

2.  **Register:** If you don't have an account, click on "Register here" to create a new user.

3.  **Login:** Use your registered username and password to log in. You will be redirected to the prediction page.

4.  **Make a Prediction:**
    *   Select a forecasting model from the dropdown menu.
    *   Enter the number of days for the forecast horizon.
    *   Click the "Predict" button.

5.  **View Results:** The application will display a plot comparing the actual data from `test.csv` with the model's forecast. The plot will be saved as `static/forecast.png`.
































