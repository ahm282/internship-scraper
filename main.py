import json
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, PORTAL_URL, COOKIES_FILE
from selenium_setup import create_driver
from extractors import (
    add_cookies,
    get_available_internship_offers,
    extract_internship_overview,
    extract_internship_details,
)


def main():
    driver = create_driver()
    driver.get(BASE_URL)

    add_cookies(driver, COOKIES_FILE)
    driver.refresh()

    login_button = driver.find_element(By.ID, "BodySection_hlnkStudentenportaal")
    login_button.click()
    driver.get(PORTAL_URL)

    # select period
    period = driver.find_element(By.ID, "BodySection_ddlJaarplanning")
    period.click()
    period.find_element(By.XPATH, ".//option[2]").click()
    driver.implicitly_wait(5)

    # paging
    select_pages = driver.find_element(
        By.XPATH, '//*[@id="BodySection_ddlPagingPagina"]'
    )
    pages = [
        opt.text
        for opt in select_pages.find_elements(By.TAG_NAME, "option")
        if opt.text
    ]
    print(f"Pages available: {pages}")

    all_internships = []
    for idx, page in enumerate(pages):
        print(f"Processing page {page} ({idx+1}/{len(pages)})")
        # change page
        try:
            wait = WebDriverWait(driver, 10)
            pages_el = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="BodySection_ddlPagingPagina"]')
                )
            )
            pages_el.click()
            driver.find_element(
                By.XPATH,
                f"//select[@id='BodySection_ddlPagingPagina']/option[text()='{page}']",
            ).click()
            sleep(1)
        except Exception:
            print("Stale reference, retrying page selection")
            continue

        rows = get_available_internship_offers(
            driver, (By.CSS_SELECTOR, "#tblAanbod > tbody > tr")
        )
        for i, row in enumerate(rows):
            try:
                overview = extract_internship_overview(row, len(all_internships))
                if overview:
                    all_internships.append(overview)
                    fresh_rows = driver.find_elements(
                        By.CSS_SELECTOR, "#tblAanbod > tbody > tr"
                    )
                    if i < len(fresh_rows):
                        details = extract_internship_details(driver, fresh_rows[i])
                        if details:
                            all_internships[-1].update(details)
            except Exception as e:
                print(f"Skipping internship #{i+1}: {e}")
                continue

        with open(f"output/internships_page_{idx+1}.json", "w") as f:
            json.dump(all_internships, f, indent=4)
        print(f"Saved {len(all_internships)} internships so far")

    with open("output/internships.json", "w") as f:
        json.dump(all_internships, f, indent=4)
    print(f"Successfully processed {len(all_internships)} internships")
    driver.quit()


if __name__ == "__main__":
    main()
