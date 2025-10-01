from etl.extract.customers_extract import Extract_customer
from etl.extract.item_extract import Extract_items
from etl.extract.collaborators_extract import Extract_collaborator
from etl.extract.sales_extract import Extract_sale
from etl.transform.customers_transform import Transform_customer
from etl.transform.item_transform import Transform_item
from etl.load.customers_load import Load_customer
from etl.transform.collaborators_transform import Transform_collaborator
from etl.transform.sales_transform import Transform_sale
from etl.load.item_load import Load_item
from etl.load.collaborators_load import Load_collaborator
from etl.load.sales_load import Load_sale
from datetime import datetime
from etl.utils.populate_DL import populate_dl

def etl_customers(process_date):
    resp_extract = Extract_customer(process_date)

    if not resp_extract['error']:
        resp_transform = Transform_customer(resp_extract['customer_data'])

        if not resp_transform['error']:
            Load_customer(resp_transform['customer_data'])

def etl_items(process_date):
    resp_extract = Extract_items(process_date)

    if not resp_extract['error']:
        resp_transform = Transform_item(resp_extract['servicio_data'], resp_extract['producto_data'])
        
        if not resp_transform['error']:
            Load_item(resp_transform['item_data'])

def etl_collaboratos(process_date):
    resp_extract = Extract_collaborator(process_date)
    if not resp_extract['error']:
        resp_transform = Transform_collaborator(resp_extract['collaborator_data'])
        
        if not resp_transform['error']:
            Load_collaborator(resp_transform['collaborator_data'])

def etl_sale(process_date):
    resp_extract = Extract_sale(process_date)
    if not resp_extract['error']:
        resp_transform = Transform_sale(resp_extract['sale_data'])
        
        resp_transform['sale_data'].to_excel("./sales.xlsx", index=False)
        if not resp_transform['error']:
            Load_sale(resp_transform['sale_data'])

if __name__ == "__main__":
    process_date = datetime.now().strftime("%d%m%Y")

    populate_dl(process_date)

    etl_customers(process_date)
    etl_items(process_date)
    etl_collaboratos(process_date)
    etl_sale(process_date)
    
