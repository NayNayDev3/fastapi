from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

client = MongoClient("mongodb+srv://tonybalogny69:LQv93WjBC0hbXj7a@mythcity.kcmvkv5.mongodb.net/")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
operaDB = client.test
rewardsPaidCollection = operaDB.rewardpaids
ethBorrowedCollection = operaDB.ethborroweds
ethLentCollection = operaDB.ethlents
ethWithdrawnCollection = operaDB.ethwithdrawns
queueAddedCollection = operaDB.queueaddeds
rewardsRecievedCollection = operaDB.rewardrecieveds
tokensDeployedCollection = operaDB.tokendeployeds
withdrawnFromLockCollection = operaDB.withdrawnfromlocks
tokensLockedCollection = operaDB.tokenlockeds
ethReturnedCollection = operaDB.ethreturnds


async def getEthBorrowed():
    tempObject = {}
    tempList = []
    for x in ethBorrowedCollection.find():
        tempObject["borrower"] = x["borrower"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getEthReturned():
    tempObject = {}
    tempList = []
    for x in ethReturnedCollection.find():
        tempObject["borrower"] = x["borrower"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getRewardsPaid():
    tempObject = {}
    tempList = []
    for x in rewardsPaidCollection.find():
        tempObject["receiver"] = x["receiver"]
        tempObject["amount"] = x["amount"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getEthLent():
    tempObject = {}
    tempList = []
    for x in ethLentCollection.find():
        tempObject["lender"] = x["lender"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getEthWithdrawn():
    tempObject = {}
    tempList = []
    for x in ethWithdrawnCollection.find():
        tempObject["lender"] = x["lender"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
async def getQueueAdded():
    tempObject = {}
    tempList = []
    for x in queueAddedCollection.find():
        tempObject["lender"] = x["lender"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempObject["position"] = x["position"]
        tempList.append(tempObject.copy())
    return tempList
async def getRewardsRecieved():
    tempObject = {}
    tempList = []
    for x in rewardsRecievedCollection.find():
        tempObject["sender"] = x["sender"]
        tempObject["transactionHash"] = x["transactionHash"]
        tempObject["amount"] = x["amount"]
        tempObject["blocktime"] = x["blocktime"]
        tempList.append(tempObject.copy())
    return tempList
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


async def load():
    await getEthBorrowed()
    await getRewardsPaid()
    await getEthLent()
    await getEthWithdrawn()
    await getQueueAdded()
    await getRewardsRecieved()
    await getTokensDeployed()
    await getTokensWithdrawnFromLock()
    await getEthReturned()
    await getTokensWithdrawnFromLock()
    await getTokensLocked()

@app.get('/')
async def root():

    return {"id":0}
@app.get('/maindata/{account}')
async def getData(account):
    print(account)
    revenue = await getRewardsRecieved()
    ethLent = await getEthLent()
    ethWithdrawn = await getEthWithdrawn()
    totalList = []
    print("printing revenue")

    for x in revenue:
        copied = x.copy()
        copied["type"] = "revenue"
        totalList.append(copied)
    print("printing eth lent")
    for x in ethLent:
        copied = x.copy()
        copied["type"] = "lent"
        totalList.append(copied)
    print("printing withdrawn")
    for x in ethWithdrawn:
        copied = x.copy()
        copied["type"] = "withdrawn"
        totalList.append(copied)
    totalList.sort(key= lambda item:item['blocktime'])
    usersLentEth = 0
    totalLentEth = 0
    usersRevenue = 0
    for x in totalList:
        if(x['type']=="lent"):
            if(x['lender'].lower() == account):
                usersLentEth = usersLentEth + x['amount']
            totalLentEth += x['amount']
        elif(x['type']=="withdrawn"):
            if(x['lender'].lower() == account):
                usersLentEth = usersLentEth - x['amount']
            totalLentEth -= x['amount']
        elif(x['type']=="revenue"):
            usersRevenue = usersRevenue + ( x['amount'] * (usersLentEth/totalLentEth))
    print(f"Total Lent Eth: {totalLentEth}")
    print(f"Users Current Lent Eth: {usersLentEth}")
    print(f"Users Total Revenue: {usersRevenue / 10 ** 18}")

    
    return {"usersLentEth":usersLentEth,"totalLentEth":totalLentEth,"usersRevenue":usersRevenue}
# @app.get('/{id}')
# async def root(id : int):
#     return {"id":id}