from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import ScrollView
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
from kivy.properties import StringProperty, DictProperty
from functools import partial

Window.size = (360,600)

class MD3Card(MDCard):
    '''Implements a material design v3 card.'''
    text = StringProperty()

class FreeMeal(MDApp):
    myText='init'
    categories = []
    image = ''
    meals = []
    category = ''
    details_meal = []

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        self.categories = self.get_categories()
        return Builder.load_file('free_meal.kv')
    
    def remove(self):
        self.root.ids.box.clear_widgets()

    def add_meal_detail(self, id_meal):
        self.root.ids.menu.clear_widgets()
        self.details_meal = self.get_details_meal(id_meal)
        print(self.details_meal)
        detail = self.details_meal[0]
        layout = MDGridLayout(
                    FitImage(
                        source= detail['strMealThumb'],
                        size_hint_y=None,
                        height='150dp'
                    ),
                    MDLabel(text=detail['strMeal']),
                    MDLabel( text=detail['strCategory']),
                    MDLabel(text=detail['strArea']),
                    MDLabel(
                    text='Instructions :'),
                    MDLabel(
                    text=detail['strInstructions']),
                    cols=1, spacing=10, size_hint_y=None,
                    pos_hint=(-1,1)
                )
        layout.bind(minimum_height=layout.setter('height'))
        r = ScrollView(
                    size_hint=(1, None), size=(Window.width, Window.height))
        r.add_widget(layout)
        self.root.ids.menu.add_widget(r)

    def add_meals(self, category):
        self.remove()
        self.meals = self.get_meals(category)
        for meal in self.meals:
            self.root.ids.box.add_widget(
                MDCard(
                     MDBoxLayout(
                        FitImage(
                            source= meal['strMealThumb'],
                            radius= [20, 20, 0, 0],
                            size_hint=(1,.5)
                        ),
                        MDBoxLayout(
                            MDLabel(
                                id='labelone',
                                text=meal['strMeal'],
                                padding=[7,7,0,0],
                                theme_text_color="Custom",
                                text_color=app.theme_cls.primary_color
                            ) ,
                            orientation='vertical',
                            pos_hint= {"bottom": 1},
                            adaptive_height= True,
                            size_hint=(1,.20),
                            md_bg_color= '#ede0c0',
                            radius= [0, 0, 20, 20 ],
                        ),
                        orientation='vertical',
                    ),
                    on_press= partial(self.on_meal_card_press,meal['idMeal']),
                    line_color=app.theme_cls.primary_color,
                    md_bg_color='#f8f5f4',
                    shadow_offset=(0, -1),
                    height='150dp',
                    size_hint=(1,None)
                )
            )
            
    def add_categories(self):
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
                                id='labelone',
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
                    on_press= partial(self.on_category_card_press,category['strCategory']),
                    line_color=app.theme_cls.primary_color,
                    md_bg_color='#f8f5f4',
                    shadow_offset=(0, -1),
                    height='250dp',
                    size_hint=(1,None)
                ),
            )

    def on_tab_press(self, args):
        print(type(args))
        print(args.name)
        print(args.text)
        print('tab pressed !')
        self.remove()
        self.add_categories()

    def on_category_card_press(self,category, args):
        self.add_meals(category)
        print('clicked !')

    def on_meal_card_press(self, id_meal, args):
        self.add_meal_detail(id_meal)

    def on_start(self):
        self.add_categories()

    def get_categories(self):
        try :
            url = 'https://www.themealdb.com/api/json/v1/1/categories.php'
            response = requests.get(url)
            x = response.json()
            #print(x)
            self.myText = x['categories'][0]['strCategory']
            self.categories = x['categories']
        except requests.ConnectionError:
            print('No Internet Connection!')
        return self.categories
    
    def get_meals(self, category):
        try:
            url = f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}'
            response = requests.get(url)
            x = response.json()
            self.meals = x['meals']
        except requests.ConnectionError:
            print('No Internet Connection!')
        return self.meals
    
    def get_details_meal(self, id_meal):
        try:
            url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={id_meal}'
            response = requests.get(url)
            x = response.json()
            self.details_meal = x['meals']
        except requests.ConnectionError:
            print('No Internet Connection!')
        return self.details_meal


app = FreeMeal()
app.run()
