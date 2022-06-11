import PySimpleGUI, test_canvas_api, time

def main() -> None:
    theme_name_list = PySimpleGUI.theme_list()
    PySimpleGUI.theme(theme_name_list[4])

    layout = [  [PySimpleGUI.Text('Welcome to the Canvas Date Update Tool!')],
                [PySimpleGUI.Text('Enter your CANVAS token:'), PySimpleGUI.InputText()],
                [PySimpleGUI.Text('Enter the URL you woud like to use:'), PySimpleGUI.InputText()],
                [PySimpleGUI.Text('Enter the WEEK you woud like to update:'), PySimpleGUI.InputText()],
                [PySimpleGUI.Button('Ok'), PySimpleGUI.Button('Close')] , 
                [PySimpleGUI.Text('STATUS: ', key = "status")]
                ]

    window = PySimpleGUI.Window("Canvas Date Update Tool", layout)

    while True:
        event, values = window.read()
        if event == PySimpleGUI.WIN_CLOSED or event == "Close":
            break
        elif event == "Ok":
            canvas_token = values[0]
            url = values[1]
            weeks = values[2].split(',')

            assert canvas_token != "", "Please enter a value for CANVAS token."
            assert url != "", "Please enter a value for URL token."
            assert weeks != "", "Please enter a value for WEEKS token."

            for week in weeks:
                result = test_canvas_api.execute_main(url, int(week), canvas_token)
            window['status'].update(f"STATUS: {result}")

    window.close()

if __name__ == '__main__': main()