from bootcamp_lib.dynamodb import DynamodbTable


class HoroscopeStatsModel(DynamodbTable):
    horoscopeStatType: str = ""


class HoroscopeStatsTable(DynamodbTable[HoroscopeStatsModel]):
    table = "horoscope_stats"
    model_type = HoroscopeStatsModel
