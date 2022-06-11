#Devesh Krishan
#Program updates a Canvas LMS Page by replacing relevant dates with specified dates. 
#Uses Google Sheets API and Canvas API

import urllib.request, urllib.parse, json, requests, download_csv


def _extract_course_info(url: str) -> tuple:
    course_num = url[url.find("courses") + 8:url.find("pages") - 1]
    title = url[url.find("pages") + 6:]
    return (course_num, title)



def run() -> None:
    pass

def execute_main(url: str, week, access_token) -> None:
    headers = {'Authorization' : 'Bearer ' + access_token}
    title = _extract_course_info(url)[1]
    course_num = _extract_course_info(url)[0]
    data = obtain_response(title, course_num, access_token)
    converted_dict = json.loads(data)
    class_dates_list = container_of_spreadsheet_dates()
    new_html_code = change_html(week, converted_dict, class_dates_list)
    result = send_new_page(title, course_num, new_html_code, access_token, headers)
    return result

def container_of_spreadsheet_dates() -> list:
    '''Creates a list of all the dates.'''
    # return storing_dates.grab_dates()
    return download_csv.download_data()

def obtain_response(title, course_num, access_token) -> str:
    '''Takes a URL and returns the data from the given URl.'''
    url = f"https://canvas.eee.uci.edu/api/v1/courses/{course_num}/pages/{title}?access_token={access_token}"
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    try: data = response.read()
    finally: response.close()
    return data.decode(encoding = "utf-8")

def _extract_course_info(url: str) -> tuple:
    # course_num = url[url.find("courses") + 8:url.find("pages") - 1]
    # title = url[url.find("pages") + 6:]
    # return (course_num, title)
    return (url[url.find("courses") + 8:url.find("pages") - 1], url[url.find("pages") + 6:])

def send_new_page(title, course_num, data: str, access_token, headers) -> None:
    url = f"https://canvas.eee.uci.edu/api/v1/courses/{course_num}/pages/{title}?'wiki_page[body]=Updated+body+text'?access_token={access_token}"
    dict_send = {'wiki_page[published]': True, 'wiki_page[body]': data}
    r = requests.put(url, headers=headers, data=dict_send)
    if r.reason != 'OK': return 'Was not successful!'
    else: return 'Successful!'

#Aim to rewrite this with a generator to save memory
def change_html(week_date: int , converted_dict: dict, class_dates_list: list) -> str:
    class_date = _change_numbers(week_date)
    for header, info in converted_dict.items():
        if header == "body":
            if f"Week{class_date}_ClassDate" in info:
                tag_value = info.split(f'class="Week{class_date}_ClassDate"')[1]
                tag_value = tag_value.split('<')[0]
                tag_value = tag_value.replace(">", "")
                tag_value = tag_value.replace("<", "")
                week = class_dates_list[week_date - 1]
                replace_date = ' '.join(week.split()[1:])
                replace_date = f"Week {week_date} Lecture - {replace_date}"
                info = info.replace(tag_value, replace_date)
                return info
            else: print("Week[00-10]_ClassDate tag is not found!")

def _change_numbers(week_date: int) -> str:
    assert 0 < week_date < 11, "Week is not between 1 and 10."
    if week_date < 10: return f'0{week_date}'
    else: return str(week_date)

if __name__ == "__main__": run()