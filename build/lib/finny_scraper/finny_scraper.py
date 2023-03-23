import requests
from bs4 import BeautifulSoup


class PropertyInfo:
    def __init__(self, url):
        self.url = url
        r = requests.get(self.url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        self.results = soup.find(class_="aboveBelowTheRail")
        self.property_object = {}

    # Property Image
    def get_property_image(self):
        images = self.results.find_all(
            "div", class_="InlinePhotoPreview--Photo")
        main_image_source = images[0].img['src']
        self.property_object['image'] = main_image_source
        return main_image_source

    # Listing Price
    def get_listing_price(self):
        house_price_element = self.results.find(
            'div', {'data-rf-test-id': 'abp-price'})
        house_price = house_price_element.find(class_="statsValue").text
        clean_house_price = int(
            round(float(house_price.replace('$', '').replace(',', ''))))
        self.property_object['list_price'] = clean_house_price
        return clean_house_price

    # Property Type
    def get_property_type(self):
        key_details_list = self.results.find(
            class_="keyDetailsList").find_all("div", class_="keyDetail")

        for detail in key_details_list:
            header = detail.find('span', class_="header")
            if header.text == "Property Type":
                content = detail.find('span', class_="content").text
                property_type = content
                break

        self.property_object['property_type'] = {
            'classification': property_type}
        return property_type

    # Specific Amenities
    def get_number_of_units(self):
        amenities = self.results.find(class_="amenities-container")
        number_of_units = amenities.find(
            string=lambda text: text and 'units' in text.lower() and '#' in text.lower() and 'with' not in text.lower()).find_next().text
        number_of_units_int = int(
            number_of_units)
        if number_of_units:
            self.property_object['property_type']['units'] = number_of_units_int
        else:
            self.property_object['property_type']['units'] = 1

        return number_of_units_int

    def get_property_info(self):
        self.get_property_image
        self.get_listing_price
        self.get_property_type
        self.get_number_of_units
        return self.property_object
