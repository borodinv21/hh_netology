import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def find_vacancies():
    user_agent = fake_useragent.UserAgent()
    hh_link = f'https://chelyabinsk.hh.ru/search/vacancy?text=python&area=1&area=2'
    response = requests.get(hh_link, headers={'user-agent': user_agent.random})
    soup = BeautifulSoup(response.content, "lxml")
    vacancies_cards = soup.find_all("div", attrs={"class": "vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS"})

    result_vacancies = []
    for vacancy_card in vacancies_cards:
        vacancy_link = vacancy_card.find("a")["href"]

        vacancy_response = requests.get(vacancy_link, headers={'user-agent': user_agent.random})
        vacancy_soup = BeautifulSoup(vacancy_response.content, "lxml")

        print(vacancy_link)
        vacancy_description = vacancy_soup.find("div", class_="vacancy-description")

        if 'django' in vacancy_description.text.lower() or 'flask' in vacancy_description.text.lower():
            try:
                salary = vacancy_card.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh").text
            except:
                salary = "Не указано"

            company_name = vacancy_card.find("span", class_="company-info-text--vgvZouLtf8jwBmaD1xgp").text
            city = vacancy_card.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni").text

            vacancy_info = {
                "link": vacancy_link,
                "salary": salary,
                "company_name": company_name,
                "city": city
            }

            result_vacancies.append(vacancy_info)

    return result_vacancies



if __name__ == "__main__":
    vacancies = find_vacancies()

    with open('data.json', 'w') as file:
        json.dump(vacancies, file, ensure_ascii=False)


