import json
import requests
from bs4 import BeautifulSoup
import time
import openai
from dotenv import load_dotenv
import tiktoken

load_dotenv()
request_number = 0
client = openai.OpenAI()
model = "gpt-4o-mini"
output_token_number = 0
input_token_number = 0

def send_to_openai(job_data):
    global request_number
    global input_token_number
    request_number += 1
    client = openai.OpenAI()
    model = "gpt-4o-mini"
    if request_number == 3:
        time.sleep(120)
        request_number = 0
    if output_token_number + input_token_number >= 50000:
        time.sleep(120)

    prompt = f"""
You are a data extraction assistant. Given this job description:

{job_data["content_section"]}

Analyze the description and extract all the skills required for the position.

### **Output Format:**  
Return a **JSON object** with the following structure:

{{
    "company_name": "{job_data['company_name']}",
    "job_title": "{job_data['job_name']}",
    "required_skills": {{
        "soft_skills": ["List of soft skills"],
        "hard_skills": {{
            "technical_skills": ["List of technical skills"],
            "tools": ["List of specific tools, software, frameworks, or technologies required"]
        }}
    }}
}}

### **Extraction Guidelines:**
1. **Soft Skills:**  
   - Extract all **behavioral, interpersonal, and problem-solving** skills.
   - Examples: communication, leadership, adaptability, time management.

2. **Hard Skills:**  
   - **Technical Skills:** Extract all domain-specific **expertise and competencies**.  
     - Examples: programming languages, engineering principles, financial analysis, etc.
   - **Tools:** Extract a list of all **software, platforms, frameworks, or technologies** mentioned.  
     - Examples: Python, Excel, Salesforce, Kubernetes, AWS.

### **Important Notes:**
- Ensure the extraction is **as exhaustive as possible**.
- Only include **relevant** skills that are explicitly or implicitly required.
- Preserve **specific terminology** used in the job description.

Now, extract and return the JSON object.
"""

    completion = client.chat.completions.create(
        model=model,
        messages = [
            {
                "role":"user",
                "content":prompt
            }
        ]
    )
    input_token_number += completion.usage.completion_tokens
    print(input_token_number)
    print(completion.choices[0].message.content)

def check_input_token_number(job_data):
    global output_token_number
    encoding = tiktoken.encoding_for_model(model)
    token_number = len(encoding.encode(job_data["content_section"]))
    output_token_number += token_number
    print(output_token_number)
    send_to_openai(job_data)


def get_job_datas(url):
    global output_token_number
    time.sleep(5)
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")
    company_name = soup.find("span",class_="bkXoKy")
    content_section = soup.find("div",id="the-position-section")
    job_name = soup.find("h2", class_="ELqnp")
    job_data = {
        "company_name": company_name.text if company_name else None,
        "content_section": content_section.text if content_section else None,
        "job_name": job_name.text if job_name else None
    }
    # print(job_data["content_section"])
    check_input_token_number(job_data)
    # send_to_openai(job_data)


def get_job_url(response):
    jobs_offer = response.json()["results"][0]["hits"]
    for job in jobs_offer:
        url = f"https://www.welcometothejungle.com/fr/companies/{job['organization']['slug']}/jobs/{job['slug']}"
        get_job_datas(url)
        break

def request_data():
    with open("payload.json", "r") as file:
        data = json.load(file)  

    request_payload = data

    request_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "10888",
        "Host": "csekhvms53-dsn.algolia.net",
        "Origin": "https://www.welcometothejungle.com",
        "Referer": "https://www.welcometothejungle.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "x-algolia-api-key": "4bd8f6215d0cc52b26430765769e65a0",
        "x-algolia-application-id": "CSEKHVMS53"
    }

    response = requests.post("https://csekhvms53-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.20.0)%3B%20Browser&search_origin=job_search_client",
        headers=request_headers,
        json=request_payload,
    )
    
    get_job_url(response)

request_data()