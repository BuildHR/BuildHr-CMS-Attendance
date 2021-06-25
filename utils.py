# build-in modules
import os
import sys
import logging
import json
from configparser import ConfigParser
from datetime import datetime

# global modules
import pyodbc
import requests
from dotenv import load_dotenv

# global config
configParser = ConfigParser()
now = datetime.now()
load_dotenv()

# global variables
if os.getenv("ref") != None:
    ref = os.getenv("ref")
if os.getenv("cid") != None:
    cid = os.getenv("cid")
if os.getenv("cst") != None:
    cst = os.getenv("cst")

# -> global functions


def getOauthToken():

    httpRes = httpReq.post(
        "https://accounts.zoho.in/oauth/v2/token?refresh_token=%s&client_id=%s&client_secret=%s&grant_type=refresh_token"
        % (ref, cid, cst)
    )
    res = json.loads(httpRes.text)

    if "access_token" in res:
        authToken = res["access_token"]
        return authToken
    else:
        logging.info("OauthError: Please contact developer")
        return ""


"""
    @author: SS Subash
    limitedSpace for Zoho Multi line space
"""


def splitMemSpace(anyObj, limitedSpace=65477):
    result = []
    if type(anyObj) != "str":
        anyObj = str(anyObj)
    anyObjByte = sys.getsizeof(anyObj)
    if anyObjByte > limitedSpace:
        logging.info("Data was exceed the limit " + str(limitedSpace))
        logging.info("Total length of attendence data: " + str(len(anyObj)))
        resultSize = int(round(anyObjByte / limitedSpace, 0))
        index = int(round(len(anyObj) / resultSize, 0))
        startIn = 0
        for i in range(resultSize):
            endIn = startIn + index
            logging.info("StartIn: %s, EndIn: %s" % (str(startIn), str(endIn)))
            result.append(anyObj[startIn:]) if i == (resultSize - 1) else result.append(
                anyObj[startIn:endIn]
            )
            startIn = endIn
    else:
        result.append(anyObj)
    return result


def prefix(some, search):
    if not isinstance(some, str):
        raise Exception("Prefix: Given value is not a str")
    startIndex = some.find(search)
    return some[:startIndex]


def suffix(some, search):
    if not isinstance(some, str):
        raise Exception("Prefix: Given value is not a str")
    startIndexofsearch = some.find(search)
    searchLen = len(search)
    startIndex = startIndexofsearch + searchLen
    return some[startIndex:]


def formatDatetime(dTstr):
    dateTime = prefix(suffix(dTstr, "("), ")")
    elements = dateTime.split(",")
    result = elements[0]
    return result


# <-

# -> HTTP requests function


class httpReq:
    def post(endpointURL, bodyData={}, headers={}):
        response = requests.post(endpointURL, bodyData, headers=headers)
        return response


# <-

# -> database functions


class database:
    def connectDB(
        databaseID,
        database,
        server,
        uid,
        pwd,
        driver="{Microsoft Access Driver (*.mdb, *.accdb)}",
        charset="utf8mb4",
    ):

        if databaseID == 1:
            connection_string = (
                "DRIVER=%s;"
                "DBQ=%s;"
                "UID=%s;"
                "PWD=%s;" % (driver, database, uid, pwd)
            )
        elif databaseID == 2:
            driver = "MySQL ODBC 8.0 Unicode Driver"
            connection_string = (
                "DRIVER=%s;"
                "SERVER=%s;"
                "DATABASE=%s;"
                "UID=%s;"
                "PWD=%s;"
                "charset=%s;" % (driver, server, database, uid, pwd, charset)
            )
        else:
            driver = "ODBC Driver 17 for SQL Server"
            connection_string = (
                "DRIVER=%s;"
                "SERVER=%s;"
                "DATABASE=%s;"
                "UID=%s;"
                "PWD=%s;"
                "Trusted_Connection=yes;" % (driver, server, database, uid, pwd)
            )
        logging.info("Connection string : %s", connection_string)

        return pyodbc.connect(connection_string)

    def executeQuery(connection, query, parameters):
        response = []
        curs = connection.cursor()
        for data in curs.execute(query, parameters).fetchall():
            response.append(data)
        res = database.alignData(response)
        return res

    def alignData(data):
        res = []
        for rec in data:
            map = {
                "E": rec.employeeId,
                "T": formatDatetime(str(rec.eventTime)),
                "I": rec.isCheckin,
            }
            res.append(map)
        return res

    def formatDynamicTable(query):
        monthSign = "*M"
        yearSign = "*Y"
        # month = "{0:0=2d}".format(now.month)
        month = now.month
        year = now.year
        if monthSign in query or yearSign in query:
            return query.replace(monthSign, str(month)).replace(yearSign, str(year))
        else:
            return query

    def closeDB(connection):
        connection.close()


# <-

# -> config functions


class config:
    def readIni(filename="config.ini"):
        configParser.read(filename)
        return configParser

    def updateIni(config, section, option, value, filename="config.ini"):
        config[section][option] = value

        with open(filename, "w") as configfile:
            config.write(configfile)


# <-
