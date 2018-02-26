# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import csv


def getHtml(url):
    try:
        html = urlopen(url)
    except:
        result = {"error": "E001_HTTPError"}
        return result

    try:
        Html = BeautifulSoup(html.read(), "html.parser")
        result = {"error": "OK",
                  "data": Html}
        return result
    except:
        result = {"error": "E002_HTTPParsing Error"}
        return result


def getCompany(htmlMeta, yyyymm):
    if htmlMeta["error"].startswith("OK"):
        try:
            data = htmlMeta["data"]
            table = data.find("table", {"class": "public_recruit_calendar"})
            companyMeta = table.findAll("div", {"class": "more-data"})
        except:
            result = {"error": "E003_AttributeError01(table not found)"}
            return result

        temp = []

        for i in companyMeta:
            try:
                day = i.find("span", {"class": "date"}).get_text()
                startDate = yyyymm+"-"+str(day)
                startDate = datetime.strptime(startDate, "%Y-%m-%d")
            except:
                startDate = "E004_AttributeError02(startDate not found)"

            companyLists = i.ol.findAll("li")

            for i in companyLists:
                companyList = i.find("a", {"class": "tit"})
                href = "http://www.saramin.co.kr" + str(companyList.attrs["href"])
                name = companyList.get_text()
                data = {"startDate": startDate,
                        "href": href,
                        "name": name}
                temp.append(data)

        result = {"error": "OK",
                  "data": temp}
        return result

    else:
        result = htmlMeta
        return result


def getCompanyDetail(htmlMeta):
    data = htmlMeta
    try:
        jobTitle = data.find("div", {"class": "job_title"})
        for child in jobTitle.find_all("div"):
            child.decompose()
        jobTitle = jobTitle.get_text()
    except:
        jobTitle = "E005_AttirubteError03(jobTitle not found)"

    try:
        finishDate = data.find("div", {"class": "company_date"}).p
        finishDate = finishDate.get_text()
        finishDate = datetime.strptime(finishDate[:10], "%Y.%m.%d")
        # if finishDate.find_all("span") is not None:
        #     for child in finishDate.find_all("span"):
        #         child.decompose()
        #     finishDate = finishDate.get_text()
        #     finishDate = datetime.strptime(finishDate[:5], "%m/%d")
        # else:
        #     finishDate = finishDate.get_text()
        #     finishDate = datetime.strptime(finishDate[:10], "%Y.%m.%d")
    except:
        finishDate = "E006_AttributeError04(finishDate not found)"

    try:
        salary = data.find("div", {"class": "section_salary"})
        salary = salary.find("li", {"class": "last"}).find("span", {"class" : "amount"}).strong
        salary = salary.get_text()
    except:
        salary = "E007_AttributeError05(salary not found)"

    data = {"jobTitle": jobTitle,
            "finishDate": finishDate,
            "salary": salary}
    result = {"error": "OK",
              "data": data}
    return result


def getData(url, yyyymm):
    try:
        html = urlopen(url)
    except HTTPError as e:
        result = "Error: HTTPError"
        return result

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        table = bsObj.find("table", {"class": "public_recruit_calendar"})
        companyMeta = table.findAll("div", {"class": "more-data"})
        result = []

        for i in companyMeta:
            day = i.find("span", {"class": "date"}).get_text()
            startDate = yyyymm+"-"+str(day)
            startDate = datetime.strptime(startDate, "%Y-%m-%d")
            companyList = i.ol.findAll("li")
            try:
                for i in companyList:
                    obj = i.find("a", {"class": "tit"})
                    href = "http://www.saramin.co.kr"+str(obj.attrs["href"])
                    name = obj.get_text()
                    result.append({"startDate": startDate, "href": href, "name": name})
            except:
                result = "Error: AttributeError_01"
                return result

        return result
    except AttributeError as e:
        result = "Error: AttributeError_02"
        return result

    return result


def getCompanyData(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        result = "Error: HTTPError"
        return result

    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        jobTitle = bsObj.find("div", {"class": "job_title"})
        for child in jobTitle.find_all("div"):
            child.decompose()
        jobTitle = jobTitle.get_text()
        finishDate = bsObj.find("div", {"class": "company_date"}).p.get_text()
        finishDate = datetime.strptime(finishDate[:10],"%Y.%m.%d")
        result = {"jobTitle": jobTitle, "finishDate": finishDate}
        return result
    except AttributeError as e:
        result = "Error: AttributeError_03"
        return result


url = "http://www.saramin.co.kr/zf_user/calendar"
param = {"cal_dt": ["2013-01", "2013-02", "2013-03", "2013-04", "2013-05", "2013-06",
                    "2013-07", "2013-08", "2013-09", "2013-10", "2013-11", "2013-12",
                    "2014-01", "2014-02", "2014-03", "2014-04", "2014-05", "2014-06",
                    "2014-07", "2014-08", "2014-09", "2014-10", "2014-11", "2014-12",
                    "2015-01", "2015-02", "2015-03", "2015-04", "2015-05", "2015-06",
                    "2015-07", "2015-08", "2015-09", "2015-10", "2015-11", "2015-12",
                    "2016-01", "2016-02", "2016-03", "2016-04", "2016-05", "2016-06",
                    "2016-07", "2016-08", "2016-09", "2016-10", "2016-11", "2016-12",
                    "2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06",]}

output = []

for i in param['cal_dt']:
    yyyymm = i

    http_url = url+"?"+"cal_dt="+yyyymm+"&"+"cal_kind%5B%5D=start&up_cd%5B%5D=4&company_scale_calendar%5B%5D=scalecd001"
    htmlMeta = getHtml(http_url)
    result = getCompany(htmlMeta, yyyymm)
    if result["error"].startswith("OK"):
        for i in result["data"]:
            htmlurl = i["href"]
            data = getHtml(htmlurl)
            if data["error"].startswith("OK"):
                html = data["data"]
                temp = getCompanyDetail(html)
                temp_ = temp["data"]
                i["jobTitle"] = temp_["jobTitle"]
                i["finishDate"] = temp_["finishDate"]
                i["salary"] = temp_["salary"]
            else:
                i["jobTitle"] = "Error: Urlopen error"
                i["finishDate"] = "Error: Urlopen error"
                i["salary"] = "Error: Urlopen error"
        print(result["data"])
        output = output + result["data"]

    else:
        print(result["error"])



# csv 파일 읽고 쓰기
fieldnames = ["name", "jobTitle", "startDate", "finishDate", "href", "salary"]
with open("/Users/k/Desktop/crawl_proj/result.csv", "w", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(output)

#
# for i in param['cal_dt']:
#     yyyymm = i
#     # 기업 : 대기업, 매출1000대기업,
#     # 업종 : {up_cd: 3-IT, 4-금융}
#     http_url = url+"?"+"cal_dt="+yyyymm+"&"+"cal_kind%5B%5D=start&up_cd%5B%5D=4&company_scale_calendar%5B%5D=scalecd001&company_scale_calendar%5B%5D=scalecd002"
#     result = getData(http_url, yyyymm)
#     if result == None:
#         print("None")
#     else:
#
#         for i in result:
#             if i["href"].startswith("http://www.saramin.co.kr/zf_user"):
#                 try:
#                     newUrl = i["href"]
#                     newResult = getCompanyData(newUrl)
#                     i["jobTitle"] = newResult["jobTitle"]
#                     i["finishDate"] = newResult["finishDate"]
#                 except:
#                     i["jobTitle"] = "Error: Urlopen error"
#                     i["finishDate"] = "Error: Urlopen error"
#             else:
#                 i["jobTitle"] = None
#                 i["finishDate"] = None
#         print(result)
#         output = output + result
#
# # csv 파일 읽고 쓰기
# fieldnames = ["name", "jobTitle", "startDate", "finishDate", "href"]
# with open("/Users/k/Desktop/crawl_proj/result.csv", "w", encoding="utf-8") as f:
#     w = csv.DictWriter(f, fieldnames=fieldnames)
#     w.writeheader()
#     w.writerows(output)

