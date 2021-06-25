# Attendance Device Integration with CMS Attendance

The goal of this CMS Attendance is to sync Bio-Metric Attendance data from databases to Contract Management System(CMS by BuildHr)

## Introduction

An attendance management tool is a positive strategy to magnify productivity in any organization. CMS Attendance offers attendance device integrations that aid in accurate attendance management.

You can integrate your attendance device with CMS Attendance by making use of APIs. In order to sync your device's attendance entries with your employee's attendance records in CMS, you need to have a common format between your device and your CMS Attendance account.

## Getting Started with Prerequisites

The biometric device with CMS is through the configuration of a plugin using **Python and ODBC drivers**.

Integration can be done with any of these databases: **MS SQL Server, MS Access and MY SQL**.

> _**Note:** The **data** from the biometric **should be automatically downloaded into the database**._

### Database Query Format

_Select employeeID, eventTime, isCheckin, downloadDate from Attendance_

- **employeeID** : Should be the same employee-id in CMS
- **eventTime** : Attendance In-punch and Out-punch
- **isCheckin** : 1/0 ( 1 denotes check-in and 0 denotes check-out)
- **downloadDate** : Date and Time at which the attendance data got pushed to database

> _**Note:** For **MS Access**, database should be available in the **local system**_

### Software installation

1. **Python**
   - From Microsoft Store
     - Go to [Python in Store](https://www.microsoft.com/en-in/search?q=python) and choose the _first_ one
     - Click on _Get_. Now open the browser dialog box with the message of Microsoft Store
     - Click on _Open in Microsoft Store_
     - Click on _Install_ in Microsoft Store
   - Others
     - Go to [Python Downloads](https://www.python.org/downloads/windows/) and download the latest stable release **Windows installer (64-bit)**
     - Click the download file then choose **Recommended Installation** in Python installation window.
     - After click **Finish** to complete Python installation

> _**Note:** **Python** should be **v3.6 and above**_

2. **Install Python Packages**

   - Open _cmd_ using `Windows search bar` or `⊞ + R`.
   - `pip install pyodbc requests schedule python-dotenv` this command in **Command Prompt**

3. ODBC Driver
   - Download ODBC driver using hyperlink on database. For [MS Access](https://www.microsoft.com/en-in/download/confirmation.aspx?id=13255), [MySQL](https://dev.mysql.com/downloads/file/?id=504545) and [MS SQL](https://go.microsoft.com/fwlink/?linkid=2156851)
   - Click next on every pop-up and then click on Install

> _[Learn more](https://www.microsoft.com/en-in/download/details.aspx?id=13255) about MS Access ODBC Driver_

4. CMS Attendance
   - Download [CMS Attendance](https://github.com/BuildHR/BuildHr-CMS-Attendance) ZIP using **Code** green button.

## Contributor

- **[SS Subash](https://github.com/sssubash)** - _Developer and Maintainer_

> _Raise issues on [Issues](https://github.com/BuildHR/BuildHr-CMS-Attendance/issues) of this repository_

> _Raise Questions, Suggestions or Feedback on [Discussions](https://github.com/BuildHR/BuildHr-CMS-Attendance/discussions) of this repository_
