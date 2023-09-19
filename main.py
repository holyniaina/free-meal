from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivymd.uix.fitimage.fitimage import FitImage
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.core.window import Window
from kivy.loader import Loader
from kivy.clock import Clock
from test import TestApp
import requests
from kivy.properties import StringProperty

Window.size = (360,600)

class MD3Card(MDCard):
    '''Implements a material design v3 card.'''

    text = StringProperty()

class FreeMeal(MDApp):
    myText='init'
    categories = []
    image = ''

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        self.categories = self.get_data_req()
        return Builder.load_file('free_meal.kv')
    
    def on_category_card_pressed(self,*args):
        print('clicked')

    def on_start(self):
        for category in self.categories:
            self.root.ids.box.add_widget(
                MD3Card(
                    MDBoxLayout(
                        FitImage(
                            source= category['strCategoryThumb'],
                            radius= [20, 20, 0, 0],
                            size_hint=(1,.5)
                        ),
                        MDBoxLayout(
                            MDLabel(
                                text=category['strCategory'],
                                padding=[7,7,0,0],
                                theme_text_color="Custom",
                                text_color=app.theme_cls.primary_color
                            ) ,
                            MDLabel(
                                text=category['strCategoryDescription'][:50]+' ...',
                                padding='7dp'
                            ),
                            orientation='vertical',
                            pos_hint= {"bottom": 1},
                            adaptive_height= True,
                            size_hint=(1,.5),
                            md_bg_color= '#ede0c0',
                            radius= [0, 0, 20, 20 ],
                        ),
                        orientation='vertical',
                    ),
                    line_color=app.theme_cls.primary_color,
                    md_bg_color='#f8f5f4',
                    shadow_offset=(0, -1),
                    height='250dp',
                    size_hint=(1,None)
                )
            )

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
        return self.categories

class MyListView(MDBoxLayout):
    def on_category_card_pressed(self,*args):
        print('clicked')


app = FreeMeal()
app.run()
