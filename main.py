from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import requests
from kivy.properties import StringProperty

class MD3Card(MDCard):
    '''Implements a material design v3 card.'''

    text = StringProperty()

class Test(MDApp):
    myText='init'
    categories = []

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_file('free_meal.kv')

    def on_start(self):
        print(len(self.categories))
        for category in self.categories:
            self.root.ids.box.add_widget(
                MD3Card(
                    MDLabel(text=category['strCategory']),
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    md_bg_color='#f8f5f4',
                    shadow_offset=(0, -1),
                    padding = '10dp',
                    size_hint=(1,None)
                )
            )
    
    def on_success(self, req, result):
        print('Got the result:')
        print(result)
        self.myText = 'result'

    def on_error(self, req, error):
        print('Got an error:')
        print(error)
    
    def get_data(self):
        req = UrlRequest('https://www.themealdb.com/api/json/v1/1/categories.php',
            self.on_success, self.on_error)
        while not req.is_finished:
            Clock.tick()

    def get_data_req(self):
        try :
            url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
            response = requests.get(url)
            x = response.json()
            print(x)
            self.myText = x['categories'][0]['strCategory']
            self.categories = x['categories']
        except requests.ConnectionError:
            print('No Internet Connection!')

class MyListView(BoxLayout):
    pass


app = Test()
app.get_data_req()
app.run()
