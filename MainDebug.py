# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 10:53:03 2022

@author: Ken
"""

import requests,json,time,uuid,sys,random,datetime


headers = {
    'x-amz-access-token': '',



    'x-flex-instance-id': '',
    
    
    'X-Amzn-RequestId': str(uuid.uuid4()),
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 12; Pixel 6 Build/S3B1.220318.003) RabbitAndroid/3.72.1.25.0',
    'X-Flex-Client-Time': str(int(time.time() * 1000)),
    
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'Authorization': 'RABBIT3-HMAC-SHA256 SignedHeaders=host;x-amz-access-token;x-amz-date;x-amzn-requestid,Signature=SIGNATURE',
    'Host': 'flex-capacity-na.amazon.com',
}




def accept_block(headers,offerId):
    # Accepting a block, returns status code. 200 is a successful attempt and 400 (I think, could be 404 or something else) is a failed attempt
    r = requests.Session()

    url = "https://flex-capacity-na.amazon.com/AcceptOffer"
    
    data = json.dumps({
                          "__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/",
                          "offerId": offerId
                        })
                            
    res = r.post(url,headers = headers , data = data)
    return res.status_code

    

def filter_blocks(block):
    # Filtering out blocks that you don't want.
    # Comment out individual filters that you don't want applied
    block_length = (block["endTime"] - block["startTime"]) / 3600
    start_time =  datetime.datetime.fromtimestamp( block["startTime"]  )

    frame_start = datetime.datetime(2022, 10, 11, 6, 00)
    frame_end   = datetime.datetime(2022, 10, 11, 16, 0)

    serviceAreaFilter = [
                          "96898094-4c98-4cb4-ac83-db44767a9149",
                          "1f2ef849-eac6-408a-b8e3-80766e63ca2a",
                          "22eaac51-fa93-4d4f-8847-2db4a02181d2"
                        ]
                                              
    block['serviceAreaId']

    if block["hidden"]:
      print("Block Hidden")
      return False
    
    # if block["startTime"] - int(time.time()) >= 18000: #start in less than 5 hour:
    #   print(" start time over 5 hours ")
    #   return False
    if not (frame_start <= start_time and start_time <= frame_end):
      print(f"Block not in desired time frame {str(start_time)}")
      return False

    if block_length > 5      :
      print(f"Block length {block_length}")
      return False

    if block['serviceAreaId'] not in serviceAreaFilter:
      print("Block out of service area")
      return False

    return True
    # return (
    #     not block["hidden"]
    #     and block["startTime"] - int(time.time()) <= 18000 #start in less than 5 hour
    #     and block_length < 5                              #less than 5 hours block 
    #     and block['serviceAreaId'] not in serviceAreaFilter
    # ) 


r = requests.Session()



Url = "https://flex-capacity-na.amazon.com/GetOffersForProviderPost"

data = json.dumps({
                    "apiVersion": "V2",
                    "filters": {
                      "deliveryRequestFilter": {
                        "deliveryRequestCount": 0,
                        "orderCount": 0
                      },
                      "serviceAreaFilter": [
                        "96898094-4c98-4cb4-ac83-db44767a9149",
                        "1f2ef849-eac6-408a-b8e3-80766e63ca2a",
                        "22eaac51-fa93-4d4f-8847-2db4a02181d2"
                      ],
                      "timeFilter": {}
                    },
                    "serviceAreaIds": [
                      "811f0105-4e37-4ff6-b4ea-f7a13d301648"
                    ]
                  })
while True: #3:27
    Timenow = time.time()

    res = r.post(Url,headers = headers , data = data)
    
    if res.status_code == 400 and res.json()['message'] == 'Rate exceeded':
      print("Rate Exceed")
      time.sleep(90)
      continue

    offerlist = res.json()['offerList']
    if offerlist != [] :
        print(f'{Timenow} - Got {len(offerlist)} blocks')
        for block in offerlist:
            
            if filter_blocks(block):
                accepting = accept_block(headers,block["offerId"])
                if accepting == 200 :
                    s = input(f"Caught The Block For {block['rateInfo']['priceAmount']}")
                    sys.exit()
                    break
                else:
                    print(f"Fail To Catch The Block For {block['rateInfo']['priceAmount']}")
                    continue
            else:
                print(f'Block No Good')
                continue
    else:
        print(f'{Timenow} - no block')
            #******** Logic 
    x = random.uniform(0.5, 2)	
    xy = random.random()
    time.sleep(x)


    
    
    
