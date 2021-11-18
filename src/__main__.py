import kivy
from kivy.app import App
from kivy.uix.label import Label
from core.main import main

class MyApp(App):
    def build(self):
        return Label(text = main.mainAlgo([[0,0,1,1],[2,0,1,1]]))


if __name__ == "__main__" :
    MyApp().run()