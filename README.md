# Oracle Project

Oracle is a machine learning model designed to predict the profitability of trades made by BlackBoxStocks member Maria. Leveraging historical order entry and exit data from the past three years provided by Maria, this model aims to forecast the success of her trades.

## Dataset Sample

The dataset contains the following fields:

- `order_execution_datetime`
- `trader`
- `direction`
- `ticker`
- `expiration`
- `contract_details`
- `contract_price`
- `timeframe`
- `comment`
- `success`

## Project Overview

Initially, the model utilized historical 90-day time series price data for each order ticker. However, the accuracy fell short, prompting a shift to generating features based on indicators and patterns. The current accuracy stands at 76.62% using 181 days of historical price data combined with order details, with a mean cross-validation accuracy of 74%.

## In-progress Implementations

The ongoing enhancements include:

- Incorporating price differences to long-term/short-term resistances/supports using Fibonacci
- Analyzing price variance with moving averages
- Integration of sentiment analysis scores on the stock
- Inclusion of various index prices for comprehensive analysis

## Approach to Trading

The choice of this approach stems from years of experience trading with BlackBoxStocks, coupled with a newfound understanding of machine learning acquired at university. The convergence of practical trading knowledge and academic insights has inspired the application of machine learning techniques to enhance trading decisions.

## How to Use

To replicate the model:

1. **Dataset**: Ensure you possess the historical order details and price data.
2. **Python Environment**: Set up a Python environment with essential libraries like Pandas, XGBoost, Matplotlib, and Seaborn.
3. **Run the Code**: Utilize the provided code snippet to load the dataset, preprocess features, and train the XGBoost classifier.

## Contributions and Future Work

Contributions, suggestions, and enhancements to improve model accuracy and efficiency are encouraged. Future iterations may involve:

- Refining feature engineering techniques
- Incorporating additional technical indicators
- Optimizing hyperparameters for superior performance

Feel free to reach out for collaboration or improvements to Oracle!
