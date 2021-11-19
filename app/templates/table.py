from datetime import datetime

def heading(cols:list):
    header = "<tr>\n"
    for key in cols:
        header = f"{header}\t<th class='col col-{key}'>{key.title()}</th>\n"

    return f"{header}</tr>\n"


def row(package:dict, cols:list) -> str:
    row = "<tr>\n"
    i:int = 0
    for key in cols:
        value = package.get(key, None)
        if i == 0:
            row_id = int(datetime.utcnow().timestamp() * 1000)
            row = f"{row}\t<th id='p-{row_id}' class='col col-{key}'>{value}</th>\n"
        else:
            row = f"{row}\t<td class='col col-{key}'>{value}</td>\n"
        i = i + 1

    row = f"{row}</tr>\n"
    return row
