import pandas as pd
import glob

# Load all CSV files into dataframes
csv_files = glob.glob("*.csv")
dataframes = {file[:-4]: pd.read_csv(file) for file in csv_files}

# Access dataframes by name
DimCustomer = dataframes['DimCustomer']
DimModel = dataframes['DimModel']
DimOffer = dataframes['DimOffer']
DimShop = dataframes['DimShop']
DimStock = dataframes['DimStock']
FactSales = dataframes['FactSales']

# Merge FactSales with all dimension tables
final_df = FactSales.merge(DimCustomer, on='customer_id') \
                   .merge(DimModel, on='model_id') \
                   .merge(DimOffer, on='offer_id') \
                   .merge(DimShop, on='shop_id') \
                   .merge(DimStock, on='stock_id')