from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import tests
import uuid

app = FastAPI()

class TestInfo(BaseModel):
    name: str
    api_test_code: str
    documentation: str = None

class TestIn(BaseModel):
    name: str
    api_test_code: str
    n_control: int
    n_test: int
    converted_control: int
    converted_test: int
    confidence_level: float

class TestOut(BaseModel):
    test_name: str
    test_id: str
    conversion_rate_control: float
    conversion_rate_test: float
    relative_variation: float
    pvalue: float
    score: float
    significativity: str

TESTS = {
        "z": {
               "name": "Z test",
               "api_test_code": "z",
               "documentation": None,
               "test": tests.ztest
        },
        "chi2": {
              "name": "Chi-2 test",
              "api_test_code": "chi2",
              "documentation": None,
              "test": tests.chi2test
        },
        "MWU": {
               "name": "Mann-Whitney U test",
               "api_test_code": "MWU",
               "documentation": None,
               "test": tests.MWUtest
        },
        "t": {
              "name": "Student test",
              "api_test_code": "t",
              "documentation": None,
              "test": tests.ttest
        }
}

@app.get("/abtest/info", response_model = List[TestInfo])
async def get_info():
    infos = list()
    for test in TESTS:
        t = TESTS[test]
        t.pop("test")
        infos.append(t)
    return infos

@app.post("/abtest/test/", response_model=List[TestOut])
async def run(inputs: TestIn):
    inputs = inputs.dict()
    p_control, p_test, variation, score, pvalue = TESTS[inputs['api_test_code']]['test'](inputs["n_control"], inputs["n_test"], inputs["converted_control"], inputs["converted_test"])
    if pvalue < inputs['confidence_level']:
        significativity = True
    else:
        significativity = False
    return [{
             "test_name": inputs['name'],
             "test_id": uuid.uuid4().hex,
             "conversion_rate_control": p_control,
             "conversion_rate_test": p_test,
             "relative_variation": variation,
             "pvalue": pvalue,
             "score": score,
             "significativity": str(significativity)
             }]
