# Trade Oracle Project 🔮

**Updated Model Information (12/5/2023):**
The main branch now incorporates a Random Forest classifier achieving an 80.49% accuracy and 58.33% recall. More updates coming :)

Oracle is a machine learning model tailored to predict the profitability of trades executed by BlackBoxStocks member Maria. Utilizing historical order entry and exit data over the past three years provided by Maria, this model aims to forecast the success of her trades.

## Dataset Sample

The dataset comprises various fields:

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

Initially, the model relied on historical 90-day time series price data for each order ticker. However, the accuracy fell short, leading to a shift in strategy towards generating features based on indicators and patterns. The current model achieves 76.62% accuracy by leveraging 181 days of historical price data combined with order details, with a mean cross-validation accuracy of 74%.

## In-progress Implementations

As of 12/5/2023, ongoing enhancements include:

- Incorporating price differences related to long-term/short-term resistances/supports using Fibonacci
- Analyzing price variance with moving averages
- Integrating sentiment analysis scores on the stock
- Including various index prices for comprehensive analysis

## Approach to Trading

Maria's strategy revolves around options flow analysis, leveraging her 10+ years of trading experience, including her tenure at TD Ameritrade. Her approach involves analyzing options flow, representing orders of options traded at varying strike prices and expiration dates. By following the lead of large institutions trading these options, Maria aims to make informed decisions based on their position entries.

Oracle's dataset amalgamates 2 years of practical trading experience in technical analysis and options flow as a BlackBoxStocks member, coupled with academic insights gained through machine learning studies at university. This convergence aims to apply machine learning techniques to enhance trading decisions.

## Statistics

![Profitability Ratio and Cumulative Profit (80% stop loss) vs. Time](images/Figure_1.png)

## How to Use

To replicate the model:

1. **Dataset**: Ensure you possess historical order details and price data.
2. **Python Environment**: Set up a Python environment with essential libraries like Pandas, XGBoost, Matplotlib, and Seaborn.
3. **Run the Code**: Utilize the provided code snippet to load the dataset, preprocess features, and train the Random Forest classifier.

## Contributions and Future Work

Contributions, suggestions, and enhancements to improve model accuracy and efficiency are welcomed. Future iterations may involve:

- Refining feature engineering techniques
- Incorporating additional technical indicators
- Optimizing hyperparameters for superior performance

Feel free to reach out for collaboration or improvements to Oracle!
