print("🔥 main.py çalışıyor!")

from extract import extract_selected_tables
from transform import (
    monthly_sales_summary,
    customer_lifetime_value,
    top_products_online,
    top_products_in_stores,
    top_products_all_channels,
    product_seasonality,
    store_revenue_summary
)
from load import load_to_csv, load_to_excel, load_to_sqlite

dfs = extract_selected_tables()

if not dfs:
    print("[!] Veri çekilemedi.")
    exit()

transformed_dfs = {
    "MonthlySalesSummary": monthly_sales_summary(dfs),
    "CustomerLifetimeValue": customer_lifetime_value(dfs["DimCustomer"], dfs["FactOnlineSales"]),
    "TopProductsOnline": top_products_online(dfs),
    "TopProductsInStores": top_products_in_stores(dfs),
    "TopProductsAllChannels": top_products_all_channels(
        dfs["FactSales"], dfs["FactOnlineSales"], dfs["DimProduct"]
    ),
    "StoreRevenueSummary": store_revenue_summary(dfs),
    "ProductSeasonality_214": product_seasonality(dfs, product_id=214)
}

load_to_csv(transformed_dfs, csv_path="../output/csv")
load_to_excel(transformed_dfs, excel_path="../output/excel/etl_results.xlsx")
load_to_sqlite(transformed_dfs, sql_path="../output/sqlite/etl_results.sqlite")

print("[✓] ETL süreci tamamlandı.")
