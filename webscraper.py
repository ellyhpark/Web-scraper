import requests
from bs4 import BeautifulSoup, NavigableString
import csv

r = requests.get('https://chamber.sdbusinesschamber.com/list/search?q=&c=&sa=False&gr=25&gn=')
soup = BeautifulSoup(r.text, 'html.parser')

# list of all business boxes
business_boxes = soup.find_all('div', class_='gz-list-card-wrapper')

# 2D list containing lists that each represent a business
businesses = [['Name', 'Description', 'Address', 'Phone', 'Website']]

# collect business name
def get_business_name(box) -> str:
    name_h5 = box.h5
    if name_h5 is not None:
        h5_children = name_h5.contents
        anchor = h5_children[1]
        name = str(anchor.string)
    else:
        name = ''
    return name

# collect business description
def get_business_description(box) -> str:
    description_p = box.find('p', class_='card-text gz-description gz-member-description')
    if description_p is not None:
        description_p_children = description_p.contents
        description = ''

        for child in description_p_children:
            if isinstance(child, NavigableString) and child != ' ':
                description += (child + ' | ')
    else:
        description = ''
    return description

# collect business address
def get_business_address(box) -> str:
    street_addr_span = box.find('span', class_='gz-street-address')
    if street_addr_span is not None:
        street_addr_span_children = street_addr_span.contents
        street_addr = street_addr_span_children[0] + ', '
    else:
        street_addr = ''
    
    citystatezip_addr_div = box.find('div', attrs={'itemprop': 'citystatezip'})
    if citystatezip_addr_div is not None:
        citystatezip_addr_div_children = citystatezip_addr_div.contents
        city_addr = ''
        state_addr = ''
        zip_addr = ''
        has_stateorzip_addr = False

        for child in citystatezip_addr_div_children:
            if child == citystatezip_addr_div.find('span', class_='gz-address-city'):
                city_addr = child.string
            elif child != '\n' and not has_stateorzip_addr:
                # assumes if one of state or zip address exists and not both, then it is state address
                state_addr = child.string
                has_stateorzip_addr = True
            elif child != '\n' and has_stateorzip_addr:
                zip_addr = child.string
        
        citystatezip_addr = city_addr + ', ' + state_addr + ' ' + zip_addr
    else:
        citystatezip_addr = ''
    
    address = street_addr + citystatezip_addr
    return address

# collect business phone
def get_business_phone(box) -> str:
    phone_li = box.find('li', class_='gz-card-phone')
    if phone_li is not None:
        phone_li_children = phone_li.contents
        phone_a_children = phone_li_children[1].contents
        phone = str(phone_a_children[1].string)
    else:
        phone = ''
    return phone

# collect business website link
def get_business_website(box) -> str:
    website_li = box.find('li', class_='gz-card-website')
    if website_li is not None:
        website_li_children = website_li.contents
        website_a = website_li_children[1]
        website = website_a['href']
    else:
        website = ''
    return website

# gather info from each business box
def update_businesses_list(business_boxes):
    for box in business_boxes:
        b = []

        b.append(get_business_name(box))
        b.append(get_business_description(box))
        b.append(get_business_address(box))
        b.append(get_business_phone(box))
        b.append(get_business_website(box))
        
        businesses.append(b)

    # for each business box
        # check name exists and add to the b list
        # do the same for description, address, phone, website link
        # if info does not exist, add empty string for that category to the b list
        # add the b list to the businesses list

# write to CSV file
def write_csv_file(businesses, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(businesses)

update_businesses_list(business_boxes)
write_csv_file(businesses, 'businesses.csv')