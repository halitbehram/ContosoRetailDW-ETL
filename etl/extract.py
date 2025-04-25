from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

def extract_selected_tables():
    server = 'DESKTOP-R41JDGP\\SQLEXPRESS'  
    database = 'ContosoRetailDW'
    driver = 'ODBC Driver 17 for SQL Server'

    try:
        connection_string = (
            f"mssql+pyodbc://@{server}/{database}"
            "?trusted_connection=yes"
            f"&driver={driver}"
        )
        engine = create_engine(connection_string)
        connection = engine.connect()
        print("✅ Veritabanına başarıyla bağlanıldı.")
    except SQLAlchemyError as e:
        print(f"[!] Bağlantı hatası: {e}")
        return {}

    tables = ['FactSales', 'DimCustomer', 'DimProduct', 'DimDate', 'FactOnlineSales', 'DimStore']
    dataframes = {}

    for table_name in tables:
        try:
            print(f"🔄 Veri çekiliyor: {table_name}")
            df = pd.read_sql(f"SELECT TOP 1000 * FROM {table_name}", engine)
            dataframes[table_name] = df
        except Exception as e:
            print(f"[!] {table_name} tablosu alınamadı: {e}")

    return dataframes


    


