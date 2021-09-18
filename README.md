# 'CMS Attendance' - Integration Middleware

The objective of this middleware is to sync attendance data from Bio-Metric device's database to Contract Management System (CMS by BuildHr)

## Introduction

An attendance management tool is a positive strategy to magnify productivity in any organization. 'CMS Attendance' offers attendance device integrations that aid in accurate attendance management.

You can integrate your attendance device with CMS Attendance by making use of APIs. In order to sync attendance entries of employees in CMS attendance, it is required to have certain pre-requisites captured in the bio-metric device's database.

## Getting Started with Pre-requisites

Integration between Bio-metric device's database & CMS Attendance  is achieved by configuration of a middleware using **Python and ODBC drivers**.

Using this middleware, CMS can be integrated with any of these databases: **MS SQL Server, MS Access and MY SQL**.

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
   - Go to [Python Downloads](https://www.python.org/downloads/windows/) and download the latest stable release of **Windows installer (64-bit)**
   - Click the downloaded file and choose **Recommended Installation** in Python installation window.
   - Then, click **Finish** to complete Python installation
   - Right click the **connect.pyw** file and click **opens with...**
   - Then click **Look for another app in this PC**
   - Go to the Python's `.exe` file and pick that then just click **OK** in the Opens with.. pop-up window.

> _**Note:** **Python** should be **v3.6 and above**_

2. **Install Python Packages**

   - Open _cmd_ using `Windows search bar` or `⊞ + R`.
   - Type `pip install pyodbc requests schedule python-dotenv`  command in **Command Prompt** and click **Enter**

3. ODBC Driver
   - Download ODBC driver using the following hyperlinks [MS Access](https://www.microsoft.com/en-in/download/confirmation.aspx?id=13255), [MySQL](https://dev.mysql.com/get/Downloads/Connector-ODBC/8.0/mysql-connector-odbc-8.0.25-winx64.msi) and [MS SQL](https://go.microsoft.com/fwlink/?linkid=2156851)
   - Click the downloaded file.
   - Click **Next** on every pop-up and then click on **Install**

> _[Learn more](https://www.microsoft.com/en-in/download/details.aspx?id=13255) about MS Access ODBC Driver_

4. CMS Attendance
   - Download [CMS Attendance](https://github.com/BuildHR/BuildHr-CMS-Attendance) ZIP by clicking on the green color **Code** button in the top right corner of the page.

## Contributor

- **[SS Subash](https://github.com/sssubash)** - _Developer and Maintainer_

> _To raise any issue click on [Issues](https://github.com/BuildHR/BuildHr-CMS-Attendance/issues) tab of this repository._

> _To raise Questions, Ideas or Feedback click on [Discussions](https://github.com/BuildHR/BuildHr-CMS-Attendance/discussions) tab of this repository._
