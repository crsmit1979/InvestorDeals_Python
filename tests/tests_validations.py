import pytest
from components.formbuilder.validations import  *

def test_value_is_numeric():
    #GIVEN
    txt = 100

    #WHEN
    val = IsNumeric_Validation(txt)
    result = val.is_valid()

    #THEN
    assert result == True, "Is not numeric"

def test_value_is_not_numeric():
    #GIVEN
    txt = "198"

    #WHEN
    val = IsNumeric_Validation(txt)
    result = val.is_valid()

    #THEN
    assert result == True, "Is not numeric"

def test_value_is_not_numeric():
    #GIVEN
    txt = "198str"

    #WHEN
    val = IsNumeric_Validation(txt)
    result = val.is_valid()

    #THEN
    assert result == False, "Is numeric"

@pytest.fixture()
def test_value_is_not_numeric():
    #GVIEN
    txt = "test"
    val = IsNumeric_Validation(txt)
    result = val.is_valid()

    #THEN
    assert result == False, "Is numeric"


def test_NotEmpty_Validation_is_empty():
    #GIVEN
    txt = ""

    #WHEN
    val = NotEmpty_Validation(txt)
    result = val.is_valid()
    #THEN
    assert result == False



def test_NotEmpty_Validation_is_empty2():
    # GIVEN
    txt = None

    # WHEN
    val = NotEmpty_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False


def test_NotEmpty_Validation_is_not_empty():
    # GIVEN
    txt = "1"

    # WHEN
    val = NotEmpty_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == True


def test_ValidateDate_Validation_is_valid():
    # GIVEN
    txt = "10/12/2019"

    # WHEN
    val = ValidDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == True

def test_ValidateDate_Validation_is_not_valid():
    # GIVEN
    txt = ""

    # WHEN
    val = ValidDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False

def test_ValidateDate_Validation_is_not_valid2():
    # GIVEN
    txt = "2019/10/20"

    # WHEN
    val = ValidDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False


def test_IsFutureDate_is_valid():
    # GIVEN
    txt = "20/10/2020"

    # WHEN
    val = IsFutureDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == True

def test_IsFutureDate_is_not_valid():
    # GIVEN
    txt = "20/10/1920"

    # WHEN
    val = IsFutureDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False


def test_IsPastDate_is_not_valid():
    # GIVEN
    txt = "20/10/2020"

    # WHEN
    val = IsPastDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False

def test_IsPastDate_is_valid():
    # GIVEN
    txt = "20/10/1920"

    # WHEN
    val = IsPastDate_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == True



def test_IsEmailValidation_is_valid():
    # GIVEN
    txt = "crsmit@gmail.com"

    # WHEN
    val = IsEmail_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == True


def test_IsEmailValidation_is_not_valid():
    # GIVEN
    txt = "crsmit.gmail.com"

    # WHEN
    val = IsEmail_Validation(txt)
    result = val.is_valid()

    # THEN
    assert result == False



