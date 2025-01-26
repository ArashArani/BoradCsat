from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

db = SQLAlchemy()

mail = Mail()
import random
import string

def generate_random_code(length=6):
  """Generates a random code of specified length using uppercase letters and digits."""
  characters = string.ascii_uppercase + string.digits
  code = ''.join(random.choice(characters) for i in range(length))
  return code

# Example usage:
