from bootcamp_lib.dynamodb import DynamodbTable


class HoroscopeDataModel(DynamodbTable):
    signDateMapping: str = ""
    sign: str = ""
    horoscopeString: str = ""
    horoscopeDate: str = ""


class HoroscopeDataTable(DynamodbTable[HoroscopeDataModel]):
    table = "horoscope_data"
    model_type = HoroscopeDataModel
