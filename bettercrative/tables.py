from flask_table import Table, Col

class Results(Table):
    id = Col('Id' show=False)
    key =C ol('Key')
    title = Col('title')
    creation_date = Col('Date Created')