import requests
import socket
import yaml
import json

httpProxy = {
    'http':  'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

def getPorxyCountry(index, proxy):
    country = "未知地区"
    try:
        ip = socket.gethostbyname(proxy['server'])
        data = requests.get(f"http://ip.plyz.net/ip.ashx?ip={ip}", proxies=httpProxy).text
        if(len(data) != 0):
            country = data.split("|")[1].split()[0]
    except Exception as e:
        print(e)

    print(f"节点{index}: {proxy['server']} {country}")
    return country

def createGroup(name, groupType, proxies):
    allType = ['select', 'load-balance', 'url-test', 'fallback']
    assert(groupType in allType)

    group = {
        "name"     : name,
        "type"     : groupType,
        "proxies"  : proxies,
    }

    if(groupType != "select"):
        group['url'] = "https://twitter.com/favicon.ico"
        group["interval"] = 300

    return group

def createLocationProxyGroup(proxies):
    print("按照ip地址查询节点所属地区")

    location = dict()
    for index, proxy in enumerate(proxies):
        country = getPorxyCountry(index+1, proxy)
        countryGroup = location[country] if (country in location) else createGroup(country, "url-test", [])
        proxy['name'] = f"{country}-{len(countryGroup['proxies']) + 1}"
        countryGroup['proxies'].append(proxy['name'])

        location[country] = countryGroup

    return location

if __name__ == "__main__":
    with open("list.yaml", encoding='utf8') as fp:
        listFile = yaml.load(fp.read(), Loader=yaml.FullLoader)
        createLocationProxyGroup(listFile['proxies'])