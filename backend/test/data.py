import datetime

from infracheck.model.ITestResult import ITestResult

result: ITestResult = {
    "id": "",
    "pdf_link": "",
    "name": "",
    "description": "",
    "success_count": 0,
    "failure_count": 0,
    "error_count": 0,
    "total_count": 0,
    "message": "",
    "date": datetime.datetime.now(),
    "plugin_result": []
}
