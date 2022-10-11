# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 10:53:03 2022

@author: Ken
"""

import requests,json,time,uuid,sys,random,datetime


headers = {
    'x-amz-access-token': 'Atna|EwICIEfggdDMv_ZQ4dAPLt1_Tx3BYGOg__VrkJ5Rk3macH4wPicntda_E2zLeKsTVX3GQbe9q8uNjF2KyLwvnz_ulqpDPRbPWGxyGzyj0uqdvrGtjacqDwSL6QnxPdcfE1996sLh3qIJzQ1pLVzPTwsy2lkscwIpBevxkOX5NSgtAZPRc4xuSUVP6pHP1C6MfuwpR9yaslLW3p490itk1wEKlIvsgygpPetbKqAa72zjIXnTjP000WCAXeVeIiGPjHPANEB7vbYu6tuEGqSAX05Vadyp5NwZ68lF_CrPowSY5U_vugzSZ2tgYqH5iT_0-eIakEs3VzP6LrloGUzFjDSo4t49',




    'x-flex-instance-id': 'a3e8f85d-121a-46f3-abe8-ac9f026e74dc',
    
    
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


    
    
    

# https://flex-capacity-na.amazon.com/AcceptOffer

    
# {
#   "__type": "AcceptOfferInput:http://internal.amazon.com/coral/com.amazon.omwbuseyservice.offers/",
#   "offerId": "Ok9mZmVySWQuRW5jcnlwdGlvbktleS02aGlZbDQAAACDDtWCQwquLr5pJsGZl2myL4h3776OFJ8fwCyr4JUBvxT90Zb+McgTw1ReXrik3nNaxkr1rvzzP3b3PyA6KgD0pfDSC55Wrh5p4/pDRAHLSB5VfBw/Ttpg7LCARTeuhoJxD7kIapOP9GPAwui8xuglfoT63m3YHHrwm79V9STwR1eP2Wd5tZztArmG2xEiOgbkuH9JbIDP20EHoDjxz88QAAfftDNVR+q4v8ezpYgrog03eVl+NQq2zzJUmMMxVmOYnaNEmTHKHE4+lDHOHe9yT0vQNZV/Mc5sdqMo1XhstMH9SlY+NNvD9+0KR/zX4Dh4EeA4ezZWR9FwG+9PvhgyRfQaQCM0YAKPzZPGMXxFSVcI/mFgDyfTfNVPvahqCFqkxR4OVkzRFkpsbVIj6Cd5qYveAFfk75z6QtADA4XaJdPeFKybnhtRvj2IoZBYYjgnasxysZWT2HBEg40936ufH54pf6wmnAQoX79AJWUbv6+Ichk4+xsGu9rEeWrggFK+0hm5E75w5TN8fTACtIvFALeU3voIK6XW0eDaFoGnK9Wt/699/ZvGoC4R4nZAQeBXNErKVcsRfg==|mAeYxHSne8pbbXC2KUDfZFdFur4FwHVfBu4bZwL3Jq8="
# }


# {"offerExperienceVersion":"V1","offerList":[{"creationDate":null,"deliveryCutOffTimeEpoch":null,"deliveryRequest":{"deliveryRequestCount":1.0,"orderCount":10},"endTime":1.664658E9,"expirationDate":1.6646508E9,"hidden":false,"isPriorityOffer":false,"legalEntity":null,"maxWorkload":0,"offerId":"Ok9mZmVySWQuRW5jcnlwdGlvbktleS02aGlZbDQAAACDDtWCQwquLr4zKMfLwDy3f4hytb3ZFJ8fxS6r4Z0H6BTy0pb0Mc4TlwJeX7uk3nNaxkr1rvzzP3b3PyA6KgD0pfDSC55Wrh5p4/pDRAHLSB5VfBw/Ttpg7LCARTeuhoJxD7kIapOP92vAwui8xuglfYL63m3YHHrwm79V9STwR1eP2Wd5tZztALiC2UslbVfk439KP4DP2UMCoGOmnMcQUlbc5mcDFru8uczppYgr9Ag5dgZ3ZQ62yWNXmMMxCTWanaNMkmbKTEhixTDHS7p1TkvSNZV/Mc5sdqMo1XhstMH9SlY+NNvD9+0KR/zX4Dh4EeA4ezZWR9FwEeRZrxNWLYp5IFxDE2jvp+q5UwUhPmx8ikQUakTedt1Ns6c9DQ+qyEoOUx+DDhFobQQvuXwkr4SDU1G578CqEIZdVYrYediLQfybzU1T6DyLps0GZTUubs5z5JTG3yURiYk7iq7PGswpe/t2mw1/D+kUcjNJ46uLcks0+0hc7YGde2q30Qfi0x6+FrYm4zR9LWBSvoPKsjvV1S9RXd7ohJOd6DQndg==|Ldt68PjhRStpl6AfPNATs/VxKxAub750/Tl2PG5Bj9U=","offerMetadata":null,"offerType":"NON_EXCLUSIVE","rateInfo":{"PriceDetails":null,"currency":"USD","isSurge":false,"priceAmount":44.0,"pricingUXVersion":"V2","projectedTips":30.0,"surgeMultiplier":null},"schedulingType":"BLOCK","serviceAreaId":"88c3e32b-7c01-4510-88bf-7f43b5d175eb","serviceTypeId":"amzn1.flex.st.v1.PuyOplzlR1idvfPkv5138g","serviceTypeMetadata":{"modeOfTransportation":null,"nameClassification":"STANDARD"},"startTime":1.6646508E9,"startingLocation":{"address":{"address1":"","address2":null,"address3":null,"addressId":null,"city":null,"countryCode":null,"name":null,"phone":null,"postalCode":null,"state":null},"geocode":{"latitude":0.0,"longitude":0.0},"locationType":null,"startingLocationName":""},"status":"OFFERED","trIds":null}],"refreshInterval":1000,"refreshTimeout":1800000}