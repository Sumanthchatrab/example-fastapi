from fastapi import FastAPI
from . import schema
from datetime import datetime, timedelta

app = FastAPI()
@app.post("/post")
def ReqDelDate(data: schema.body):
    temp = []
    response = {"OrderId": None, "PK": None, "OrderLine": temp }
    for line in data.Order.OrderLine:
        if line["IsGiftCard"] == 1 and line["IsRefundGiftCard"] == 1:
            response["OrderId"] = line["OrderId"]
            response["PK"]= data.Order.PK
            created_time = line["CreatedTimestamp"]
            print(created_time)
            date = created_time.split('T')[0].replace("-","/")
            datetime_object = datetime.strptime(date,'%Y/%m/%d')
            rdd = datetime_object + timedelta(days=5)
            line_detail= {"RequestedDeliveryDate": rdd,
                          "ItemId": line["ItemId"],
                          "OrderLineId": line["OrderLineId"],
                          "Extended": { "O4UPC": line["Extended"]["O4UPC"] } }
            temp.append(line_detail)
        
    return response

