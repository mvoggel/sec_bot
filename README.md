/13f_bot_project
├── extraction
│   ├── data_collection.py       # Orchestrates form-based extraction
│   ├── extract_13F.py           # Parses 13F-HR forms
│   ├── extract_10Q.py           # Parses 10-Q forms
│   ├── extract_DEF14A.py        # Parses DEF 14A forms
│   ├── extract_form4.py         # Parses Form 4 filings
│   ├── parse_extract.py         # Shared XML/HTML parsing functions
├── main
│   ├── main.py                  # Entry point for the full pipeline
│   ├── config.py                # General configuration, paths, and settings(e.g., API details)
├── analysis
│   ├── model_random_forest.py   # Random Forest model for predictions
│   ├── model_neural_network.py  # Neural network model
│   └── data_preprocessing.py    # Data preprocessing and feature engineering
└── execution
    ├── rebalance.py             # Executes rebalancing decisions
    └── order_execution.py       # Order execution logic (e.g., Alpaca API calls)
