import pytest
from components.formbuilder.formoutput import *

def test_yesno_output_yes():
    #given
    value = "1"
    #when
    d = YesNo_Output(value).output()
    #then
    expected = "Yes"
    assert expected == d

def test_yesno_output_no():
    #given
    value = "0"
    #when
    d = YesNo_Output(value).output()
    #then
    expected = "No"
    assert expected == d