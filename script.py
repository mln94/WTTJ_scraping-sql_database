import requests
from bs4 import BeautifulSoup
import json
import time 
import re
datas = [{"company_count": 0},[]]
job_number = []
def txt_format():
    # with open('/Users/necib/Desktop/DEV/Scraping/WTTJ/data.json', 'w') as json_file:
    #     json.dump(objData, json_file, indent=4)
    for data in datas[1]:
        print(data["job_title"])
        with open("output.txt", "a") as file:
            # Write both variables on the same line
            file.write(f"\t{data['job_title']}\t{data['company_name']}\t{data['contract']}\t{data['location']}\t{data['salary']}\t{data['experience']}\t{data['place']}\t{data['date']}\t{data['employee']}\t{data['company_url']}\t{data['creation']}\n")

def get_job_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_title = soup.find_all("h2", class_=("ELqnp", "irtGov"))
    job_title = job_title[0].text
    # print(job_title)
    span_company_name = soup.find("span",class_="bkXoKy")
    if span_company_name:
        company_name = span_company_name.text
    else:
        company_name = span_company_name.next_sibling.text
    contract = (soup.find('i', attrs={"name": "contract"}).next_sibling.text)
    location = soup.find('i', attrs={"name": "location"}).find_next('span').find_next('span').text
    salary = soup.find('i', attrs={"name": "salary"}).find_next('span').next_sibling.text
    suitcases = soup.find_all('i', attrs={"name": "suitcase"})
    for suitcase in suitcases:
        if suitcase.find_next('span').text == "Expérience : ":
            experience = suitcase.find_next('span').next_sibling.text
        else:
            experience = "none"
    place = soup.find('i', attrs={"name": "remote"}).find_next('span').text
    date = soup.find_all("time")
    date = date[0].text
    # print(date)
    sector = soup.find('i', attrs={"name": "tag"})
    if sector:
        sector = sector.find_next('span').text
    else:
        sector = "none"
    department = soup.find('i', class_="fMfBBJ")
    if department:
        employee = department.find_next('span').text
        employee = re.findall(r'\d+', employee)
        employee = employee[0]
    else:
        employee = "none"
    company_url = soup.find("li", class_="gPFRIa")
    if company_url:
        company_url = company_url.find_next("a").get("href")
    else:
        company_url = "none"
    print(company_url)
    turnover = soup.find('i', attrs={"name": "euro_currency"})
    if turnover:
        turnover = turnover.find_next('span').text
    else:
        turnover = "none"
    creation = soup.find('i', class_="cnlZHK").find_next('span').text
    creation = re.findall(r'\d+', creation)
    creation = int(creation[0])
    # print(creation)
    datas[1].append({
        "job_title": job_title,
        "company_name": company_name,
        "contract": contract,
        "location": location,
        "salary": salary,
        "experience": experience,
        "place": place,
        "date": date,
        "employee": employee,
        "company_url": company_url,
        "creation": creation,
    })
    # print(objData)

# ajouter jobtitle ligne par ligne sur un fichier text et rajouter le fichier text dans la bdd
def get_job_links(response):
    jobs = (response.json()["results"][0]["hits"])
    # company_slug = jobs["organization"]["slug"]
    # job_slug = jobs["slug"]
    # url = f"https://www.welcometothejungle.com/fr/companies/{company_slug}/jobs/{job_slug}"
    # job_number.append(url)
    # get_job_data(url)
    print(len(jobs))
    datas[0]["company_count"] = len(jobs)
    for job in jobs:
        company_slug = job["organization"]["slug"]
        job_slug = job["slug"]
        url = f"https://www.welcometothejungle.com/fr/companies/{company_slug}/jobs/{job_slug}"
        job_number.append(url)
        get_job_data(url)
    txt_format()
    
def requests_data():
    form_data = {"requests":[{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"attributesToHighlight=%5B%22name%22%5D&attributesToRetrieve=%5B%22*%22%5D&clickAnalytics=true&hitsPerPage=300&maxValuesPerFacet=999&analytics=true&enableABTest=true&userToken=7e3d2cb557&analyticsTags=%5B%22page%3Ajobs_index%22%2C%22language%3Afr%22%5D&facets=%5B%22benefits%22%2C%22organization.commitments%22%2C%22contract_type%22%2C%22contract_duration_minimum%22%2C%22contract_duration_maximum%22%2C%22has_contract_duration%22%2C%22education_level%22%2C%22has_education_level%22%2C%22experience_level_minimum%22%2C%22has_experience_level_minimum%22%2C%22organization.nb_employees%22%2C%22organization.labels%22%2C%22salary_yearly_minimum%22%2C%22has_salary_yearly_minimum%22%2C%22salary_currency%22%2C%22followedCompanies%22%2C%22language%22%2C%22new_profession.category_reference%22%2C%22new_profession.sub_category_reference%22%2C%22remote%22%2C%22sectors.parent_reference%22%2C%22sectors.reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&page=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_promoted","params":"attributesToHighlight=%5B%22name%22%5D&attributesToRetrieve=%5B%22*%22%5D&clickAnalytics=true&hitsPerPage=200&maxValuesPerFacet=999&analytics=true&enableABTest=true&userToken=7e3d2cb557&analyticsTags=%5B%22page%3Ajobs_index%22%2C%22language%3Afr%22%5D&facets=%5B%5D&filters=(%22offices.country_code%22%3A%22FR%22)%20AND%20is_boosted%3Atrue&page=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22benefits%22%2C%22organization.commitments%22%2C%22contract_type%22%2C%22contract_duration_minimum%22%2C%22contract_duration_maximum%22%2C%22has_contract_duration%22%2C%22education_level%22%2C%22has_education_level%22%2C%22experience_level_minimum%22%2C%22has_experience_level_minimum%22%2C%22organization.nb_employees%22%2C%22organization.labels%22%2C%22salary_yearly_minimum%22%2C%22has_salary_yearly_minimum%22%2C%22salary_currency%22%2C%22followedCompanies%22%2C%22language%22%2C%22new_profession.category_reference%22%2C%22new_profession.sub_category_reference%22%2C%22remote%22%2C%22sectors.parent_reference%22%2C%22sectors.reference%22%5D&filters=&hitsPerPage=0"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22benefits%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.commitments%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_type%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A1%20TO%203%20OR%20contract_duration_maximum%3A1%20TO%203%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A4%20TO%206%20OR%20contract_duration_maximum%3A4%20TO%206%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A7%20TO%2012%20OR%20contract_duration_maximum%3A7%20TO%2012%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A13%20TO%2024%20OR%20contract_duration_maximum%3A13%20TO%2024%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_minimum%22%5D&filters=contract_duration_minimum%3A25%20TO%2036%20OR%20contract_duration_maximum%3A25%20TO%2036%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22contract_duration_maximum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22has_contract_duration%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22education_level%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22has_education_level%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A0%20TO%201%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A1%20TO%203%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A3%20TO%205%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%3A5%20TO%2010%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22experience_level_minimum%22%5D&filters=experience_level_minimum%20%3E%3D%2010%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22has_experience_level_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A0%20TO%2015%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A15%20TO%2050%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A50%20TO%20250%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%3A250%20TO%202000%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.nb_employees%22%5D&filters=organization.nb_employees%20%3E%3D%202000%20AND%20(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22organization.labels%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22salary_yearly_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22has_salary_yearly_minimum%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22salary_currency%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22followedCompanies%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22language%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22new_profession.category_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22new_profession.sub_category_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22remote%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22sectors.parent_reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"},{"indexName":"wttj_jobs_production_fr_published_at_desc","params":"analytics=false&facets=%5B%22sectors.reference%22%5D&filters=(%22offices.country_code%22%3A%22FR%22)&hitsPerPage=0&query=growth%20marketing"}]}
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "18",
        "Content-Type": "application/json",
        "Host": "csekhvms53-dsn.algolia.net",
        "Origin": "https://www.welcometothejungle.com",
        "Referer": "https://www.welcometothejungle.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "x-algolia-api-key": "4bd8f6215d0cc52b26430765769e65a0",
        "x-algolia-application-id": "CSEKHVMS53"
    }
    response = requests.post("https://csekhvms53-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.20.0)%3B%20Browser&search_origin=job_search_client",
        headers=headers,
        json=form_data,
    )
    # with open('/Users/necib/Desktop/DEV/Scraping/WTTJ/response.json', 'w') as json_file:
    #     json.dump(response.json(), json_file, indent=4)
    get_job_links(response)

def main():
    requests_data()

main()