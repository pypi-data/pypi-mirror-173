from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.data.tables import TableClient
import os
import datetime
import json
import pandas as pd
import requests
import io
from azure.core.exceptions import ResourceExistsError

ACCOUNT_KEY = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
TEAMS_FUNCTIONS_KEY = os.getenv("TEAMS_FUNCTIONS_KEY")

tickers_table_client = TableClient.from_connection_string(CONNECTION_STRING, "NPDTickers")
filings_table_client = TableClient.from_connection_string(CONNECTION_STRING, "SecDocs")
suggestions_table_client = TableClient.from_connection_string(CONNECTION_STRING, "Suggestions")
fund_table_client = TableClient.from_connection_string(CONNECTION_STRING, "FundMetadata")

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

TICKER_USE_CASES = ["ww_prospect","ww_client","cat_corrs","cat_corrs_retailer", "sec_filings"]

def get_blob_url(container, blob_name, link_minutes=1):

    url = "https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}".format(account_name="stdevfinservices", container_name=container, blob_name=blob_name)
    sas_token = generate_blob_sas(
        account_name="stdevfinservices",
        account_key=ACCOUNT_KEY,
        container_name=container,
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(minutes=link_minutes)
    )

    url_with_sas = f"{url}?{sas_token}"
    return url_with_sas

def blob_exists(container, file_name):

    container_client = ContainerClient.from_connection_string(CONNECTION_STRING, container)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        if blob.name == file_name:
            return True
    return False

def list_blobs(container, path):

    if not path == "" and not path.endswith('/'):
        path += "/"

    container_client = ContainerClient.from_connection_string(CONNECTION_STRING, container)
    blob_iter = container_client.list_blobs(name_starts_with=path)
    return [blob.name for blob in blob_iter]

def get_json(container, file_name):

    container_client = blob_service_client.get_container_client(container)
    blob_client = container_client.get_blob_client(file_name)
    streamdownloader = blob_client.download_blob()
    fileJson = json.loads(streamdownloader.readall())
    return fileJson

def get_npd_tickers(subset):

    #available subsets: all, sec_filings, category_correlations, whale_wisdom_prospect, whale_wisdom_client
    if subset == "all":
        results = list(tickers_table_client.query_entities("ww_prospect eq true".format(subset=subset))) + list(tickers_table_client.query_entities("ww_prospect eq false".format(subset=subset)))
    else:
        results = list(tickers_table_client.query_entities("{subset} eq true".format(subset=subset)))
    return [r for r in results if "RowKey" in r.keys()]

def get_npd_tickers_df(subset):

    results = get_npd_tickers(subset)
    tickers = [x["PartitionKey"] for x in results]
    names = [x["RowKey"] for x in results]
    return pd.DataFrame(data={"stock_name":names, "stock_ticker":tickers})


def update_npd_ticker(ticker, name, project, use):

    if name != "":
        entity = tickers_table_client.get_entity(ticker, name)
    else:
        results = tickers_table_client.query_entities("PartitionKey eq '{ticker}'".format(ticker=ticker))
        results = list(results)
        if len(results) == 1:
            entity = results[0]
    entity[project] = use
    tickers_table_client.update_entity(entity)
    if project in ["ww_prospect","ww_client"]:
        pass
        #reset_ww_reports()
    elif project == "cat_corrs":
        pass
        #reset_cat_corr_reports()

def new_npd_ticker(ticker, name, uses):

    entity = {"PartitionKey":ticker, "RowKey":name}
    for use_case in TICKER_USE_CASES:
        entity[use_case] = use_case in uses
    try:
        tickers_table_client.create_entity(entity)
        return ""
    except ResourceExistsError as e:
        return "Ticker ({ticker}) already covered".format(ticker=ticker)


def delete_blob(container, file_path):

    container_client = blob_service_client.get_container_client(container)
    container_client.delete_blob(file_path)

def clear_blob_dir(container, dir_path):

    container_client = blob_service_client.get_container_client(container)
    all_blobs = list_blobs(container, dir_path)
    container_client.delete_blobs(*all_blobs)

def upload_blob_file(container, file_path, local_file_path, remove=False):

    blob_client = blob_service_client.get_blob_client(container, file_path)
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)
    if remove:
        os.remove(local_file_path)

def upload_dataframe(df, container, filename):

    stream = bytes(df.to_csv(lineterminator='\r\n', index=False), encoding='utf-8')
    container_client = blob_service_client.get_container_client(container)
    container_client.upload_blob(name=filename, data=stream, overwrite=True)

def get_dataframe_file(container, filename, dtype={}):

    url = get_blob_url(container, filename)
    return pd.read_csv(url, dtype=dtype)

def generate_funds_file():

    all_funds = fund_table_client.query_entities(query_filter="PartitionKey eq 'FUND'")
    all_funds = pd.DataFrame(list(all_funds))
    all_funds = all_funds.drop(columns=["PartitionKey"])
    all_funds = all_funds.rename(columns={"RowKey":"cik"})
    upload_dataframe(all_funds, "docoh", "all_funds.csv")
