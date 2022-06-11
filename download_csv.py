import csv

def download_data() -> dict:
    # data = open_file("dates.csv")
    return _format_tags(open_file("dates.csv"))

def open_file(file: str)  -> list:
    '''Opens a .csv file and returns of a list of its contents.'''
    with open(file) as file:
        data = csv.reader(file)
        #Catches the header of the spreadsheet if needed.
        header = next(data)
        return list(data)

def _format_tags(data: list) -> list:
    '''Creates a formatted dictionary of tags and dates.'''
    dict_data =  {f'{"".join(line[0].split()[:2])}_ClassDate': line[1] for line in data}
    return [f'{week} {date}' for week, date in dict_data.items()]


def run() -> None:
    pass

if __name__ == "__main__": run()