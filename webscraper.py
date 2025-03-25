import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString

r = requests.get('https://chamber.sdbusinesschamber.com/list/search?q=&c=&sa=False&gr=25&gn=')
soup = BeautifulSoup(r.text, 'html.parser')

# list of all business boxes
business_boxes = soup.find_all('div', class_='gz-list-card-wrapper')

# for each business box
    # check name exists and add to dictionary with key = 'name'
    # do the same for description, address, phone, website link
    # if info does not exist, add emty string as the value
    # add the dictionary to the businesses list

businesses = []

for box in business_boxes:
    business = {}

    # collect business name
    h5_children = box.h5.contents
    anchor = h5_children[1]
    name = anchor.string
    business['name'] = name
    print(name)

    # collect business description
    description_p = box.find('p', class_='card-text gz-description gz-member-description')
    if description_p is not None:
        description_p_children = description_p.contents
        description = ''

        for child in description_p_children:
            if isinstance(child, NavigableString) and child != ' ':
                description += (child + ' | ')
    else:
        description = ''
    business['description'] = description
    print(description)

    # collect business address
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
    business['address'] = address
    print(address)

    # collect business phone
    phone_li = box.find('li', class_='gz-card-phone')
    if phone_li is not None:
        phone_li_children = phone_li.contents
        phone_a_children = phone_li_children[1].contents
        phone = phone_a_children[1].string
    else:
        phone = ''
    business['phone'] = phone
    print(phone)

    # collect business website link
    website_li = box.find('li', class_='gz-card-website')
    if website_li is not None:
        website_li_children = website_li.contents
        website_a = website_li_children[1]
        website = website_a['href']
    else:
        website = ''
    business['website'] = website
    print(website)
    
    businesses.append(business)
    print('------------------------')