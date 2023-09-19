from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.image import AsyncImage, Image
from kivy.loader import Loader
from kivy.clock import Clock


class TestApp(MDApp):
    '''Demonstrate the mechanics of managing asynchronous image loading'''
    
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)

    def _image_loaded(self, proxyImage):
        '''Fired once the image is loaded and ready to use'''
        if proxyImage.image.texture:
            self.image.texture = proxyImage.image.texture

    def _cancel_loading(self, dt):
        '''Stop the image from loading'''
        Loader.stop()  # It looks like this would stop all other
                       # ProxyImages loading too.

    def build(self):
        '''Build and return the main Image widget'''
        proxyImage = Loader.image("https://www.themealdb.com/images/category/breakfast.png")
        proxyImage.bind(on_load=self._image_loaded)
        self.image = Image()

        # Uncomment the line below to close the background loading threads
        # Clock.schedule_once(self._cancel_loading, 0.1)
        return self.image

#if __name__ == '__main__':
#    TestApp().run()