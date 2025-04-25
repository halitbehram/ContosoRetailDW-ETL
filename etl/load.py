import os
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def load_to_csv(dfs: dict, csv_path="data/csvout"):
    os.makedirs(csv_path, exist_ok=True)
    for name, df in dfs.items():
        filename = os.path.join(csv_path, f"{name}.csv")
        df.to_csv(filename, index=False)
        print(f"[✓] CSV kaydedildi: {filename}")

def load_to_excel(dfs: dict, excel_path="data/excelout/cleaned_data.xlsx"):
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        for name, df in dfs.items():
            df.to_excel(writer, sheet_name=name, index=False)
            print(f"[✓] Excel'de '{name}' sayfası oluşturuldu → {excel_path}")
"""
def load_to_sql_server(dfs: dict, server, database, driver="ODBC Driver 17 for SQL Server", if_exists="replace"):
    try:
        connection_string = (
            f"mssql+pyodbc://@{server}/{database}"
            "?trusted_connection=yes"
            f"&driver={driver}"
        )
        engine = create_engine(connection_string)

        for name, df in dfs.items():
            df.to_sql(name, engine, if_exists=if_exists, index=False)
            print(f"[✓] SQL Server'a '{name}' tablosu kaydedildi.")
    except SQLAlchemyError as e:
        print(f"[!] SQL Server bağlantı hatası: {e}")
    except Exception as e:
        print(f"[!] Genel hata: {e}")
"""
def load_to_sqlite(dfs: dict, sql_path="data/sqlout/cleaned_data.sqlite"):
    os.makedirs(os.path.dirname(sql_path), exist_ok=True)
    conn = sqlite3.connect(sql_path)
    for name, df in dfs.items():
        df.to_sql(name, conn, if_exists="replace", index=False)
        print(f"[✓] SQLite: '{name}' tablosu veritabanına kaydedildi → {sql_path}")
    conn.close()

