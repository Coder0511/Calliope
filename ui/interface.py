from os import getenv
from time import sleep
from pathlib import Path
import pyperclip
from json import dump, load
from dotenv import load_dotenv
from core.operations.operations import process_string, process_file
from core.operations.key_generator import generate_key
from flet import Page, FilePickerResultEvent, Theme, \
TextTheme, Container, Row, ResponsiveRow, WindowDragArea, \
IconButton, icons, Radio, RadioGroup, Text, TextField, \
border, padding, Column, FontWeight, colors, ElevatedButton, \
ButtonStyle, FilePicker, Slider, Tabs, Tab, ProgressBar, ClipBehavior

def main(page: Page):
    relative_path = f"{Path(__file__).parent}/../settings/config.json"
    
    load_dotenv()
    randomorg_key = getenv("RANDOMORG_KEY")
    
    picked_file_path = Text("")
    
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
        picked_file_path.value = e.files[0].path if e.files else ""
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
        config_separator.size = default_size + 4
        config_separator_1.size = default_size + 2
        config_help_1.size = default_size
        config_separator_2.size = default_size + 2
        config_help_2.size = default_size
        page.update()
    
    def update_default_size(e):
        with open(relative_path, "w") as file:
            default_size = int(e.control.value)
            data["size"] = default_size
            dump(data, file)
    
    def update_default_theme(my_theme):
        with open(relative_path, "w") as file:
            default_theme = my_theme
            data["theme"] = default_theme
            dump(data, file)
    
    def update_default_route(my_route):
        with open(relative_path, "w") as file:
            default_route = my_route
            data["route"] = default_route
            dump(data, file)
            
    def text_section_set_text(self):
        text_textField2.value = generate_key(randomorg_key)
        text_textField2.update()
        
    def text_copy_to_clipboard(self):
        pyperclip.copy(text_textField2.value)
        row_Text_1.value = "Copiado!"
        row_Text_1.update()
    
    def file_section_set_text(self):
        text_textField4.value = generate_key(randomorg_key)
        text_textField4.update()
        
    def file_copy_to_clipboard(self):
        pyperclip.copy(text_textField4.value)
        row_Text_2.value = "Copiado!"
        row_Text_2.update()
    
    def process_message(self):
        if len(text_textField1.value) > 0:
            message = process_string(text_radio_1.value, text_radio_2.value, text_textField1.value, text_textField2.value)
            editable.value = message
            editable.update()
            
    def process_file_message(self):
        progress_bar.visible = True
        progress_bar.update()
        process_file(picked_file_path.value ,text_radio_3.value, text_radio_4.value, text_textField4.value, directory_path.value)
        progress_bar.visible = False
        progress_bar.update()
        
    with open(relative_path, "r") as file:
        data = load(file)
    
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
    text_radio_1.value = "encriptar"

    text_radio_2_text1 = Text("AES", size=default_size)
    text_radio_2_text2 = Text("Calíope", size=default_size)
    
    text_radio_2 = RadioGroup(content=Row([
        Radio(value="aes", label=""),
        text_radio_2_text1,
        Radio(value="calíope", label=""),
        text_radio_2_text2
    ]))
    text_radio_2.value = "aes"

    text_textField1 = TextField(
        width=500,
        height=273,
        multiline=True,
        min_lines=1,
        hint_text="Cadena de 128 bits",
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

    elevatedButton_1 = ElevatedButton(text="Generar", style=ButtonStyle(animation_duration=500))
    elevatedButton_1.on_click = text_section_set_text

    elevatedButton_2 = ElevatedButton(text="Copiar", style=ButtonStyle(animation_duration=500))
    elevatedButton_2.on_click = text_copy_to_clipboard
    
    row_Text_1 = Text(value="", color="green")
    
    operate_button_1 = ElevatedButton(text="Operar", style=ButtonStyle(animation_duration=500))
    operate_button_1.on_click = process_message

    tab1_content = Container(
        content=Column([
            separator_1,
            text_radio_1,
            separator_2,
            text_radio_2,
            text_textField2,
            Row([
                elevatedButton_1,
                elevatedButton_2,
                row_Text_1
            ]),
            Text("\n"),
            Row([
                text_textField1,
                operate_button_1,
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
    text_radio_3.value = "encriptar"

    text_radio_4_text1 = Text("AES", size=default_size)
    text_radio_4_text2 = Text("Calíope", size=default_size)
    
    text_radio_4 = RadioGroup(content=Row([
        Radio(value="aes"),
        text_radio_4_text1,
        Radio(value="calíope"),
        text_radio_4_text2
    ]))
    text_radio_4.value = "aes"

    text_textField4 = TextField(
        width=800,
        hint_text="Clave simétrica",
        text_size=default_size
    )

    pick_file_dialog = FilePicker(on_result=pick_files_result)
    selected_file = Text(value="Solo formato .txt", selectable=True)

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
    
    elevatedButton_3 = ElevatedButton(text="Generar", style=ButtonStyle(animation_duration=500))
    elevatedButton_3.on_click = file_section_set_text

    elevatedButton_4 = ElevatedButton(text="Copiar", style=ButtonStyle(animation_duration=500))
    elevatedButton_4.on_click = file_copy_to_clipboard
    
    row_Text_2 = Text(value="", color="green")
    
    operate_button_2 = ElevatedButton(text="Operar", style=ButtonStyle(animation_duration=500))
    operate_button_2.on_click = process_file_message

    progress_bar = ProgressBar(width=200, color="#9ecaff", bgcolor="#eeeeee")
    progress_bar.visible = False
    
    tab2_content = Container(
        content=Column([
            separator_3,
            text_radio_3,
            separator_4,
            text_radio_4,
            text_textField4,
            Row([
                elevatedButton_3,
                elevatedButton_4,
                row_Text_2
            ]),
            Text(""),
            file_picker,
            save_file,
            Text("\n"),
            Row([
                operate_button_2,
                Text("  "),
                progress_bar
            ])
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

    config_separator = Text("\nSobre la aplicación", size=default_size+4)

    config_separator_1 = Text("\nPrimera pestaña:", size=default_size+2)
    config_help_1 = Text("Solo se aceptan cadenas de 128 bits, es decir, 16 caracteres para encriptar y 16 en hexadecimal (es decir, 32 de longitud) para desencriptar.", size=default_size)
    
    config_separator_2 = Text("\nSegunda pestaña:", size=default_size+2)
    config_help_2 = Text("Solo se aceptan ficheros de texto cuyo contenido tenga una cantidad de caracteres múltiplo de 16. Esta aplicación no está destinada a codificar o descodificar cuando el texto no tenga tamaños múltiplos de 16. El propósito es demostrar que es viable su uso en términos de tiempo de ejecución.", size=default_size)

    tab3_content = Container(
        content=Column([
            theme_text,
            text_radio_5,
            Text("\n\n"),
            sample_text, 
            slider1,
            config_separator,
            config_separator_1,
            config_help_1,
            config_separator_2,
            config_help_2
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
