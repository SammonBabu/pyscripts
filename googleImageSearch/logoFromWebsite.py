import requests, re, json,csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except Exception as e:
        print(e)
        return False

def src_finder(child_soup):
    src = ""
    error = ""
    srcList = []
    for i in child_soup:
        string = str(i)
        try:
            if src == "":
                try:
                    src = re.search('src="(.+?)"',string).group(1) #<h1><img src="a.jpeg">
                except Exception as e:
                    error = e
                    src = ""         
            if src == "":
                try:
                    src = re.search('srcset="(.+?)"',string).group(1)
                except Exception as e:
                    error = e
                    src = ""
        except Exception as e:
            error = e
            print (e)
            src = ""
        srcList.append(src)
    if srcList == ['']:
        return []
    if srcList != []:
        srcList = list(filter(None, srcList))
    return srcList

def logo_parser(URL):
    try:

        headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
                    }
        page = requests.get(URL,headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")
        regex = re.compile('.*logo.*',re.IGNORECASE)
        regex2 = re.compile('.*icon.*',re.IGNORECASE)
        regex3 = re.compile('.*brand.*',re.IGNORECASE)
        logo = ""
        divLogo_soup =soup.find_all('div', {'class': regex})
        divBrand_soup =soup.find_all('div', {'class': regex3})
        imgLogo_soup =soup.find_all('img', {'src': regex})
        imgLogoAlt_soup =soup.find_all('img', {'alt': regex})
        aLogo_soup =soup.find_all('a', {'class': regex})
        aHrefLogo_soup =soup.find_all('a', {'href': regex})
        linkIcon_soup = soup.find_all("link",{'rel': regex2})
        allClassLogo_soup = soup.find_all(True, {'class': regex})
        allClassBrand_soup = soup.find_all(True, {'class': regex3})
        allClassIcon_soup = soup.find_all(True, {'class': regex2})
        getSrcList = []
        if getSrcList == []:
            getSrcList = src_finder(imgLogo_soup)
            print("imgLogo_soup")
        if getSrcList == []:
            getSrcList = src_finder(divLogo_soup)
            print("divLogo_soup")
        if getSrcList == []:
            getSrcList = src_finder(divBrand_soup)
            print("divBrand_soup")
        if getSrcList == []:
            getSrcList = src_finder(aHrefLogo_soup)
            print("aHrefLogo_soup")
        if getSrcList == []:
            getSrcList = src_finder(aLogo_soup)
            print("aLogo_soup")
        if getSrcList == []:
            getSrcList = src_finder(imgLogoAlt_soup)
            print("imgLogoAlt_soup")
        if getSrcList == []:
            getSrcList = src_finder(allClassLogo_soup)
            print("allClass_soup")
        if getSrcList == []:
            getSrcList = src_finder(allClassBrand_soup)
            print("allClassBrand_soup")
        if getSrcList == []:
            src = ""
            error = ""
            srcList = []
            for i in linkIcon_soup:
                string = str(i)
                try:
                    src = re.search('href="(.+?)"',string).group(1)
                except Exception as e:
                    error = e
                    src = ""
                    print(error)
                srcList.append(src)
            if srcList == ['']:
                srcList == []
            if srcList != []:
                srcList = list(filter(None, srcList))
            getSrcList = srcList
            print("linkIcon_soup")
        if getSrcList == []:
            getSrcList = src_finder(allClassIcon_soup)
            print("allClassIcon_soup")
        if getSrcList != []:
            if getSrcList[0][0:2] == "//":
                # getSrcList[0] = re.sub('//+','', getSrcList[0])
                getSrcList[0] = "https:"+ getSrcList[0]
            if getSrcList[0][0] == "/" or getSrcList[0][0] == ".":
                if URL.endswith('/'):
                    URL = URL[:-1]
                getSrcList[0]=URL+getSrcList[0]
            if uri_validator(getSrcList[0]) == False:
                if URL.endswith('/'):
                    URL = URL[:-1]
                getSrcList[0]=URL+"/"+getSrcList[0]
            logo = getSrcList[0]
        else:
            logo ="logo not found"
            
        # print(urlVal)
        # parsed_logo.append([URL,logo])
    except Exception as e:
        logo = e
    return logo

x = "https://orgenza.in/"
try:
    logo = logo_parser(x)
except:
    logo = "logo not found"

print(logo)