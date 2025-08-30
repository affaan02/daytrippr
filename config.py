# config.py
class AppConfig:
    SECRET_KEY = "dev-daytrippr-not-sensitive"
    MORNING_ARRIVE_END_HOUR = 11     # arrive by 11:00
    EVENING_DEPART_START_HOUR = 17   # depart 17:00+
    CURRENCY = "USD"

    BRAND_NAME = "Daytrippr"
    BRAND_TAGLINE = "Day-Trip Flights · Morning in, Evening out"
    BRAND_EMAIL = "hello@daytrippr.app"
