# MobileShoppee Data Curation & Analytics

**Author:** Tanashree  
**Date:** 2025-11-15

## Project Overview
This project ingests and curates mobile shop datasets (Customers, MobileModels, Shops, Sales, Offers, Stocks),
performs data cleaning, profiling, integration (star schema), feature engineering, and predictive modeling (regression).

## Folder structure (generated)
- `documentation/` : data dictionary, transformation log, profiling summaries (CSV/MD/XLSX)
- `notebooks/` : Jupyter notebooks for ETL, EDA, modeling
- `data/` : raw and cleaned CSV files
- `models/` : trained model artifacts (if any)
- `reports/` : final report, figures, slides

## Workflow
1. Load raw CSVs from `data/` into pandas DataFrames.
2. Run data profiling and generate `documentation/profiling_summary.*`.
3. Clean and standardize columns (snake_case), fix misspellings, handle missing values.
4. Log every transformation with `documentation/transformation_log.csv`.
5. Join tables into star schema:
   - Fact: `FactSales` (sales + revenue)
   - Dims: `DimCustomer`, `DimModel`, `DimShop`, `DimOffer`, `DimStock`
6. Feature engineering: revenue, discount_value, stock_turnover, price buckets, loyalty tiers.
7. Train models (XGBoost recommended) to predict final_price or revenue.
8. Save models and evaluation metrics in `models/` and `reports/`.

## Important files produced
- `documentation/data_dictionary.csv` and `.xlsx`
- `documentation/transformation_log.csv`
- `documentation/profiling_summary.csv` and `.md`
- `customers_cleaned.csv`, `sales_cleaned.csv`, etc.

## How to re-run
1. Place raw CSVs in `data/` and update the `folder_path` variables in the notebooks.
2. Run the notebook cells in order:
   - 00_load_data.ipynb
   - 01_profile_and_backup.ipynb
   - 02_cleaning_and_transforms.ipynb
   - 03_integration_star_schema.ipynb
   - 04_modeling.ipynb
3. Use `TransformationLogger` to record every change.

## Notes
- Great Expectations is not used due to environment constraints; all validations implemented using pandas checks.
- Use `documentation/profiling_summary.md` for a quick review before modeling.

