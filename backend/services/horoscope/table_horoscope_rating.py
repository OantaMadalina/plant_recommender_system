from bootcamp_lib.dynamodb import DynamodbTable


class HoroscopeRatingModel(DynamodbTable):
    signDateMapping: str = ""
    sign: str = ""
    horoscopeDate: str = ""
    rating: int = None


class HoroscopeRatingTable(DynamodbTable[HoroscopeRatingModel]):
    table = "horoscope_rating"
    model_type = HoroscopeRatingModel
