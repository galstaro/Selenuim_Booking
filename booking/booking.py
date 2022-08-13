from selenium import webdriver
import os
import booking.constants as const
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/chromedriver_win32", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, "button[data-tooltip-text='בחירת סוג מטבע']")
        currency_element.click()
        selected_currency_element = self.find_element(
            By.CSS_SELECTOR,
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )

        selected_currency_element.click()

    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)

        first_result = self.find_element(By.CSS_SELECTOR, "li[data-i='0']")
        first_result.click()

    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(By.CSS_SELECTOR, f"td[data-date='{check_in_date}']")
        check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, f"td[data-date='{check_out_date}']")
        check_out_element.click()

    def select_adults(self, count):
        selection_element = self.find_element(By.ID, "xp__guests__toggle")
        selection_element.click()

        adults_default = self.find_element(By.CSS_SELECTOR, 'span[data-bui-ref="input-stepper-value"]')
        plus = self.find_element(By.CSS_SELECTOR, 'button[aria-label="הגדילו את מספר המבוגרים"]')
        minus = self.find_element(By.CSS_SELECTOR, 'button[aria-label="הקטינו את מספר המבוגרים"]')
        adults_default_number = int(adults_default.text)
        while adults_default_number != count:
            if adults_default_number < count:
                plus.click()
                adults_default_number += 1
            else:
                minus.click()
                adults_default_number -= 1

    def click_search(self):
        search_button = self.find_element(By.CLASS_NAME, 'js-sb-submit-text')
        search_button.click()

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4, 5)

    def report_results(self):
        hotel_boxes = self.find_element(By.CLASS_NAME,
                                        'd4924c9e74'
                                        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)
