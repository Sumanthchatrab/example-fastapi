from fastapi import FastAPI
from . import schema
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

@app.post("/post")
def ReqDelDate(data: schema.body):
    temp = []
    length= len(data.Order.OrderLine)
    count=0
    response = {"OrderId": None, "PK": None, "OrderLine": temp }
    response["PK"]= data.Order.PK
    response["OrderId"] = data.Order.OrderLine[0]["OrderId"]

    for line in data.Order.OrderLine:
        if line["IsGiftCard"] == 1 and line["IsRefundGiftCard"] == 1:
            created_time = line["CreatedTimestamp"]
            date = created_time.split('T')[0].replace("-","/")
            datetime_object = datetime.strptime(date,'%Y/%m/%d')
            rdd = datetime_object + timedelta(days=5)
            line_detail= {"RequestedDeliveryDate": rdd,
                          "ItemId": line["ItemId"],
                          "OrderLineId": line["OrderLineId"],
                          "Extended": { "O4UPC": line["Extended"]["O4UPC"] } }
            temp.append(line_detail)

        elif line["IsRefundGiftCard"]==0  and line["IsGiftCard"] == 0:
            count= count+1 

    if length==count:
        response.pop("OrderLine")         
    return response

