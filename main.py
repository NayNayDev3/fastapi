from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

client = MongoClient("mongodb+srv://basicUser:fO2yUzuLrcnbxOyW@mythcity.kcmvkv5.mongodb.net/")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
operaDB = client.test
tokensDeployedCollection = operaDB.tokendeployeds
withdrawnFromLockCollection = operaDB.withdrawnfromlocks
tokensLockedCollection = operaDB.tokenlockeds
rewardsMovedCollection = operaDB.rewardsmoveds
ethMovedCollection = operaDB.ethmoveds



async def getTokensDeployed():
    tempObject = {}
    tempList = []
    for x in tokensDeployedCollection.find():
        tempObject["user"] = x["user"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["token"] = x["token"]
        tempObject["amount"] = x["amountEth"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getTokensWithdrawnFromLock():
    tempObject = {}
    tempList = []
    for x in withdrawnFromLockCollection.find():
        tempObject["token"] = x["token"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempList.append(tempObject.copy())
    return tempList
async def getTokensLocked():
    tempObject = {}
    tempList = []
    for x in tokensLockedCollection.find():
        tempObject["token"] = x["token"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["locktime"] = x["locktime"]
        tempObject["account"] = x["account"]
        tempList.append(tempObject.copy())
    return tempList
async def getEthMoved():
    tempObject = {}
    tempList = []
    for x in ethMovedCollection.find():
        tempObject["account"] = x["account"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempObject["code"] = x["code"]
        tempList.append(tempObject.copy())
    return tempList
async def getRewardsMoved():
    tempObject = {}
    tempList = []
    for x in rewardsMovedCollection.find():
        tempObject["account"] = x["account"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempObject["incoming"] = x["incoming"]
        tempList.append(tempObject.copy())
    return tempList


@app.get('/')
async def root():

    return {"id":0}
@app.get('/maindata/{account}')
async def getData(account):
    print(account)
    rewardsMoved = await getRewardsMoved()
    ethMoved = await getEthMoved()
    totalList = []
    print("printing revenue")
    for x in rewardsMoved:
        copied = x.copy()
        print(copied)
        if(copied['incoming'] == 1):
            copied["type"] = "revenue"  
        else:
            copied["type"] = "withdrawRev"  
        totalList.append(copied)
    for x in ethMoved:
        copied = x.copy()
        print(copied)
        if(copied['code'] == 1):
            copied["type"] = "lent"
        elif(copied['code'] == 4):
            copied["type"] = "withdrawLent"

        totalList.append(copied)

    totalList.sort(key= lambda item:item['blocktime'])
    usersLentEth = 0
    usersWithdrawnRev = 0
    totalLentEth = 0
    usersRevenue = 0

    for x in totalList:
        if('type' not in x):
            continue
        print(x)
        if(x['type']=="lent"):
            if(x['account'].lower() == account):
                usersLentEth = usersLentEth + x['amount']
            totalLentEth += x['amount']
        elif(x['type']=="withdrawLent"):
            if(x['account'].lower() == account):
                usersLentEth = usersLentEth - x['amount']
            totalLentEth -= x['amount']
        elif(x['type']=="revenue"):
            usersRevenue = usersRevenue + (( x['amount'] * (usersLentEth/totalLentEth)) * 0.7)
        elif(x['type']=="withdrawRev"):
            if(x['account'].lower() == account):
                usersWithdrawnRev = usersWithdrawnRev +  x['amount'] 
    print(f"Total Lent Eth: {totalLentEth}")
    print(f"Users Current Lent Eth: {usersLentEth}")
    print(f"Users Total Revenue: {usersRevenue / 10 ** 18}")
    print(f"Users Withdrawn Revenue: {usersWithdrawnRev / 10 ** 18}")

    
    return {"usersLentEth":usersLentEth,"totalLentEth":totalLentEth,"usersRevenue":usersRevenue, "usersClaimedRevenue":usersWithdrawnRev}
# @app.get('/{id}')
# async def root(id : int):
#     return {"id":id}