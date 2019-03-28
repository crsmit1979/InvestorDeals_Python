from selenium import webdriver
from db.db import initialize_db, Deal
import os
import pytest

driver = webdriver.Chrome()
#initialize_db()

def open_window(url):
    driver.get(url)

def get_element_by_name(name):
    elem = driver.find_element_by_name(name)

def get_element_by_id(name):
    elem = driver.find_element_by_id(name)

def type_text(elem_id, txt):
    elem = driver.find_element_by_name(elem_id)
    elem.send_keys(txt)

def select_combo(name, value):
    el = driver.find_element_by_name(name)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == value:
            option.click() # select() in earlier versions of webdriver
            break

def select_checkbox(name):
    el = driver.find_element_by_name(name)
    el.click()

def click_button(name):
    el = driver.find_element_by_name(name)
    el.click()

def click_by_xpath(xpath):
    el = driver.find_element_by_xpath(xpath)
    el.click()

def login_user():
    driver.get("http://localhost:3002/login_test_user")

def goto_page(url):
    driver.get(url)

def get_text_value(name):
    el = driver.find_element_by_name(name)
    return el.get_attribute("value")

def test_adding_deal():
    title = "title"
    county = "county"
    description = "description"
    postcode = "tw18"
    city = "shepperton"
    address_line_1 = "add 1"
    address_line_2 = "add 2"
    sourcing_fee = 100
    roi = 10

    Deal.delete().where(Deal.title == str(title)).execute()
    open_window("http://localhost:3002")
    login_user()
    goto_page("http://localhost:3002/deals/new")
    type_text("title", title)
    type_text("description", description)
    type_text("sourcing_fee", sourcing_fee)
    type_text("roi", roi)
    type_text("address_line_1", address_line_1)
    type_text("address_line_2", address_line_2)
    type_text("city", city)
    type_text("postcode", postcode)
    type_text("county", county)
    select_combo("deal_type","HMO")
    select_combo("bedrooms", "4 Bed")
    select_checkbox("show_address")
    #type_text("", "")
    #type_text("", "")

    click_button("submit_button")

    #THEN
    deal = Deal.get(Deal.county==str(county))
    goto_page("http://localhost:3002/deals/%s" % (deal.uuid))
    assert title == get_text_value('title')
    assert description == get_text_value('description')
    assert county == get_text_value('county')
    assert city == get_text_value('city')
    assert postcode == get_text_value('postcode')
    assert address_line_1 == get_text_value('address_line_1')
    assert address_line_2 == get_text_value('address_line_2')
    assert roi == float(get_text_value('roi'))
    assert sourcing_fee == float(get_text_value('sourcing_fee'))

    driver.close()

def test_validation_error_is_shown():
    description = ""

    goto_page("http://localhost:3002/deals")
    click_by_xpath("//a[@title='Edit Record']")
    type_text("description", description)
