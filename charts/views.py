import os
import json
import zipfile
import tempfile
import requests
import numpy as np
import pandas as pd
import polars as pl

from datetime import datetime
from google.cloud import storage
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "datastore-readonly3-key.json"

# Instantiate a storage client
storage_client = storage.Client()

def candlestick_chart(request):
    return render(request, 'charts/candlestick_chart.html')

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

@login_required
@api_view(['GET'])
def get_chart_data(request, symbol='BTCUSDT', interval='1m', timestamp='', location=''):
    # Define the base URLs for the two endpoints
    base_url_com = "https://fapi.binance.com/fapi/v1/klines"
    base_url_us  = "https://data.binance.com/api/v1/klines"

    days = 4.85625
    base_d = 1440
    p = int(days*base_d)
    q = 0
    
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    I = {"1m":1, "3m":3, "5m":5, "15m":15, "30m":30, "1h":60}
    Q = I[interval]
    p2 = p//Q
    
    # Get the current time in milliseconds
    current_time = int(timestamp)

    # Calculate the time ranges
    sixteen_hours_ago       = int( current_time -  16.65 * 60 * 60 * 1000 )
    thirty_three_hours_ago  = int( current_time -  33.30 * 60 * 60 * 1000 )
    fourty_eight_hours_ago  = int( current_time -  49.95 * 60 * 60 * 1000 )
    sixty_fooour_hours_ago  = int( current_time -  66.60 * 60 * 60 * 1000 )
    eighty_hours_ago        = int( current_time -  83.25 * 60 * 60 * 1000 )
    ninety_six_hours_ago    = int( current_time -  99.90 * 60 * 60 * 1000 )
    hundred_sx_hours_ago    = int( current_time - 116.55 * 60 * 60 * 1000 )

    # Set initial base_url to fapi.binance (com)
    base_url = base_url_us

    limit = 1000
    limit2 = int(round(limit/Q, 0))

    url1 = f"{base_url}?symbol={symbol}&interval={interval}&limit={limit2}"
    url2 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={thirty_three_hours_ago}&endTime={sixteen_hours_ago}&limit={limit2}"
    url3 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={fourty_eight_hours_ago}&endTime={thirty_three_hours_ago}&limit={limit2}"
    url4 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={sixty_fooour_hours_ago}&endTime={fourty_eight_hours_ago}&limit={limit2}"
    url5 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={eighty_hours_ago}&endTime={sixty_fooour_hours_ago}&limit={limit2}"
    url6 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={ninety_six_hours_ago}&endTime={eighty_hours_ago}&limit={limit2}"
    url7 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={hundred_sx_hours_ago}&endTime={ninety_six_hours_ago}&limit={limit2}"
    # url1 = f"https://api.gemini.com/v2/candles/{symbol.lower().replace('usdt', 'usd')}/{interval}"
    
    # Make the first API calls (last 36 hours)
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    response3 = requests.get(url3)
    response4 = requests.get(url4)
    response5 = requests.get(url5)
    response6 = requests.get(url6)
    response7 = requests.get(url7)
    
    # If the first attempt fails, try the second endpoint (data.binance)
    if response1.status_code != 200 or response2.status_code != 200:
        base_url = base_url_com
    
        # Calculate the time ranges
        twenty_four_hours_ago   = current_time - 24 * 60 * 60 * 1000
        fourty_eight_hours_ago  = current_time - 48 * 60 * 60 * 1000
        seventy_two_hours_ago   = current_time - 72 * 60 * 60 * 1000
        eighty_hours_ago        = current_time - 80 * 60 * 60 * 1000

        limit = 1500
        limit2 = limit//Q
        
        # Construct URLs for the first attempt
        url1 = f"{base_url}?symbol={symbol}&interval={interval}&limit={limit2}"
        url2 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={fourty_eight_hours_ago}&endTime={twenty_four_hours_ago}&limit={limit2}"
        url3 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={seventy_two_hours_ago}&endTime={fourty_eight_hours_ago}&limit={limit2}"
        url4 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={eighty_hours_ago}&endTime={seventy_two_hours_ago}&limit={limit2}"
        
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        response3 = requests.get(url3)
        response4 = requests.get(url4)
        q = 1
    
    # Check if the responses are successful
    if response1.status_code == 200 and response2.status_code == 200:
        try:
            data1 = response1.json() ### last values
            data2 = response2.json() ### non last values
            if q==1:
                data3 = response3.json() ### non last values
                data4 = response4.json() ### non last values
                combined_data = data4 + data3 + data2 + data1
            else:
                data3 = response3.json() ### non last values
                data4 = response4.json() ### non last values
                data5 = response5.json() ### non last values
                data6 = response6.json() ### non last values
                data7 = response7.json() ### non last values
                combined_data = data7 + data6 + data5 + data4 + data3 + data2 + data1
            
            combined_data2 = [i[:5] for i in combined_data[-p2:]]
            return JsonResponse(combined_data2, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

def get_chart_data2(request, symbol='BTCUSDT', interval='1m', timestamp='', location=''):
    
    # Define the base URLs for the two endpoints
    base_url_com = "https://fapi.binance.com/fapi/v1/klines"
    base_url_us  = "https://data.binance.com/api/v1/klines"

    days = 4.85625
    base_d = 1440
    p = int(days*base_d)
    q = 0
    
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    I = {"1m":1, "3m":3, "5m":5, "15m":15, "30m":30, "1h":60}
    Q = I[interval]
    p2 = p//Q
    
    # Get the current time in milliseconds
    current_time = int(timestamp)

    # Calculate the time ranges
    sixteen_hours_ago       = int( current_time -  16.65 * 60 * 60 * 1000 )
    thirty_three_hours_ago  = int( current_time -  33.30 * 60 * 60 * 1000 )
    fourty_eight_hours_ago  = int( current_time -  49.95 * 60 * 60 * 1000 )
    sixty_fooour_hours_ago  = int( current_time -  66.60 * 60 * 60 * 1000 )
    eighty_hours_ago        = int( current_time -  83.25 * 60 * 60 * 1000 )
    ninety_six_hours_ago    = int( current_time -  99.90 * 60 * 60 * 1000 )
    hundred_sx_hours_ago    = int( current_time - 116.55 * 60 * 60 * 1000 )

    # Set initial base_url to fapi.binance (com)
    base_url = base_url_us

    limit = 1000
    limit2 = int(round(limit/Q, 0))

    url1 = f"{base_url}?symbol={symbol}&interval={interval}&limit={limit2}"
    url2 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={thirty_three_hours_ago}&endTime={sixteen_hours_ago}&limit={limit2}"
    url3 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={fourty_eight_hours_ago}&endTime={thirty_three_hours_ago}&limit={limit2}"
    url4 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={sixty_fooour_hours_ago}&endTime={fourty_eight_hours_ago}&limit={limit2}"
    url5 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={eighty_hours_ago}&endTime={sixty_fooour_hours_ago}&limit={limit2}"
    url6 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={ninety_six_hours_ago}&endTime={eighty_hours_ago}&limit={limit2}"
    url7 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={hundred_sx_hours_ago}&endTime={ninety_six_hours_ago}&limit={limit2}"
    # url1 = f"https://api.gemini.com/v2/candles/{symbol.lower().replace('usdt', 'usd')}/{interval}"
    
    # Make the first API calls (last 36 hours)
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    response3 = requests.get(url3)
    response4 = requests.get(url4)
    response5 = requests.get(url5)
    response6 = requests.get(url6)
    response7 = requests.get(url7)
    
    # If the first attempt fails, try the second endpoint (data.binance)
    if response1.status_code != 200 or response2.status_code != 200:
        base_url = base_url_com
    
        # Calculate the time ranges
        twenty_four_hours_ago   = current_time - 24 * 60 * 60 * 1000
        fourty_eight_hours_ago  = current_time - 48 * 60 * 60 * 1000
        seventy_two_hours_ago   = current_time - 72 * 60 * 60 * 1000
        eighty_hours_ago        = current_time - 80 * 60 * 60 * 1000
        
        limit = 1500
        limit2 = limit//Q
        
        # Construct URLs for the first attempt
        url1 = f"{base_url}?symbol={symbol}&interval={interval}&limit={limit2}"
        url2 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={fourty_eight_hours_ago}&endTime={twenty_four_hours_ago}&limit={limit2}"
        url3 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={seventy_two_hours_ago}&endTime={fourty_eight_hours_ago}&limit={limit2}"
        url4 = f"{base_url}?symbol={symbol}&interval={interval}&startTime={eighty_hours_ago}&endTime={seventy_two_hours_ago}&limit={limit2}"

        response1 = requests.get(url1)
        response2 = requests.get(url2)
        response3 = requests.get(url3)
        response4 = requests.get(url4)
        q = 1
    
    # Check if the responses are successful
    if response1.status_code == 200 and response2.status_code == 200:
        try:
            data1 = response1.json() ### last values
            data2 = response2.json() ### non last values
            if q==1:
                data3 = response3.json() ### non last values
                data4 = response4.json() ### non last values
                combined_data = data4 + data3 + data2 + data1
            else:
                data3 = response3.json() ### non last values
                data4 = response4.json() ### non last values
                data5 = response5.json() ### non last values
                data6 = response6.json() ### non last values
                data7 = response7.json() ### non last values
                combined_data = data7 + data6 + data5 + data4 + data3 + data2 + data1
            
            combined_data2 = [i[:5] for i in combined_data[-p2:]]
            return JsonResponse(combined_data2, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

def get_chart_data0(request):
    apiUrl = "https://fapi.binance.com/fapi/v1/klines"
    symbol = request.GET.get('symbol', 'BTCUSDT')  # Default to BTCUSDT if no symbol is provided
    interval = request.GET.get('interval', '1m')  # Default to 1m if no interval is provided
    limit = 72
    fullUrl = f"{apiUrl}?symbol={symbol}&interval={interval}&limit={limit}"

    response = requests.get(fullUrl)

    if response.status_code == 200:
        try:
            data = response.json()
            return JsonResponse(data, safe=False)
        except ValueError as e:
            return JsonResponse({'error': 'Unable to parse response data'}, status=500)
    else:
        return JsonResponse({'error': 'Could not fetch data from Binance API'}, status=500)

def get_timezone_offset(request):
    # First, get the client's public IP address
    ip_address = requests.get('https://api.ipify.org?format=json').json()['ip']

    # Then, pass that IP address to ipapi.co
    response = requests.get(f"https://ipapi.co/{ip_address}/json")

    if response.status_code == 200:
        data = response.json()

        # Convert the utc_offset string to milliseconds
        def offset_string_to_milliseconds(offset):
            sign = -1 if offset[0] == '-' else 1
            hours = int(offset[1:3])
            minutes = int(offset[3:5])
            return sign * ((hours * 60 + minutes) * 60 * 1000)

        timezone_offset = offset_string_to_milliseconds(data['utc_offset'])
        return JsonResponse({'timezoneOffset': timezone_offset}, safe=False)
    else:
        return JsonResponse({'error': 'Could not fetch data from ipapi.co'}, status=500)

def parse_date_from_filename(filename):
    date_string = filename.split("/")[-1].split('_')[3:9] # Split the filename and get the date part
    date_string = '_'.join(date_string) # Rejoin the date part
    return datetime.strptime(date_string, '%d_%m_%Y_%H_%M_%S') # Convert to datetime

def get_files(storage_client, bucket_name, coin_type):
    blobs = storage_client.list_blobs(bucket_name)  ### Bucket initialization
    files = [blob.name for blob in blobs if blob.name.startswith(f"mModels/{coin_type}/")]  ### Filter files by coin type
    # Sort files by date
    files.sort(key=parse_date_from_filename, reverse=True) # Sort in descending order so the latest file is first
    return files

def download_tmp_file(storage_client, bucket_name, blob_source):
    # Download files from bucket
    bucket = storage_client.bucket(bucket_name) # Initialize bucket
    blob = bucket.blob(blob_source)             # Initialize blob
    _, temp_local_path = tempfile.mkstemp()     # Create a temporary file
    blob.download_to_filename(temp_local_path)  # Download blob to temp file
    return temp_local_path

def unzip_file(zip_file_path, output_folder_path):
    # Unzip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder_path)  # Extract all files
        extracted_file_name = zip_ref.namelist()[0]  # Assuming the first file in the archive is the one you want
    # Return the full path of the extracted file
    return os.path.join(output_folder_path, extracted_file_name)  

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

@login_required
@api_view(['GET'])
def get_xtimes_preds(request, coin_type, interval):
    storage_client = storage.Client()
    # bucket_name = "xd_rock"  # update it with your bucket name
    bucket_name = "xd_block"  # update it with your bucket name
    
    ### latest files first
    files = get_files(storage_client, bucket_name, coin_type.upper())
    # If there are no files for this coin type, return an error
    if not files:
        return Response({"error": f"No files found for coin type: {coin_type}"}, status=404)
    # Otherwise, use the latest file
    L = []
    m = 3
    # for i in range(m-1, -1, -1):
    for i in range(len(files)-1, -1, -1):
        blob_source = files[i] ### 0
        print(blob_source)
        temp_file = download_tmp_file(storage_client, bucket_name, blob_source)
        output_folder_path = '/tmp'
        unzipped_csv = unzip_file(temp_file, output_folder_path)
        xtimes_preds_list = xtimes_preds(unzipped_csv, interval)
        L += xtimes_preds_list

    L2, ls = [], []
    for l in L:
        tmps, val = l
        if tmps not in ls:
            ls.append(tmps)
            L2.append(l)
    # m = 2160
    # m = 2000
    days = 4.85625
    base_m = 1440
    m = int(days*base_m)
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    I = {"1m":1, "3m":3, "5m":5, "15m":15, "30m":30, "1h":60}
    Q = I[interval]
    p2 = m//Q
    response = JsonResponse({"result": L2[-p2:]})
    # response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])

def futures_predictions(request, coin_type, interval):
    storage_client = storage.Client()
    # bucket_name = "xd_rock"  # update it with your bucket name
    bucket_name = "xd_block"  # update it with your bucket name
    
    ### latest files first
    files = get_files(storage_client, bucket_name, coin_type.upper())
    # If there are no files for this coin type, return an error
    if not files:
        return Response({"error": f"No files found for coin type: {coin_type}"}, status=404)
    # Otherwise, use the latest file
    L = []
    m = 3
    # for i in range(m-1, -1, -1):
    for i in range(len(files)-1, -1, -1):
        blob_source = files[i] ### 0
        print(blob_source)
        temp_file = download_tmp_file(storage_client, bucket_name, blob_source)
        output_folder_path = '/tmp'
        unzipped_csv = unzip_file(temp_file, output_folder_path)
        xtimes_preds_list = xtimes_preds(unzipped_csv, interval)
        L += xtimes_preds_list

    L2, ls = [], []
    for l in L:
        tmps, val = l
        if tmps not in ls:
            ls.append(tmps)
            L2.append(l)
    # m = 2160
    # m = 2000
    days = 4.85625
    base_m = 1440
    m = int(days*base_m)
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    I = {"1m":1, "3m":3, "5m":5, "15m":15, "30m":30, "1h":60}
    Q = I[interval]
    p2 = m//Q
    response = JsonResponse({"result": L2[-p2:]})
    # response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    return response

def xtimes_pred0(file_csv):
    # Generate predictionsdef xtimes_preds(file_csv):
    ds = pl.read_csv(file_csv, has_header=False)
    ds[['column_1']] = ds[['column_1']]*1e3
    W = [[int(i), j] for i, j in ds.to_numpy()]
    # ds = ds.with_columns([pl.col('column_1').cast(pl.Int64).cast(pl.Utf8), pl.col('column_2').cast(pl.Utf8)])
    # L = ds.to_numpy().tolist()
    return W[-600:]

def xtimes_preds(file_csv, interval):
    
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    W = D[interval]
    
    ds = pl.read_csv(file_csv, has_header=False)
    ds[['column_1']] = ds[['column_1']]*1e3
    ds = ds.with_columns([pl.col('column_1').cast(pl.Int64)])
    L = ds.to_numpy()#.tolist()
    
    dtimes = (L[:, 0]*1e6).astype('datetime64[ns]')
    # ds2 = pd.DataFrame(L[:, 1], index=dtimes).resample('30s').mean().reset_index()
    ds2 = pd.DataFrame(L[:, 1], index=dtimes).resample(W).mean().reset_index()
    
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    
    ds2['index'] = ((ds2['index'] - unix_epoch) / one_second).astype(int)*1e3
    ds2[0] = ds2[0].round(4)
    
    W = [[int(i), j] for i, j in ds2.to_numpy()]
    return W

def xtimes_preds_2(file_csv, interval):
    
    D = {"1m":"60s", "3m":"180s", "5m":"300s", "15m":"900s", "30m":"1800s", "1h":"3600s"}
    W = D[interval]
    
    ds = pl.read_csv(file_csv, has_header=False)
    ds[['column_1']] = ds[['column_1']]*1e3
    ds = ds.with_columns([pl.col('column_1').cast(pl.Int64)])
    L = ds.to_numpy()#.tolist()
    
    dtimes = (L[:, 0]*1e6).astype('datetime64[ns]')
    # ds2 = pd.DataFrame(L[:, 1], index=dtimes).resample('30s').mean().reset_index()
    ds2 = pd.DataFrame(L[:, 1], index=dtimes).resample(W).mean().reset_index()
    
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    
    ds2['index'] = ((ds2['index'] - unix_epoch) / one_second).astype(int)*1e3
    ds2[0] = ds2[0].round(4)
    
    W = [[int(i), j] for i, j in ds2.to_numpy()]
    return W
