# build-in modules
import json
import logging
import time

# global modules
import schedule
from datetime import datetime

# own modules
import utils


def sync():
    global configuration, now, logID, delayTime, recCount, logging
    logging = utils.logging
    logging.basicConfig(
        filename="attendance.log",
        filemode="w",
        format="%(asctime)s: %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logging.info("Sync execution started")

    # global variables
    now = datetime.now()
    configuration = utils.config.readIni()
    recCount = 0
    # get the all config variable
    try:
        # send data to Attendance variables
        logID = configuration.getint("user", "logid")
    except:
        logID = 1

    try:
        # send data to Attendance variables
        delayTime = configuration.getint("common", "delaytime")
    except:
        delayTime = 10

    # get the database records
    attendanceData = getData()
    if len(attendanceData) != 0:
        if len(attendanceData) < 200:
            status = "failure"
            result = sendData(attendanceData)
            if "code" in result:
                if result["code"] == 3000:
                    utils.config.updateIni(
                        configuration, "user", "logId", str(logID + 1)
                    )
                    status = "success"
                else:
                    logging.info(
                        "APIReqError: Please contact developer. Details: %s" % (result)
                    )
            else:
                logging.info("APIReqError: Please contact developer")
            logging.info(
                "Successfully completed with %s row :)" % (recCount)
            ) if status == "success" else logging.info(
                "Failed with %s row :/" % (recCount)
            )
        else:
            attCount = len(attendanceData)
            apiCount = int(attCount / 200) + 1
            startIn = 0
            apiReqStatus = "success"
            successRecCount = 0
            for api in range(apiCount):
                status = "failure"
                endIn = startIn + 200
                dataList = attendanceData[startIn:endIn]
                dataCount = len(dataList)
                if dataCount > 0:
                    result = sendData(dataList)
                    if "code" in result:
                        if result["code"] == 3000:
                            utils.config.updateIni(
                                configuration, "user", "logId", str(logID + 1)
                            )
                            status = "success"
                            successRecCount = successRecCount + dataCount
                            logging.info(
                                "Successfully completed APIReq-%s with %s row :)"
                                % (str(api + 1), dataCount)
                            )
                        else:
                            logging.info(
                                "APIReqError-%s: Please contact developer. Details: %s"
                                % (str(api + 1), result)
                            )
                    else:
                        logging.info(
                            "APIReqError-%s: Please contact developer" % (str(api + 1))
                        )
                if status != "success":
                    apiReqStatus = "failure"
                startIn = endIn
            logging.info(
                "Successfully completed the API requests with %s row :/"
                % (successRecCount)
            ) if apiReqStatus == "success" else logging.info(
                "APIs might be failed with %s row :/" % (attCount - successRecCount)
            )

    logging.info("Sync execution ended")
    # set the last sync time
    utils.config.updateIni(configuration, "common", "fromtime", str(now))


def getData():
    try:
        # configuration variables
        database = configuration.get("database", "database")
        sqlquery = configuration.get("database", "sqlquery")
        fromTime = configuration.get("common", "fromtime")
    except:
        logging.info("ConfigError: Please contact developer")
        raise AttributeError("ConfigError: Please contact developer")

    # configuration variables
    try:
        databaseID = configuration.getint("database", "id")
    except:
        databaseID = 1

    try:
        server = configuration.get("database", "server")
    except:
        server = "localhost"

    try:
        uid = configuration.get("database", "username")
        pwd = configuration.get("database", "password")
    except:
        uid = "admin"
        pwd = "admin"

    try:
        toTime = configuration.get("common", "totime")
    except:
        toTime = now

    # connect to the database
    dbconn = utils.database.connectDB(databaseID, database, server, uid, pwd)

    # query a database records
    lastSync = datetime.strptime(fromTime, "%Y-%m-%d %H:%M:%S.%f")

    query = utils.database.formatDynamicTable(sqlquery)
    if query.count("?") == 2:
        queryParams = (lastSync, toTime)
    elif query.count("?") == 4:
        queryParams = (lastSync, toTime, lastSync, toTime)
    else:
        raise Exception("SQL Query: query has mismatched random value")

    dataList = utils.database.executeQuery(dbconn, query, queryParams)
    logging.info("Queried datalist: %s", dataList)
    return dataList


def sendData(data):
    global recCount
    try:
        userID = configuration.getint("user", "id")
    except:
        logging.info("ConfigError: Please contact developer")
        raise AttributeError("ConfigError: Please contact developer")

    try:
        endpointURL = configuration.get("user", "endpointURL")
    except:
        endpointURL = "https://creator.zoho.in/api/v2/buildhrmanagementconsultants/contract-management-system/form/attendance_data"

    authToken = utils.getOauthToken()
    headers = {"Authorization": "Zoho-oauthtoken %s" % (authToken)}
    bodyData = {"result": {"fields": ["log", "organization", "details"]}}
    recList = utils.splitMemSpace(data)
    dataList = []
    recCount = recCount + len(recList)
    for rec in recList:
        dataMap = {"log": logID, "organization": userID, "details": rec}
        dataList.append(dataMap)
    bodyData["data"] = dataList
    res = utils.httpReq.post(endpointURL, json.dumps(bodyData), headers)
    result = json.loads(res.text)
    logging.info("Req Res: %s", result)
    return result


# -> config the schedule
sync()
schedule.every(delayTime).minutes.do(sync)

while True:
    schedule.run_pending()
    time.sleep(1)
# <-
