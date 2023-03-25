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
        if images:
            main_image_source = images[0].img['src']
            self.property_object['image'] =  main_image_source
            return main_image_source
        else:
           self.property_object['image'] = None
           return None

    # Listing Price
    def get_listing_price(self):
        house_price_element = self.results.find(
            'div', {'data-rf-test-id': 'abp-price'})
        if house_price_element:
            house_price = house_price_element.find(class_="statsValue").text
            clean_house_price = int(
                round(float(house_price.replace('$', '').replace(',', ''))))
            self.property_object['list_price'] = clean_house_price
            return clean_house_price
        else:
            self.property_object['list_price'] = None
            return None

    # Property Type
    def get_property_type(self):
        key_details_list = self.results.find(
            class_="keyDetailsList").find_all("div", class_="keyDetail")
        if key_details_list:
            for detail in key_details_list:
                header = detail.find('span', class_="header")
                if header and header.text == "Property Type":
                    content = detail.find('span', class_="content").text
                    property_type = content
                    break

            if property_type:
                self.property_object['property_type'] = {
                    'classification': property_type}
                return property_type
            else:
                self.property_object['property_type'] = {
                    'classification': None}
                return None
        else:
            self.property_object['property_type'] = {
                    'classification': None, 'units': None}
            return None


    # Specific Amenities
    def get_number_of_units(self):
        amenities = self.results.find(class_="amenities-container")
        number_of_units_element = amenities.find(
            string=lambda text: text and 'units' in text.lower() and '#' in text.lower() and 'with' not in text.lower())
        if number_of_units_element:
            number_of_units = number_of_units_element.find_next().text
            number_of_units_int = int(number_of_units)
            self.property_object['property_type']['units'] = number_of_units_int
            return number_of_units_int
        else:
            self.property_object['property_type']['units'] = 1
            return 1

    # County and State Abbreviation, Address
    def get_address_info(self):
        facts_table = self.results.find(class_="facts-table")
        if facts_table:
            county_element = facts_table.find(
                string=lambda text: text and 'county' in text.lower())
            if county_element:
                county = county_element.find_next().text
            else:
                county = None
            address_element = self.results.find('div', class_="street-address")
            if address_element:
                address = address_element.text[:-1]
            else:
                address = None
            city_state_zip_element = self.results.find(
                'div', {'data-rf-test-id': 'abp-cityStateZip'})
            if city_state_zip_element:
                city_state_zip = city_state_zip_element.text
                city_state_zip_list = city_state_zip.split(',')
                city = city_state_zip_list[0] if len(city_state_zip_list) > 0 else None
                state_zip = city_state_zip_list[1] if len(city_state_zip_list) > 1 else None
                if state_zip:
                    state_zip_list = state_zip.split()
                    state = state_zip_list[0] if len(state_zip_list) > 0 else None
                    zip_code = state_zip_list[1] if len(state_zip_list) > 1 else None
                else:
                    state = None
                    zip_code = None
            else:
                city = None
                state = None
                zip_code = None
            self.property_object['address'] = {
                'county': county,
                'street_address': address,
                'city': city,
                'state': state,
                'zip_code': zip_code
            }
            return self.property_object['address']
        else:
            self.property_object['address'] = {
                'county': None,
                'street_address': None,
                'city': None,
                'state': None,
                'zip_code': None
            }
            return self.property_object['address']


    def get_property_info(self):
        self.get_property_image()
        self.get_listing_price()
        self.get_property_type()
        self.get_number_of_units()
        self.get_address_info()
        return self.property_object

url = 'https://www.redfin.com/CA/San-Diego/3280-Reynard-Way-92103/home/5364230'
house = PropertyInfo(url)
print(house.get_property_info())