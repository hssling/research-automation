# Time Series Analysis and Forecasting Pipeline

A comprehensive automated pipeline that combines statistical forecasting (ARIMA/Prophet) and machine learning (LSTM) for time series analysis. Just plug in your dataset and get automatic analysis + predictions.

## Features

- **Prophet Forecasting**: Bayesian time series model with trend, seasonality, and holiday effects
- **ARIMA Forecasting**: Classical statistical time series methodology
- **LSTM Neural Network**: Deep learning approach for complex pattern recognition
- **Automated Visualization**: Generates forecast plots and model comparison
- **Performance Metrics**: MSE, RMSE, MAE comparison across models
- **Publication-Ready Reports**: Automatic Word (.docx) and PDF reports with all plots and interpretations
- **Excel Export**: Detailed forecasts with confidence intervals and model comparison table
- **Individual Model CSVs**: Separate CSV exports for each model's predictions (Prophet/ARIMA/LSTM)
- **Interactive Dashboard**: Web-based visualization dashboard with model comparisons and export options

## Project Structure

```
time_series_pipeline/
│── data/                  # Raw CSV/Excel/JSON time series data
│   └── timeseries.csv
│
│── output/                # Plots, reports, forecasts
│   ├── prophet_forecast.csv
│   ├── arima_forecast.csv
│   ├── lstm_forecast.csv
│   └── (other outputs)
│
│── pipeline.py            # Main automation script
│── dashboard.py           # Interactive web dashboard
│── requirements.txt       # Dependencies
│── README.md              # Usage instructions (this file)
```

## Quick Start

### 1. Setup Environment

```bash
# Navigate to the pipeline directory
cd time_series_pipeline

# Install dependencies
pip install -r requirements.txt
```

### 2. Prepare Your Data

Place your time series data in `data/timeseries.csv` with columns:
- `ds` → dates (YYYY-MM-DD format)
- `y` → values to predict

Example:
```csv
ds,y
2024-01-01,100.5
2024-01-02,105.2
2024-01-03,98.7
...
```

### 3. Run the Pipeline

```bash
python pipeline.py
```

## Output

The pipeline generates comprehensive outputs for complete analysis:

### Visualization Outputs
- `output/prophet_forecast.png` - Prophet forecast visualization
- `output/prophet_components.png` - Trend/seasonality components
- `output/arima_forecast.png` - ARIMA forecast visualization
- `output/lstm_forecast.png` - LSTM forecast visualization

### Publication-Ready Reports
- `output/report.docx` - Word document with all plots, metrics, and interpretation
- `output/report.pdf` - PDF summary report

### Data Export Formats
- `output/forecasts.xlsx` - Excel workbook with:
  - Forecasts sheet: Future predictions from Prophet
  - Model_Comparison sheet: Performance metrics (MSE, RMSE, MAE, AIC, BIC)

### Individual Model CSVs (Dashboard-Ready)
- `output/prophet_forecast.csv` - Prophet future predictions with confidence intervals
- `output/arima_forecast.csv` - ARIMA forecast values for test period
- `output/lstm_forecast.csv` - LSTM predictions for test period
- `output/future_forecasts.csv` - Clean CSV with future Prophet forecasts only

Console output includes model performance metrics for comparison.

## Interactive Dashboard

Launch a **fully self-contained forecasting web application**:

### Launch Dashboard
```bash
cd time_series_pipeline
streamlit run dashboard.py
```

### Dashboard Features

**🚀 Self-Contained Forecasting Engine:**
- **📥 File Upload**: Upload any CSV with `ds` (date) and `y` (value) columns
- **⚡ Instant Forecasting**: Automatically runs Prophet, ARIMA, and LSTM models
- **🔄 No External Dependencies**: Doesn't require running pipeline.py first

**📊 Advanced Visualization:**
- **Interactive Charts**: Plotly-powered zoom, pan, hover details
- **Multi-Model Comparison**: View all three forecasts simultaneously
- **Confidence Intervals**: Prophet uncertainty bands
- **Real-Time Performance**: Loading indicators during model training

**📈 Professional Analytics:**
- **Model Metrics Display**: MSE, AIC, BIC comparison table
- **Forecast Quality Assessment**: Statistical evaluation of predictions
- **Responsive Design**: Works on all devices and screen sizes

**🎯 Usage Workflow:**

1. **Upload CSV** → Browse and select your time series data
2. **Auto Processing** → Dashboard trains all three models instantly
3. **Explore Results** → Interactive visualizations with forecasts
4. **Compare Models** → Side-by-side performance metrics
5. **Export Insights** → Ready for presentation or further analysis

**💡 Key Advantages:**
- **Zero Setup Time**: Upload → Get Forecasts instantly
- **No Command Line**: Pure web interface
- **Publication Ready**: Professional visualization quality
- **Educational**: Perfect for teaching time series concepts

## Model Details

### Prophet
- Handles trend, seasonality, holidays
- Robust to missing data and outliers
- Forecasts 90 days into the future

### ARIMA
- Classical statistical approach
- Uses last 30 points for testing
- Order: (5,1,0) - 5 autoregressive terms, 1 differencing, 0 moving average

### LSTM
- Deep learning neural network
- 5-day look-back window
- 50 LSTM units, trained for 20 epochs
- Uses 80/20 train/test split

## Customization

### Modify Forecast Horizonts
```python
# In pipeline.py
future = prophet_model.make_future_dataframe(periods=30)  # Change forecast period
```

### Adjust LSTM Parameters
```python
# In pipeline.py
look_back = 10  # Increase look-back window
model = Sequential([LSTM(100, ...), ...])  # More units
model.fit(..., epochs=50, ...)  # More training
```

### Tune ARIMA Order
```python
# In pipeline.py
arima_model = ARIMA(train, order=(2,1,2))  # Adjust p,d,q parameters
```

## Requirements

- Python 3.7+
- pandas, numpy, matplotlib, scikit-learn
- statsmodels, prophet, tensorflow
- reportlab, python-docx, openpyxl

All dependencies are listed in `requirements.txt` for easy installation.

## Sample Data

The pipeline includes sample data (`data/timeseries.csv`) with 100+ days of synthetic time series values for immediate testing and demonstration.

## Next Steps

1. Replace the sample data with your own dataset
2. Adjust model parameters based on your data characteristics
3. Integrate the pipeline into your research workflow
4. Compare model performances and select the best approach for your use case

## Applications

- Financial forecasting
- Sales prediction
- Weather forecasting
- Health metrics analysis
- Resource planning
- Research data analysis
