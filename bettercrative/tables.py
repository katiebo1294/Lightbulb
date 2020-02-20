from abc import ABC

from flask_table import Table, Col


class Results(Table, ABC):
    id = Col('Id', show=False)
    key = Col('Key')
    title = Col('title')
    creation_date = Col('Date Created')
