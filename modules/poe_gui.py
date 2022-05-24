import PySimpleGUIQt as sg


gui_bgc = '#F6F5FF'


class POEGui(object):
    """docstring for POEGui"""

    def __init__(self):
        super(POEGui, self).__init__()

    def layout_hk_row(self, hk_title, cb_id):
        row = [
            sg.Checkbox(hk_title, enable_events=True, key=cb_id),
            sg.T(' ' * 30),
            # sg.Button('Default'),
            sg.InputText(enable_events=True)
        ]
        return row

    def btn_big(self, text, btn_color=None):
        btn_color = btn_color if btn_color else None
        btn = sg.Button(
            text,
            border_width=0,
            button_color=btn_color,
            size=(20, 1)
        )
        return btn


poe_gui = POEGui()


def checkbox_one():
    print('Checkbox 1 callback')


if __name__ == '__main__':
    hk_cb_callbacks = {'kb_cb_1': checkbox_one, 'kb_cb_2': ''}
    hk_cb_rows = [
        ('Hotkey 1', 'kb_cb_1'),
        ('Hotkey 2', 'kb_cb_2'),
    ]
    layout = [
        [sg.Text('Selected Hotkeys')],
        [sg.Text('')],
    ]
    tab1_layout = [
        poe_gui.layout_hk_row(i[0], i[1]) for i in hk_cb_rows
    ]
    tab2_layout = [[sg.T('This is inside tab 2')]]
    tab3_layout = [[
        sg.T('This is inside tab 3', size=(0, 18)),
    ]]
    layout = [[
        sg.TabGroup(
            [[
                sg.Tab('Hotkeys', tab1_layout),
                sg.Tab('Trader', tab2_layout),
                sg.Tab('Options', tab3_layout),
            ]],
            tab_location='top',
            selected_title_color=None,
        ),
    ], [
        poe_gui.btn_big('Start'),
        poe_gui.btn_big('Stop'),
    ]]
    sg.ListOfLookAndFeelValues()
    # Create the Window
    window = sg.Window('Program', layout, font='Verdana 10', size=(345, 380))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):   # if user closes window or clicks cancel
            break
        print(event)
        print(f'You entered {values}')

        try:
            f = hk_cb_callbacks[event]
            f()
        except Exception as err:
            print(err)

    window.close()
