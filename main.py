# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import (
#     ElementClickInterceptedException,
#     StaleElementReferenceException,
# )

# from time import sleep
# import dotenv
# import json


# def add_cookies(driver, cookies_file):
#     try:
#         with open(cookies_file, "r") as file:
#             cookies = json.load(file)
#             for cookie in cookies:
#                 driver.add_cookie(cookie)
#     except FileNotFoundError:
#         print(f"Cookies file '{cookies_file}' not found. Proceeding without cookies.")


# def get_available_internship_offers(driver, selector):
#     # Get all internship rows from the table
#     internship_offers = driver.find_elements(selector[0], selector[1])
#     print(f"Found {len(internship_offers)} internship offers")
#     return internship_offers


# def extract_internship_overview(internship, index):
#     """
#     Extract relevant information from an internship element.

#     Args:
#         internship: The WebElement representing the internship row
#         index: The index of the internship in the list

#     Returns:
#         dict: A dictionary containing the extracted internship details
#     """
#     try:
#         # Find elements relative to the current row
#         organization = internship.find_element("css selector", "td:nth-child(1)").text
#         address = internship.find_element("css selector", "td[data-title='Adres']").text
#         municipality = internship.find_element(
#             "css selector", "td[data-title='Gemeente']"
#         ).text
#         task_title = internship.find_element(
#             "css selector", "td[data-title='Titel opdracht']"
#         ).text
#         task_type = internship.find_element(
#             "css selector", "td[data-title='Type opdracht']"
#         ).text
#         tags = [
#             tag.strip()
#             for tag in internship.find_element(
#                 "css selector", "td[data-title='Kernwoorden']"
#             ).text.split("; ")
#             if tag.strip() != ""
#         ]

#         # Create a dictionary with extracted information
#         internship_data = {
#             "id": index + 1,
#             "organization": organization,
#             "address": address,
#             "municipality": municipality,
#             "title": task_title,
#             "type": task_type,
#             "tags": tags,
#         }

#         print(f"Internship #{index+1}")
#         print(f"Organization: {organization}")
#         print(f"Address: {address}")
#         print(f"Municipality: {municipality}")
#         print(f"Title: {task_title}")
#         print(f"Type: {task_type}")
#         print(f"Tags: {tags}")
#         print("-" * 30)

#         return internship_data

#     except Exception as e:
#         print(f"Error processing row #{index+1}: {e}")
#         return None


# def extract_internship_details(driver, internship):
#     """
#     Click on the internship details button and extract details from modal.

#     Args:
#         driver: The Selenium WebDriver instance
#         internship: The WebElement representing the internship row
#     """
#     try:
#         # Find the details button
#         details_button = internship.find_element(
#             "css selector", "td[data-title='Info'] a"
#         )

#         details_button.click()
#         sleep(0.5)

#         modal = driver.find_element("css selector", ".modal-content")

#         # Organization details
#         try:
#             website = modal.find_element(
#                 "xpath",
#                 "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/p/a",
#             ).text
#         except Exception as e:
#             website = modal.find_element(
#                 "xpath",
#                 "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/p",
#             ).text

#         employees_count = modal.find_element(
#             "xpath", '//*[@id="aantalwerknemers"]'
#         ).text
#         it_employees_count = modal.find_element(
#             "xpath", '//*[@id="aantalinformatici"]'
#         ).text

#         # Contact details
#         contact_name = modal.find_element("xpath", '//*[@id="naam"]').text
#         contact_email = modal.find_element("xpath", '//*[@id="email"]').text
#         contact_gsm = modal.find_element("xpath", '//*[@id="gsm"]').text
#         contact_telephone = modal.find_element("xpath", '//*[@id="telefoon"]').text

#         # Internship details
#         internship_profile = modal.find_element(
#             "xpath", '//*[@id="profielStudent"]'
#         ).text
#         internship_description = modal.find_element(
#             "xpath", '//*[@id="omschrijvingStageopdracht"]'
#         ).text

#         # Extra documents if available
#         try:
#             # First check if there are documents
#             doc_container = modal.find_element(
#                 "xpath",
#                 "/html/body/div[1]/form/div[7]/div[10]/div[2]/div/div/div[2]/div[4]/div[2]/div[2]",
#             )

#             # Check if the container contains the "no documents" message
#             if "Geen documenten bewaard" in doc_container.text:
#                 extra_documents = []
#             else:
#                 # Find all anchor tags with links
#                 doc_links = doc_container.find_elements("xpath", ".//a")
#                 extra_documents = []

#                 # Extract URL and text for each document
#                 for link in doc_links:
#                     extra_documents.append(
#                         {"text": link.text, "url": link.get_attribute("href")}
#                     )
#         except Exception as e:
#             print(f"Could not extract document information: {e}")
#             extra_documents = []

#         # Save as JSON
#         internship_data = {
#             "website": website,
#             "employees_count": employees_count,
#             "it_employees_count": it_employees_count,
#             "contact_name": contact_name,
#             "contact_email": contact_email,
#             "contact_gsm": contact_gsm,
#             "contact_telephone": contact_telephone,
#             "internship_profile": internship_profile,
#             "internship_description": internship_description,
#             "extra_documents": extra_documents,
#         }

#         # Close the modal
#         close_button = driver.find_element(
#             "css selector",
#             ".modal-lg > div:nth-child(1) > div:nth-child(1) > button:nth-child(1)",
#         )
#         close_button.click()

#         return internship_data

#     except Exception as e:
#         print(f"Error extracting details: {e}")
#         return None


# # Load environment variables from .env file
# dotenv.load_dotenv()

# # Set up the Chrome driver
# chrome_options = Options()
# chrome_options.binary_location = "/usr/bin/chromium"
# service = Service("chromedriver")
# driver = webdriver.Chrome(service=service, options=chrome_options)

# # Go to the desired URL
# driver.get("https://stages.thomasmore.be/")

# # Use cookies from a file
# add_cookies(driver, "cookies.json")

# # Refresh the page to apply cookies
# driver.refresh()

# # Get login button and click it
# login_button = driver.find_element("id", "BodySection_hlnkStudentenportaal")
# login_button.click()

# # Go to internship page
# driver.get(
#     "https://stages.thomasmore.be/Studentenportaal/Stagevoorkeur/Stagevoorkeur.aspx"
# )

# # Select period (select element -> first option)
# period_select = driver.find_element("id", "BodySection_ddlJaarplanning")
# period_select.click()
# period_option = period_select.find_element("xpath", ".//option[2]")
# period_option.click()
# driver.implicitly_wait(5)

# # Get the available pages once to know how many we need to process
# pages_select_element = driver.find_element(
#     "xpath", '//*[@id="BodySection_ddlPagingPagina"]'
# )
# pages_available = pages_select_element.find_elements("tag name", "option")
# pages_available = [page.text for page in pages_available if page.text != ""]
# print(f"Pages available: {pages_available}")

# # Process each internship offer
# all_internships = []

# # Loop through each page
# for page_number, page in enumerate(pages_available):
#     print(f"Processing page {page} ({page_number + 1}/{len(pages_available)})")

#     # Find the page dropdown element fresh each time
#     # This prevents the StaleElementReferenceException
#     try:
#         # Wait for the page select element to be available
#         wait = WebDriverWait(driver, 10)
#         pages_select_element = wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, '//*[@id="BodySection_ddlPagingPagina"]')
#             )
#         )

#         # Click the dropdown to show options
#         pages_select_element.click()

#         # Find and click the specific page option
#         page_option = driver.find_element(
#             "xpath",
#             f"//select[@id='BodySection_ddlPagingPagina']/option[text()='{page}']",
#         )
#         page_option.click()

#         # Wait for page to load
#         sleep(1)
#     except StaleElementReferenceException:
#         # If we get a stale element, retry with a fresh reference
#         print("Encountered stale element, refreshing reference...")
#         wait = WebDriverWait(driver, 10)
#         pages_select_element = wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, '//*[@id="BodySection_ddlPagingPagina"]')
#             )
#         )
#         pages_select_element.click()
#         page_option = driver.find_element(
#             "xpath",
#             f"//select[@id='BodySection_ddlPagingPagina']/option[text()='{page}']",
#         )
#         page_option.click()
#         sleep(1)

#     # Get all internship rows from the table
#     internship_offers_selector = ("css selector", "#tblAanbod > tbody > tr")
#     internship_offers = get_available_internship_offers(
#         driver, internship_offers_selector
#     )

#     for index, internship in enumerate(internship_offers):
#         try:
#             internship_data = extract_internship_overview(
#                 internship, len(all_internships)
#             )

#             if internship_data:
#                 all_internships.append(internship_data)

#                 # Extract detailed information - we need to re-find the row element
#                 # to avoid stale element references after clicking into details
#                 current_rows = driver.find_elements(*internship_offers_selector)
#                 if index < len(current_rows):
#                     fresh_internship = current_rows[index]
#                     internship_details = extract_internship_details(
#                         driver, fresh_internship
#                     )

#                     if internship_details and len(all_internships) > 0:
#                         all_internships[-1].update(internship_details)
#                     else:
#                         print(
#                             f"Skipping update for internship #{len(all_internships)} due to missing details"
#                         )

#                 sleep(0.5)
#         except StaleElementReferenceException:
#             print(
#                 f"Stale element encountered for internship #{index + 1} on page {page}, skipping..."
#             )
#             continue
#         except Exception as e:
#             print(f"Error processing internship #{index + 1} on page {page}: {str(e)}")
#             continue

#     # Save progress after each page
#     with open(f"internships_page_{page_number+1}.json", "w") as file:
#         json.dump(all_internships, file, indent=4)
#     print(
#         f"Saved progress after page {page}: {len(all_internships)} internships so far"
#     )

# # Save all internships to a JSON file
# with open("internships.json", "w") as file:
#     json.dump(all_internships, file, indent=4)

# # Print the total number of internships found
# print("Internships saved to internships.json")
# print(f"Successfully processed {len(all_internships)} internships")

# # Close the driver when done
# driver.quit()

#!/usr/bin/env python3
"""
Main script for the internship scraper.
This orchestrates the scraping process and uses the other modules.
"""
import os
import json
import dotenv
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_setup import setup_driver
from page_navigation import navigate_to_internships, get_available_pages
from internship_extractor import get_available_internship_offers, process_internships
from utils import save_json


def main():
    """Main function to run the internship scraper."""
    dotenv.load_dotenv()
    driver = setup_driver()

    try:
        # Add cookies before navigation
        from selenium_setup import add_cookies, verify_cookies

        cookie_success = add_cookies(driver, "cookies.json")

        if not cookie_success:
            print("Warning: Failed to add cookies, login might be required")
            # Give user a chance to manually login if needed
            print("Please login manually if prompted...")
            sleep(10)  # Wait a bit to allow manual intervention if needed
        else:
            # Double-check cookie status again after a successful add
            if not verify_cookies(driver):
                print(
                    "Warning: Cookie verification failed, authentication might not persist"
                )

        navigate_to_internships(driver)

        # Get available pages
        pages_available = get_available_pages(driver)

        # Process each internship offer
        all_internships = []

        # Create output directory if it doesn't exist
        if not os.path.exists("output"):
            os.makedirs("output")

        # Loop through each page
        for page_number, page in enumerate(pages_available):
            print(
                f"\n===== Processing page {page} ({page_number + 1}/{len(pages_available)}) ====="
            )

            # Try up to 3 times to navigate to the page
            success = False
            for attempt in range(3):
                if navigate_to_internships(driver, page):
                    success = True
                    break
                else:
                    print(f"Failed to navigate to page {page}, attempt {attempt+1}/3")
                    sleep(2)  # Wait before retrying

            if not success:
                print(
                    f"Failed to navigate to page {page} after multiple attempts, skipping..."
                )
                continue

            # Verify we're on the right page by checking the pagination dropdown
            try:
                dropdown = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.ID, "BodySection_ddlPagingPagina")
                    )
                )
                selected_option = dropdown.find_element(
                    By.CSS_SELECTOR, "option:checked"
                )
                if selected_option.text != page:
                    print(
                        f"Warning: Expected page {page}, but found {selected_option.text}"
                    )
            except Exception as e:
                print(f"Could not verify current page: {e}")

            # Get all internship rows from the table - wait longer for the table to load
            driver.implicitly_wait(10)
            internship_offers_selector = ("css selector", "#tblAanbod > tbody > tr")
            internship_offers = get_available_internship_offers(
                driver, internship_offers_selector
            )

            # Process internships on current page
            processed_internships = process_internships(
                driver, internship_offers, internship_offers_selector
            )
            all_internships.extend(processed_internships)

            # Save progress after each page
            save_json(all_internships, f"output/internships_page_{page_number+1}.json")
            print(
                f"Saved progress after page {page}: {len(all_internships)} internships so far"
            )

        # Save all internships to a JSON file
        save_json(all_internships, "output/internships.json")

        # Print the total number of internships found
        print("Internships saved to output/internships.json")
        print(f"Successfully processed {len(all_internships)} internships")

    except Exception as e:
        print(f"An error occurred in the main script: {e}")

    finally:
        # Close the driver when done
        driver.quit()


if __name__ == "__main__":
    main()
