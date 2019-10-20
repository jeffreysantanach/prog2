import requests
projectid = str(1929283)
response = requests.get('http://www.meistertask.com/api/projects/1929283/work_intervals?',
 headers={'Authorization': 'Bearer 94c9d1cd91ad44d636b0e072d89c5c756cc23a55ee9841e76eb1217568f805f1'})