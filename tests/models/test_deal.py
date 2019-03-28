import datetime
import pytest
from models.Deal import Deal

def create_sample():
    new_deal = Deal.create(
        title = "title",
        description = "description",
        created = datetime.datetime.now(),
        created_by=1
    )
    return new_deal


def test_add_deal():
    new_deal = create_sample()
    rec = Deal.get_by_uuid(new_deal.uuid)
    assert rec is not None
    assert rec.title == new_deal.title
    assert rec.description == new_deal.description
    assert rec.created== new_deal.created
    assert rec.created_by == new_deal.created_by

def test_get_by_uuid():
    new_deal = create_sample()
    deal = Deal.get_by_uuid(new_deal.uuid)
    assert deal.title == new_deal.title
    assert deal.description == new_deal.description

def test_get_available_cities():
    cities = Deal.available_cities()
    lst = Deal.select().where(Deal.deleted==False).select(Deal.city).distinct()

    city_names = ",".join([city.city if city.city is not None else "" for city in cities])
    expected_names = ",".join([city.city if city.city is not None else "" for city in lst])
    assert len(cities) == len(lst)
    assert city_names == expected_names


def test_get_available_counties():
    counties = Deal.available_counties()
    lst = Deal.select().where(Deal.deleted==False).select(Deal.county).distinct()

    county_names = ",".join([county.county if county.county is not None else "" for county in counties])
    expected_names = ",".join([county.county if county.county is not None else "" for county in lst])
    assert len(counties) == len(lst)
    assert county_names == expected_names
