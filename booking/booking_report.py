# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element: WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR,
                                                        '[data-testid="property-card"]'
                                                        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text

            hotel_price = deal_box.find_element(By.CSS_SELECTOR, '[data-testid="price-and-discounted-price"]')
            hotel_price = hotel_price.find_element(By.CSS_SELECTOR, "span[class='fcab3ed991 bd73d13072']").text

            try:
                hotel_score = deal_box.find_element(By.CSS_SELECTOR, '[data-testid="review-score"]')
                hotel_score = hotel_score.find_element(By.CSS_SELECTOR, "div[class='b5cd09854e d10a6220b4']").text
            except:
                hotel_score = "NA"

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
        return collection
