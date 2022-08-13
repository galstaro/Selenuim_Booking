# booking filters after search
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.CSS_SELECTOR, '[data-filters-group="class"]')

        for star_value in star_values:
            star_child_element = star_filtration_box.find_element(By.CSS_SELECTOR,
                                                                  f'[data-filters-item="class:class={star_value}"]')
            star_child_element.click()
