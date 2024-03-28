import json
from kivy import *
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

class SayHello(App):
    index = ["start"]
    data = ""
    def save_data(self):
        with open("data.json", "w") as outfile:
            json.dump(self.data, outfile, indent=4)
     
    def page_forward(self, instance):
        name = instance.text
        self.index.append(name)
        self.refresh_page()

    def page_back(self, instance):
        if len(self.index) == 1:
            return
        self.index.pop()
        self.refresh_page()
        pass

    def add_folder(self, instance):
        name = self.textinput.text
        json_data = self.data
        for step in self.index:
            json_data = json_data[step]
            json_data = json_data["content"]
        json_data[name] = {
            "info": "info",
            "content": {}
        }
        
        self.textinput.text = ""
        self.refresh_page()

    def add_item(self, instance):
        name = self.textinput.text
        json_data = self.data
        for step in self.index:
            json_data = json_data[step]
            json_data = json_data["content"]
        json_data[name] = "base"
        
        self.textinput.text = ""
        self.refresh_page()

    def refresh_page(self):
        self.middle_bar.clear_widgets()
        path = ""
        for step in self.index:
            path += step + "/"
        self.navbar.text = path
        self.add_widgets(self.get_buttons())

    def get_buttons(self):
        json_data = self.data
        for step in self.index:
            json_data = json_data[step]
            json_data = json_data["content"]
        arr = []
        for element in json_data:
            box = BoxLayout(orientation='horizontal',size_hint_y=None, height=40, spacing=10)
            button = Button(text=element, size_hint=(None, None), size=(100, 40))

            info_text = ""
            if isinstance(json_data[element], str):
                info_text = json_data[element]
            else:
                info_text = json_data[element]["info"]

            button2 = Button(text=info_text, size_hint=(None, None), size=(80, 30))
            box.add_widget(button)
            box.add_widget(button2)
            if not isinstance(json_data[element], str):
                button.background_color=(1, 0.9, 0.5, 1)
                button.bind(on_press=self.page_forward)
            arr.append(box)
        return arr

    def add_widgets(self, arr):
        for widget in arr:
            self.middle_bar.add_widget(widget)
        

    def build(self):

        with open('data.json', 'r') as f:
            self.data = json.load(f)
        
        self.main_layout = BoxLayout(orientation='vertical')

        # create top bar
        self.top_bar = GridLayout(cols=1, spacing=10, size_hint_y=None, height=100)
        self.navbar = Label(text="Welcome!", height=100, width=200)
        backbutton = Button(text="<", size_hint=(None, None), size=(50, 50))
        backbutton.bind(on_press=self.page_back)
        self.top_bar.add_widget(backbutton)
        self.top_bar.add_widget(self.navbar)

        self.main_layout.add_widget(self.top_bar)

        # create midsection
        self.middle_bar = GridLayout(cols=1, spacing=10)
        self.add_widgets(self.get_buttons())

        self.main_layout.add_widget(self.middle_bar)

        # create bottom bar
        bottom_height = 100
        self.bottom_bar = BoxLayout(orientation='horizontal',size_hint_y=None, height=bottom_height)
        self.textinput = TextInput(height=bottom_height, multiline=False)

        folderbutton = Button(text="add folder", size_hint_x=None, height=bottom_height, width=200)
        folderbutton.bind(on_press=self.add_folder)
        itembutton = Button(text="add item", size_hint_x=None, height=bottom_height, width=200)
        itembutton.bind(on_press=self.add_item)

        self.bottom_bar.add_widget(self.textinput)
        self.bottom_bar.add_widget(folderbutton)
        self.bottom_bar.add_widget(itembutton)
        self.main_layout.add_widget(self.bottom_bar)

        return self.main_layout

if __name__ == "__main__":
    app = SayHello()
    app.run()
    app.save_data()