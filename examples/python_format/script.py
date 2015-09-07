import os
import datetime
from rucola import Rucola

# Sets working directory to this file directory:
app = Rucola(os.path.dirname(__file__))

# Find all .html files in a 'src' directory, and change it content
# using python build in format() method.
for f in app.find('**/*.html'):
    f.content = f.content.format(title='Welcome!', date=datetime.date.today())

app.build()
