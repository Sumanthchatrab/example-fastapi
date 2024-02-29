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
    allow_headers=["*"],
)
@app.post("/post")
def ReqDelDate(data: schema.body):
    temp = []
  
    for line in data.Order.OrderLine:
    response = {"OrderId": None, "PK": None, "OrderLine": temp }
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
         elif line["IsRefundGiftCard"]==0 and line["IsGiftCard"]==0:
            response["OrderId"]=line["OrderId"]
            response["PK"]=data.Order.PK
            response.pop("OrderLine")
        
    return response

