from datetime import datetime

def heading(cols:list):
    header = "<tr>"
    for key in cols:
        header = f"{header}<th class='col col-{key}'>{key.title()}</th>"

    return f"{header}</tr>"


def row(package:dict, cols:list) -> str:
    row = "<tr>"
    i:int = 0
    for key in cols:
        value = package.get(key, None)
        # check for lists, in particular on the tag
        if type(value) == list:
            value = ", ".join(value)
        if type(value) == dict:
            value = value.get('version', None)

        if i == 0:
            row_id = int(datetime.utcnow().timestamp() * 1000)
            row = f"{row}<th id='p-{row_id}' class='col col-{key}'>{value}</th>"
        else:
            row = f"{row}<td class='col col-{key}'>{value}</td>"
        i = i + 1

    row = f"{row}</tr>"
    return row
