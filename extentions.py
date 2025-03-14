import string
import random
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

import jdatetime


db = SQLAlchemy()

mail = Mail()


def generate_random_code(length=6):
    """Generates a random code of specified length using uppercase letters and digits."""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    return code


# آرایه‌های نام روزها و ماه‌ها
days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد",
          "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]

# Example usage:


def today():

    today = jdatetime.datetime.now()

    # تبدیل به تاریخ شمسی
    jalali_date = today.togregorian()

    # نمایش تاریخ شمسی
    today = jdatetime.datetime.now()

    # تبدیل به تاریخ شمسی
    jalali_date = today

    # نمایش تاریخ شمسی
    return f"{days[jalali_date.weekday()]} ، {jalali_date.day} {months[jalali_date.month - 1]}"
