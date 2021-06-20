import requests
import json
import argparse
import os


def send(payload, token=None):
    headers = {
        "authority": "api.crypto-arsenal.io",
        "method": "POST",
        "path": "/",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-TW,zh;q=0.9,en-AS;q=0.8,en;q=0.7,en-US;q=0.6",
        "authorization": token,
        "content-length": "5638",
        "content-type": "application/json",
        "origin": "https//www.crypto-arsenal.io",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    response = requests.post(url="https://api.crypto-arsenal.io/", headers=headers, json=payload)
    return response.json()


def login():
    with open('setting.json', 'r') as f:
        user_information = json.loads(str(f.read()))
    payload = [{
        "operationName":
        "LoginMutation",
        "variables": {
            "email": user_information.get("email"),
            "password":  user_information.get("password")
        },
        "query":
        "mutation LoginMutation($email: String, $password: String!) {\n  login(email: $email, password: $password)\n}\n"
    }]
    result = send(payload)
    if not result[0].__contains__('errors'):
        # print(result)
        return result
    else:
        print("登入失敗")
        os._exit(0)


def GetStrategyList(token):
    payload = [{
        "operationName":
        "GetStrategyList",
        "variables": {},
        "query":
        "query GetStrategyList {\n  me {\n    id\n    strategies {\n      id\n      name\n      desc\n      note\n      binaryFilename\n      language\n      remoteToken\n      type\n      backtestTasks(page: 0, countsPerPage: 1, status: FINISHED, reverseOrder: true) {\n        profitVector(pointsCount: 80) {\n          points {\n            profit\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      isBacktesting\n      isSimulating\n      isTrading\n      isRemote\n      isBinary\n      isConnected\n      updatedAt\n      createdAt\n      version\n      baseExchange\n      baseCurrency\n      status\n      relatedCompetitionId\n      submittedAt\n      verifiedAt\n      rejectedAt\n      onBoardAt\n      options {\n        id\n        name\n        type\n        defaultValue\n        desc\n        tips\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }]
    token = "Bearer "+token
    return send(payload, token)


def GetStrategyOverview(token, ID):
    payload = [{
        "operationName":
        "GetStrategyOverview",
        "variables": {
            "id": str(ID)
        },
        "query":
        "query GetStrategyOverview($id: ID!) {\n  getStrategy(id: $id) {\n    id\n    name\n    desc\n    note\n    binaryFilename\n    language\n    remoteToken\n    type\n    isBacktesting\n    isSimulating\n    isTrading\n    isRemote\n    isBinary\n    isConnected\n    updatedAt\n    createdAt\n    version\n    baseExchange\n    baseCurrency\n    status\n    submittedAt\n    verifiedAt\n    rejectedAt\n    onBoardAt\n    relatedCompetitionId\n    options {\n      id\n      name\n      type\n      defaultValue\n      desc\n      tips\n      __typename\n    }\n    __typename\n  }\n}\n"
    }, {
        "operationName":
        "GetStrategyCode",
        "variables": {
            "id": str(ID)
        },
        "query":
        "query GetStrategyCode($id: ID!) {\n  getStrategy(id: $id) {\n    id\n    code\n    language\n    __typename\n  }\n}\n"
    }]
    token = "Bearer "+token
    return send(payload, token)


def UpdateStrategy(token, ID, name, code, options):
    payload = [{
        "operationName":
        "UpdateStrategy",
        "variables": {
            "strategyId": str(ID),
            "strategy": {
                "name": name,
                "desc": "",
                "code": code,
                "isRemote": False,
                "isBinary": False,
                "binaryFilename": None,
                "language": "PYTHON",
                "baseExchange": None,
                "baseCurrency": None,
                "type": "SINGLE_PAIR",
                "note": None,
                "options": options
            }
        },
        "query":
        "mutation UpdateStrategy($strategyId: ID!, $strategy: StrategyInput!) {\n  updateStrategy(strategyId: $strategyId, strategy: $strategy) {\n    id\n    desc\n    isRemote\n    type\n    note\n    code\n    isBinary\n    binaryFilename\n    language\n    name\n    createdAt\n    updatedAt\n    version\n    baseExchange\n    baseCurrency\n    options {\n      id\n      name\n      type\n      defaultValue\n      desc\n      tips\n      __typename\n    }\n    __typename\n  }\n}\n"
    }]
    token = "Bearer "+token
    return send(payload, token)


def download(token, StrategyList, ID_list, ID):
    try:
        if ID != "a":
            if ID not in ID_list:
                print("策略ID輸入錯誤")
                os._exit(0)
            ID_list = [ID]
        for ID in ID_list:
            StrategyOverview = GetStrategyOverview(token, ID)
            trade_name = StrategyOverview[0]["data"]["getStrategy"]["name"]
            if StrategyOverview[1]["data"]["getStrategy"]["code"]:
                folderpath = "trade\\"+str(ID)+"_"+trade_name
                if not os.path.isdir(folderpath):
                    os.makedirs(folderpath)
                filename = folderpath+"\\"+"trade.py"
                filename_o = folderpath+"\\"+"options.json"
                try:
                    with open(filename, 'w', newline='') as f:
                        f.write(StrategyOverview[1]["data"]["getStrategy"]["code"])
                        f.close()
                    with open(filename_o, 'w', newline='') as f:
                        for i in range(len(StrategyOverview[0]["data"]["getStrategy"]["options"])):
                            del StrategyOverview[0]["data"]["getStrategy"]["options"][i]["id"]
                            del StrategyOverview[0]["data"]["getStrategy"]["options"][i]["__typename"]
                        f.write(json.dumps(StrategyOverview[0]["data"]["getStrategy"]["options"]))
                        f.close()
                except Exception as e:
                    print("error in ID:", ID, ",error:", e)
            else:
                print("error in ID:", ID, ", name:", trade_name)
        return "下載成功"
    except Exception as e:
        return "失敗: " + str(e)


def upload(token, ID):
    try:
        name_list = []
        ID_list = []
        folderpath = "trade//"
        if ID == "a":
            for i in os.listdir(folderpath):
                filename = i.split("_")
                ID_list.append(filename[0])
                name = filename[1:]
                str_name = "_".join(name)
                name_list.append(str_name)
        else:
            ID_list = [ID]
            for i in os.listdir(folderpath):
                filename = i.split("_")
                if filename[0] == ID:
                    name = filename[1:]
                    str_name = "_".join(name)
                    name_list.append(str_name)
        for i in range(len(ID_list)):
            ID = ID_list[i]
            name = name_list[i]
            folderpath = "trade\\"+str(ID)+"_"+name
            filename = folderpath+"\\"+"trade.py"
            filename_o = folderpath+"\\"+"options.json"
            with open(filename, 'r') as f:
                code = str(f.read())
                f.close()
            with open(filename_o, 'r') as f:
                str_o = str(f.read())
                options = eval(str_o)
                f.close()
            UpdateStrategy(token, ID, name, code, options)
        return "上傳成功"
    except Exception as e:
        return "失敗: " + str(e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("arg1",
                        type=str,
                        nargs='?',
                        help="操作(ex:u):上傳u,下載d")
    parser.add_argument("arg2",
                        type=str,
                        nargs='?',
                        help="ID(ex:5566):指定id或是a下載全部")
    args = parser.parse_args()
    if not os.path.isdir("trade"):
        os.makedirs("trade")
    token = login()[0]["data"]["login"]
    StrategyList = GetStrategyList(token)
    times_p = len(StrategyList[0]["data"]["me"]["strategies"])
    ID_list = []
    print("-------------------------------------------------")
    for times in range(times_p):
        ID_list.append(StrategyList[0]["data"]["me"]["strategies"][times]["id"])
        print("策略ID:{}, 策略名稱:{} ".format(StrategyList[0]["data"]["me"]["strategies"][times]["id"],StrategyList[0]["data"]["me"]["strategies"][times]["name"]))
    print("-------------------------------------------------")
    if args.arg1:
        method = args.arg1
    else:
        method = input("請輸入操作(上傳u,下載d): ")
    if args.arg2:
        ID = args.arg2
    else:
        ID = input("請輸入策略ID(全部請輸入a): ")
    if method == "d":
        print(download(token, StrategyList, ID_list, ID))
    elif method == "u":
        print(upload(token, ID))
    else:
        print("錯誤操作")
    print("-------------------------------------------------")
    print("done")


if __name__ == "__main__":
    main()
