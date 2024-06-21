#!/usr/bin/env python3
""" Importing a csv file """
import requests

url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2020/5/7d3576d97e7560ae85135cc214ffe2b3412c51d7.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240621%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240621T145507Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=d94e277f7a39c6c85cd50ae3e74894a4b9f5b45e8ef57a8e97ac8d9ee402e41d"

response = requests.get(url)

if response.status_code == 200:
    with open('Popular_Baby_Names.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(response.text)
    print('File successfully written in the csv file')
else:
    print('Unsuccessful writing in csv file')
