from time import sleep
import json


def add_cookies(driver, cookies_file):
    try:
        with open(cookies_file, "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print(f"Cookies file '{cookies_file}' not found. Proceeding without cookies.")


def get_available_internship_offers(driver, selector):
    internship_offers = driver.find_elements(selector[0], selector[1])
    print(f"Found {len(internship_offers)} internship offers")
    return internship_offers


def extract_internship_overview(internship, index):
    try:
        org = internship.find_element("css selector", "td:nth-child(1)").text
        addr = internship.find_element("css selector", "td[data-title='Adres']").text
        muni = internship.find_element("css selector", "td[data-title='Gemeente']").text
        title = internship.find_element(
            "css selector", "td[data-title='Titel opdracht']"
        ).text
        typ = internship.find_element(
            "css selector", "td[data-title='Type opdracht']"
        ).text
        tags = [
            t.strip()
            for t in internship.find_element(
                "css selector", "td[data-title='Kernwoorden']"
            ).text.split("; ")
            if t.strip()
        ]

        data = {
            "id": index + 1,
            "organization": org,
            "address": addr,
            "municipality": muni,
            "title": title,
            "type": typ,
            "tags": tags,
        }

        print(
            f"Internship #{index+1}\nOrganization: {org}\nAddress: {addr}\nMunicipality: {muni}\nTitle: {title}\nType: {typ}\nTags: {tags}\n{'-'*30}"
        )
        return data
    except Exception as e:
        print(f"Error processing row #{index+1}: {e}")
        return None


def extract_internship_details(driver, internship):
    try:
        btn = internship.find_element("css selector", "td[data-title='Info'] a")
        btn.click()
        sleep(0.5)

        modal = driver.find_element("css selector", ".modal-content")
        # website fallback
        try:
            website = modal.find_element(
                "xpath",
                "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/p/a",
            ).text
        except Exception:
            website = modal.find_element(
                "xpath",
                "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/p",
            ).text

        employees = modal.find_element("xpath", '//*[@id="aantalwerknemers"]').text
        it_employees = modal.find_element("xpath", '//*[@id="aantalinformatici"]').text
        contact_name = modal.find_element("xpath", '//*[@id="naam"]').text
        contact_email = modal.find_element("xpath", '//*[@id="email"]').text
        contact_gsm = modal.find_element("xpath", '//*[@id="gsm"]').text
        contact_tel = modal.find_element("xpath", '//*[@id="telefoon"]').text
        profile = modal.find_element("xpath", '//*[@id="profielStudent"]').text
        description = modal.find_element(
            "xpath", '//*[@id="omschrijvingStageopdracht"]'
        ).text

        # documents
        try:
            doc_container = modal.find_element(
                "xpath",
                "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[4]/div[2]/div[2]",
            )
            if "Geen documenten bewaard" in doc_container.text:
                extras = []
            else:
                extras = [
                    {"text": a.text, "url": a.get_attribute("href")}
                    for a in doc_container.find_elements("xpath", ".//a")
                ]
        except Exception:
            print("Could not extract document information")
            extras = []

        data = {
            "website": website,
            "employees_count": employees,
            "it_employees_count": it_employees,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "contact_gsm": contact_gsm,
            "contact_telephone": contact_tel,
            "internship_profile": profile,
            "internship_description": description,
            "extra_documents": extras,
        }

        close_btn = driver.find_element(
            "css selector",
            ".modal-lg > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)",
        )
        close_btn.click()
        return data
    except Exception as e:
        print(f"Error extracting details: {e}")
        return None
