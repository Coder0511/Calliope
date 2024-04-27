import json
from flet import *
from time import sleep

def main(page: Page):
    def page_close():
        page.window_close()
        page.window_destroy()

    def minimize_window():
        page.window_minimized = not page.window_minimized
        page.update()
    
    def maximize_window():
        page.window_maximized = not page.window_maximized
        page.update()

    def return_theme_mode():
        if page.theme_mode == "LIGHT":
            return "light"
        elif page.theme_mode == "DARK":
            return "dark"
        return "system" 
    
    def pick_files_result(e: FilePickerResultEvent):
        selected_file.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelado!"
        )
        selected_file.update()

    def radiogroup_theme(e):
        if (e.control.value == "light"):
            page.theme_mode = "LIGHT"
        elif (e.control.value == "dark"):
            page.theme_mode = "DARK"
        else:
            page.theme_mode = "SYSTEM"
        page.update()
        update_default_theme(page.theme_mode)
        

    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else default_route
        directory_path.update()
        temporal_route = directory_path.value
        update_default_route(temporal_route)

    def wait_animation_pick():
        sleep(0.1)
        temporal_route = pick_file_dialog.pick_files()
        update_default_route(temporal_route)
        
    
    def wait_animation():
        sleep(0.2)
        temporal_route = get_directory_dialog.get_directory_path()
        update_default_route(temporal_route)
    
    def change_text(e):
        default_size = int(e.control.value)
        
        text_textField1.text_size = default_size
        sample_text.size = default_size
        editable.size = default_size
        text_radio_1_text1.size = default_size
        text_radio_1_text2.size = default_size
        text_radio_2_text1.size = default_size
        text_radio_2_text2.size = default_size
        text_radio_2_text2.size = default_size
        text_textField2.text_size = default_size
        separator_1.size = default_size + 4
        separator_2.size = default_size + 4
        text_radio_5_text1.size = default_size
        text_radio_5_text2.size = default_size
        text_radio_5_text3.size = default_size
        theme_text.size = default_size
        separator_3.size = default_size + 4
        separator_4.size = default_size + 4
        text_radio_3_text1.size = default_size
        text_radio_3_text2.size = default_size
        text_radio_4_text1.size = default_size
        text_radio_4_text2.size = default_size
        text_textField4.text_size = default_size
        selected_file.size = default_size
        directory_path.size = default_size
        page.update()
    
    def update_default_size(e):
        with open("config.json", "w") as file:
            default_size = int(e.control.value)
            data["size"] = default_size
            json.dump(data, file)
    
    def update_default_theme(my_theme):
        with open("config.json", "w") as file:
            default_theme = my_theme
            data["theme"] = default_theme
            json.dump(data, file)
    
    def update_default_route(my_route):
        with open("config.json", "w") as file:
            default_route = my_route
            data["route"] = default_route
            json.dump(data, file)
    
    with open("config.json", "r") as file:
        data = json.load(file)
    
    default_size = data["size"]
    default_theme = data["theme"]
    default_route = data["route"]

    page.theme_mode = default_theme
    page.window_title_bar_hidden = True
    page.window_min_height = 950
    page.window_min_width = 1400
    page.window_width = 1401
    page.window_height = 951
    page.theme = Theme(primary_text_theme=TextTheme.body_large)

    window_frame = Container(
        ResponsiveRow([WindowDragArea(
            Container(
                content=Row([
                    IconButton(icons.MINIMIZE_SHARP, on_click=lambda e: minimize_window()),
                    IconButton(icons.CHECK_BOX_OUTLINE_BLANK_SHARP, on_click=lambda e: maximize_window()),
                    IconButton(icons.CLOSE_SHARP, on_click=lambda e: page_close())
                ],alignment="END")
            )
        )
        ]), height=32)
    
    text_radio_1_text1 = Text("Encriptar", size=default_size)
    text_radio_1_text2 = Text("Desencriptar", size=default_size)

    text_radio_1 = RadioGroup(content=Row([
        Radio(value="encriptar", label=""),
        text_radio_1_text1,
        Radio(value="desencriptar", label=""),
        text_radio_1_text2
    ]))

    text_radio_2_text1 = Text("AES", size=default_size)
    text_radio_2_text2 = Text("Mandel", size=default_size)
    
    text_radio_2 = RadioGroup(content=Row([
        Radio(value="aes", label=""),
        text_radio_2_text1,
        Radio(value="mandel", label=""),
        text_radio_2_text2
    ]))

    text_textField1 = TextField(
        width=500,
        height=273,
        multiline=True,
        min_lines=1,
        hint_text="Escribe algo aquí",
        text_size=default_size
    )

    text_textField2 = TextField(
        width=800,
        hint_text="Clave simétrica",
        text_size=default_size
    )

    editable = Text("Resultado de la operación", selectable=True, size=default_size, weight=FontWeight.W_500, opacity=0.7)

    text_textField3 = Container(
        content=editable,
        width=500,
        height=273,
        border=border.all(1, colors.BLACK),
        border_radius=4,
        padding=padding.only(left=10, top=15)
    )

    separator_1 = Text("\nProceso:", size=default_size+4)
    separator_2 = Text("\nAlgoritmo:", size=default_size+4)

    tab1_content = Container(
        content=Column([
            separator_1,
            text_radio_1,
            separator_2,
            text_radio_2,
            text_textField2,
            Row([
                ElevatedButton(text="Generar", style=ButtonStyle(animation_duration=500)),
                ElevatedButton(text="Copiar", style=ButtonStyle(animation_duration=500))
            ]),
            Text("\n"),
            Row([
                text_textField1,
                ElevatedButton(text="Operar", style=ButtonStyle(animation_duration=500)),
                text_textField3
            ])
        ]),
        padding=16
    )

    separator_3 = Text("\nProceso:", size=default_size+4)
    separator_4 = Text("\nAlgoritmo:", size=default_size+4)

    text_radio_3_text1 = Text("Encriptar", size=default_size)
    text_radio_3_text2 = Text("Desencriptar", size=default_size)

    text_radio_3 = RadioGroup(content=Row([
        Radio(value="encriptar"),
        text_radio_3_text1,
        Radio(value="desencriptar"),
        text_radio_3_text2
    ]))

    text_radio_4_text1 = Text("AES", size=default_size)
    text_radio_4_text2 = Text("Mandel", size=default_size)
    
    text_radio_4 = RadioGroup(content=Row([
        Radio(value="aes"),
        text_radio_4_text1,
        Radio(value="mandel"),
        text_radio_4_text2
    ]))

    text_textField4 = TextField(
        width=800,
        hint_text="Clave simétrica",
        text_size=default_size
    )

    pick_file_dialog = FilePicker(on_result=pick_files_result)
    selected_file = Text(value="Solo formato .txt, .pdf, .csv, .docx y .odt", selectable=True)

    page.overlay.append(pick_file_dialog)

    file_picker = Row(
            [
                ElevatedButton(
                    "Elegir archivo",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: wait_animation_pick(),
                    style=ButtonStyle(animation_duration=500)
                ),
                selected_file,
            ]
        )

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text(value=default_route, selectable=True)

    page.overlay.append(get_directory_dialog)

    save_file = Row(
            [
                ElevatedButton(
                    "Guardar en",
                    icon=icons.SAVE,
                    on_click=lambda _: wait_animation(),
                    style=ButtonStyle(animation_duration=500),
                ),
                directory_path
            ]
        )

    tab2_content = Container(
        content=Column([
            separator_3,
            text_radio_3,
            separator_4,
            text_radio_4,
            text_textField4,
            Row([
                ElevatedButton(text="Generar", style=ButtonStyle(animation_duration=500)),
                ElevatedButton(text="Copiar", style=ButtonStyle(animation_duration=500))
            ]),
            Text(""),
            file_picker,
            save_file,
            Text("\n"),
            ElevatedButton(text="Operar", style=ButtonStyle(animation_duration=500))
        ]),
        padding=16
    )

    theme_text = Text(value="\nTema:", size=default_size)
    text_radio_5_text1 = Text(value="Claro", size=default_size)
    text_radio_5_text2 = Text(value="Oscuro", size=default_size)
    text_radio_5_text3 = Text(value="Sistema", size=default_size)

    text_radio_5 = RadioGroup(content=Row([
        Radio(value="light"),
        text_radio_5_text1,
        Radio(value="dark"),
        text_radio_5_text2,
        Radio(value="system"),
        text_radio_5_text3
        ]), on_change=radiogroup_theme, value=return_theme_mode())

    sample_text = Text(value="Tamaño de letra:", size=default_size)

    slider1 = Slider(
        min=16,
        max=30,
        divisions=14,
        label="{value}",
        width=500,
        on_change=change_text,
        value=sample_text.size,
        on_change_end=update_default_size
    )

    tab3_content = Container(
        content=Column([
            theme_text,
            text_radio_5,
            Text("\n\n"),
            sample_text, 
            slider1
        ]),
        padding=16
    )

    tabs_list = Container(
        Tabs(
            selected_index=0,
            animation_duration=250,
            tabs=[
                Tab(
                    text="Texto",
                    content=tab1_content
                ),
                Tab(
                    text="Archivo",
                    content=tab2_content
                ),
                Tab(
                    icon=icons.SETTINGS,
                    content=tab3_content
                )
            ],
            expand=1,
            divider_color=colors.with_opacity(0, "#000000")
        ))

    page.add(window_frame)
    page.add(tabs_list)

    page.update()

if __name__ == "__main__":
    app(target=main)