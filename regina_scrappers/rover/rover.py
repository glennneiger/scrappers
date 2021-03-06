'''
Created on 13-Aug-2015

@author: satyandra
'''

import re, csv, mechanize, cookielib
import random
from lxml import html
import datetime, time
temp_list = []
city_t = []


def mechanize_br():
    version_list = ['5.0', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0', '20.0', '21.0', '22.0', '23.0',
                    '24.0', '25.0', '26.0', '27.0', '28.0', '29.0', '30.0', '31.0', '32.0', '33.0', '34.0', '35.0', '36.0', '37.0', '38.0',  '1.0',  '2.0', '3.0', '4.0']
    # print "Browser version ", (random.choice(version_list))
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(False)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/'+(random.choice(version_list))+' (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'), ('Accept', '*/*')]
    
    return br

def extract_details(url, zip_code):
    time.sleep(0)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    unique_url = url
    print unique_url
    
    title = "".join(parsed_source.xpath("//span[@itemprop='name']/text()")).strip()
    print title
    
    review_count = "".join(parsed_source.xpath("//meta[@itemprop='ratingCount']/@content")).strip()
    print review_count
    
    print zip_code
    
    try:
        list_price = "".join(parsed_source.xpath("//span[@itemprop='priceRange']/text()")[0]).strip()+' per night'
    except:
        list_price = ''
    print list_price
        
    
    badges = " || ".join(parsed_source.xpath("//div[@class='profile-section-widget badges-widget noborder']/ul/li/@title"))
    print badges
    
    date_list = [unique_url, title, review_count, zip_code, list_price, badges]
    return date_list

def extract_pagination(url):
    print url
    time.sleep(0)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    items = "".join(parsed_source.xpath("//span[@class='button-meta']/strong/text()")[0]).strip()
    pages = (int(items)/15)+1
    return pages

def extract_details_url(url):
    time.sleep(0)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    url_list = []
    items_urls = parsed_source.xpath("//div[@class='sitter-card-body media-body']")
    for items_url in items_urls:
        detail_url = "".join(items_url.xpath(".//a[@class='sitter-link js-profile-link']/@href"))
        zipcode =  "".join(items_url.xpath(".//span[@class='heading-number']/text()"))
        url_list.append([detail_url, zipcode])
    return url_list

def extract_city_urls(url):
    time.sleep(0)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    city_urls = parsed_source.xpath("//ul[@class='list-unstyled']/li/a/@href")
    return city_urls

def extract_viewall_urls(url):
    time.sleep(0)
    br_instance = mechanize_br()
    html_response = br_instance.open(url)
    html_source = html_response.read()
    result = html_source.replace('\n', '').replace('\r', '')
    parsed_source = html.fromstring(result, 'https://www.rover.com')
    parsed_source.make_links_absolute()
    
    viewall_urls = parsed_source.xpath("//a[contains(text(), 'View All')]/@href")
    #print viewall_urls
    return viewall_urls
    
if __name__ == '__main__':
    date = datetime.date.today().strftime("%B %d, %Y")
    data_writer_url = csv.writer(open('rover url.csv', 'ab'))
    
    city_url_file = open('city.txt', 'ab')
    scrapped_url_file_w = open('already_scrapped_url.txt', 'ab')
    #date = datetime.date.today().strftime("%B %d, %Y")
    #data_writer = csv.writer(open('rover '+date+'.csv', 'wb'))
    #data_writer.writerow(['URL', 'Title', '# of Guest Reviews', 'Zip Code', 'List Price', 'Badges'])
    
    seed_urls = 'https://www.rover.com/top-dog-boarding-cities/'
    viewall_urls = extract_viewall_urls(seed_urls)
    for viewall_url in viewall_urls:
        city_urls = extract_city_urls(viewall_url)
        for city_url in city_urls:
            open_city_file = open('city.txt', 'rb')
            city_url_file_r = open_city_file.readlines()
            print city_url_file_r
            print city_url
            
            if city_url+'\n' in city_url_file_r or city_url in city_t:
                print '+'*78
                print "passing city"
                pass
            else:
                
                for page in range(1, 2):
                    page_url = city_url+'&page='+str(page)
                    detail_urls = extract_details_url(page_url)
                    for detail_url in detail_urls:
                        detail_url_t = detail_url[0]
                        zipcode = detail_url[1]
                        open_file = open('already_scrapped_url.txt', 'rb')
                        url_list = open_file.readlines()
                        if detail_url[0]+'\n' in url_list or detail_url in temp_list:
                            print detail_url
                            print "Passing url"
                            pass
                        else:
                            print detail_url_t
                            print city_url
                            data_writer_url.writerow(detail_url)
                            scrapped_url_file_w.write(str(detail_url))
                            scrapped_url_file_w.write('\n')
                            temp_list.append(detail_url)
                        print '+'*78
            print "writing city"
            city_url_file.write(city_url)
            city_url_file.write('\n')
            city_t.append(city_url)
            open_city_file.close()
            """
                data = extract_details(detail_url_t, zipcode)
                print "Writing data for url", detail_url
                print data
                data_writer.writerow([unicode(s).encode("utf-8") for s in data])
                print '*'*78
            """