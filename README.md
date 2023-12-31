
# 🔮 TradeOracle: Long Options Flow Signal Prediction + Risk Management

## Introduction
TradeOracle is an advanced machine learning model designed to predict the outcomes of long options flow signal trading strategies in collaboration with BlackBoxStocks team trader Maria Chaudhry. Leveraging her historical trade and market data provides traders with actionable insights to enhance their decision-making process.

## Features
- **Predictive Analysis**: Utilize historical trading data to predict the success of future trades.
- **Customizable Model**: Tailored features and parameters to fit specific trading strategies.
- **Automated Data Processing**: Integrated tools for efficient data handling and feature generation.

## Requirements
- Python 3.x
- Pandas, NumPy, Scikit-Learn, and other relevant Python libraries.
- Access to historical options trading data.

## Installation
1. Clone the repository: `git clone [repository_url]`

##  Setup & Usage
To use TradeOracle, follow these steps:
1. Prepare your data using `DataDownloader.py`.
2. Process the data with `DataProcessor.py`.
3. Generate features using `FeatureGen.py`.
4. Run the `TradeProcessor.py` to analyze the trades.
5. Train the model using the processed data. ⌛ 

## Components
- `DataDownloader.py`: Module for downloading trade data.
- `DataProcessor.py`: Script for processing raw trade data.
- `FeatureGen.py`: Tool for feature generation from processed data.
- `TradeProcessor.py`: Core engine for analyzing trades and generating predictions.

## Data
TradeOracle works with various types of trade data:
- `raw_trade_data.csv`: Raw trading data from BlackBoxStocks team trader Maria Chaudhry.
- `aggregated_index_data.csv`: Aggregated data from multiple indices.
- Other relevant datasets.
For more insights on Maria Chaudhry's trading strategies, visit [CheddarNews Interview](https://www.youtube.com/watch?v=FfGfNnhXVFM).

## Model Details
The machine learning model in TradeOracle uses a Random Forest Model to predict the success of trades. It will soon be tested and validated with historical data and our new dataset ⌛

## In Progress
- **MetaLabeling**: Upcoming secondary model to enhance primary model accuracy and adaptability by applying meta-labeling techniques to the prediction process.
- Merging final dataset with triple barrier features inspired from Marcos López de Prado's textbook: Advances in Financial Machine Learning 

## Expected Update: 12/30/2023 ⌛
