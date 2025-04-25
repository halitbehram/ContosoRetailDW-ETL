import pandas as pd

def monthly_sales_summary(dataframes):
    
    Factsales  = dataframes["Factsales"].copy()
    Factsales["DateKey"] = pd.to_datetime(Factsales["DateKey"])
    Factsales["year_month"] = Factsales["DateKey"].dt.to_period("M")


    summary = Factsales.groupby("year_month").agg(
        monthly_revenue=('SalesAmount', 'sum'),
        total_quantity=('SalesQuantity', 'sum')
    )
    
    return summary

def customer_lifetime_value(dim_customer, fact_online_sales):
    
    df = fact_online_sales.merge(dim_customer   , on = "CustomerKey")
    
    clv = df.gorupby(["CustomerKey", "FirstName", "LastName"]).agg(
        
        total_spent = ('SalesAmount', 'sum'),
        total_quantity = ('SalesQuantity', 'sum'),
        total_order_number = ('OnlineSalesKey', 'count')
    
    ).reset_index()

    clv['CLV_Segment'] = pd.qcut(clv['total_spent'], q=4, labels=["Low", "Medium", "High", "Very High"])
    
    return clv.sort_values('total_spent', ascending=False)

#En Çok Satılan Ürünler (adet + gelir bazlı) online magazada

def top_products_online(dfs, n = 10):

    fact_online_sales = dfs["FactOnlineSales"]
    dim_prodcut = dfs["DimProduct"]


    df = fact_online_sales.merge(dim_prodcut, on = "ProductKey")
    result = df.groupby(["ProductKey", "ProductName"]).agg(

        total_quantity = ("SalesQuantity", "sum"),
        total_amount = ("SalesAmount", "sum")
    
    ).reset_index().sort_values('total_amount', ascending=False).head(n)

    return result

#En Çok Satılan Ürünler (adet + gelir bazlı) fiziksel magazada

def top_products_in_stores(dfs, n = 10):

    fact_sales = dfs["FactSales"]
    dim_prodcut = dfs["DimProduct"]

    df = fact_sales.merge(dim_prodcut, on = "ProductKey")
    result = df.groupby(["ProductKey", "ProductName"]).agg(

        total_quantity = ("SalesQuantity", "sum"),
        total_amount = ("SalesAmount", "sum")
    
    ).reset_index().sort_values('total_amount', ascending=False).head(n)

    return result

#En Çok Satılan Ürünler (adet + gelir bazlı) fiziksel + online magazada


def top_products_all_channels(fact_sales, fact_online_sales, dim_product, n=10):
    combined = pd.concat([
        fact_sales[['ProductKey', 'SalesQuantity', 'SalesAmount']],
        fact_online_sales[['ProductKey', 'SalesQuantity', 'SalesAmount']]
    ], ignore_index=True)

    df = combined.merge(dim_product, on='ProductKey')
    
    result = df.groupby(['ProductKey', 'ProductName']).agg(
        
        total_quantity=('SalesQuantity', 'sum'),
        total_revenue=('SalesAmount', 'sum')
        
        ).reset_index().sort_values('total_revenue', ascending=False).head(n)
    
    return result

#Belirli Ürünün fiziksel mağazada Aylara Göre Satış Trendleri

def product_seasonality(dfs, product_id):

    fact_sales = dfs["FactSales"]
    dim_product = dfs["DimProduct"]
    dim_date = dfs["DimDate"]

    df = fact_sales.merge(dim_product, on = "ProductKey")
    df = df.merge(dim_date, on = "DateKey")

    product_df = df[df["ProductKey"] == product_id]

    result = product_df.groupby(["CalendarYear", "CalendarMonthLabel"]).agg(

        total_spent = ('SalesAmount', 'sum'),
        total_quantity = ('SalesQuantity', 'sum'),
        total_order_number = ('SalesKey', 'count')
    
    ).reset_index().sort_values(["CalendarYear", "CalendarMonthLabel"])

    return result

#Fiziksel Mağaza Bazlı Satış Özeti

def store_revenue_summary(dfs):

    fact_sales = dfs["FactSales"]
    dim_store = dfs["DimStore"]

    df = fact_sales.merge(dim_store, on = 'StoreKey')

    result = df.groupby("StoreName").agg(

        total_revenue=('SalesAmount', 'sum'),
        total_quantity=('SalesQuantity', 'sum'),
        total_order_number = ('SalesKey', 'count')
    
    ).reset_index().sort_values('total_revenue', ascending=False)

    return result



# Bu fonksiyon, online satış verilerinden tekrar eden ve ilk kez alışveriş yapan müşterilerin oranını hesaplar.
# 'First-Time' ve 'Repeat' müşteri oranlarını yüzdelik olarak döndürür.
def repeat_customer_rate(dfs):

    # Gerekli tabloları al
    dim_customer = dfs["DimCustomer"]
    fact_online_sales = dfs["FactOnlineSales"]

    # Müşteri bilgilerini satış verileriyle birleştir
    df = fact_online_sales.merge(dim_customer, on="CustomerKey")

    # Her müşteri için toplam sipariş sayısı, adı ve soyadını hesapla
    order_counts = df.groupby("CustomerKey").agg(
        customer_total_order_counts=("SalesOrderNumber", "nunique"),  # Kaç farklı sipariş numarası?
        customer_first_name=("FirstName", "first"),                   # İlk adı
        customer_last_name=("LastName", "first")                      # Soyadı
    ).reset_index()

    # Sipariş sayısına göre müşteri türünü belirle
    order_counts["customer_type"] = order_counts["customer_total_order_counts"].apply(
        lambda x: "First-Time" if x == 1 else "Repeat"
    )

    # Her müşteri türü için toplam müşteri sayısını hesapla
    result = order_counts.groupby("customer_type").agg(
        type_count=("customer_type", "count")
    ).reset_index()

    # Yüzde hesabı yap
    total = result["type_count"].sum()
    result["type_percentage"] = (result["type_count"] / total * 100).round(2)

    return result  # First-Time vs Repeat oranları



#FactOnlineSales'ten sadece repeat müşterileri almak
def get_repeat_customers(dfs):

    fact_online_sales = dfs["FactOnlineSales"]

    df = fact_online_sales.groupby("CustomerKey").agg(

        order_number = ("SalesOrderNumber", "ununiqe")
    
    ).reset_index()

    df_greater1 = df[df["order_number"] > 1]
    df_greater1_cust = df_greater1["CustomerKey"]

    result = fact_online_sales[fact_online_sales["CustomerKey"].isin(df_greater1_cust)]

    return result

if __name__ == "__main__":
    print("transform.py test ediliyor...")










    














