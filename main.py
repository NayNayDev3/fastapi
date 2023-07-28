from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
# import time
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
        tempObject["name"] = x["name"]
        tempObject["symbol"] = x["symbol"]
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
    # currentTime = int(time.time())
    currentTime = 1690506094
    rewardsMoved = await getRewardsMoved()
    ethMoved = await getEthMoved()
    deployedTokens = await getTokensDeployed()
    totalList = []
    print("printing revenue")
    for x in rewardsMoved:
        copied = x.copy()

        if(copied['incoming'] == 1):
            copied["type"] = "revenue"  
        else:
            copied["type"] = "withdrawRev"  
        totalList.append(copied)
    for x in ethMoved:
        copied = x.copy()

        if(copied['code'] == 1):
            copied["type"] = "lent"
        elif(copied['code'] == 4):
            copied["type"] = "withdrawLent"
        elif(copied['code'] == 3):
            copied["type"] = "returnedBorrow"
        elif(copied['code'] == 2):
            copied["type"] = "borrow"

        totalList.append(copied)

    totalList.sort(key= lambda item:item['blocktime'])
    usersLentEth = 0
    usersWithdrawnRev = 0
    totalLentEth = 0
    usersRevenue = 0
    totalAvailable = 0
    dailyRevenue = 0
    for x in totalList:
        if('type' not in x):
            continue

        if(x['type']=="lent"):
            if(x['account'].lower() == account):
                usersLentEth = usersLentEth + x['amount']
            totalLentEth += x['amount']
            totalAvailable += x['amount']
        # elif(x['type']=="withdrawLent"):
        #     if(x['account'].lower() == account):
        #         usersLentEth = usersLentEth - x['amount']
        #     totalLentEth -= x['amount']
        #     totalAvailable -= x['amount']
        # elif(x['type']=="revenue"):
        #     if(totalLentEth!=0):
        #         usersRevenue = usersRevenue + (( x['amount'] * (usersLentEth/totalLentEth)) * 0.7)
        #         # if(x['account'].lower() == account and x["blocktime"] > currentTime - 86400):
        #         #     dailyRevenue = dailyRevenue + x['amount']
        # elif(x['type']=="returnedBorrow"):
        #     totalAvailable = totalAvailable + x['amount']
        # elif(x['type']=="borrow"):
        #     totalAvailable = totalAvailable - x['amount']
        # elif(x['type']=="withdrawRev"):
        #     if(x['account'].lower() == account):
        #         usersWithdrawnRev = usersWithdrawnRev +  x['amount'] 

    # print(f"Total Lent Eth: {totalLentEth}")
    # print(f"Users Current Lent Eth: {usersLentEth}")
    # print(f"Users Total Revenue: {usersRevenue / 10 ** 18}")
    # print(f"Users Withdrawn Revenue: {usersWithdrawnRev / 10 ** 18}")

    # deployedTokens.reverse()
    return {"dailyRevenue":dailyRevenue,"deployedTokens":deployedTokens,"usersLentEth":usersLentEth,"totalLentEth":totalLentEth,"usersRevenue":usersRevenue, "usersClaimedRevenue":usersWithdrawnRev,"totalAvailable":totalAvailable}
# @app.get('/{id}')
# async def root(id : int):
#     return {"id":id}