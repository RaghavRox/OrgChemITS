import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from core.main import main
from core.imagetolines import LineScanner
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.button import Button
import os

class OrgChemITSApp(App):
    def build(self):
        return RootWidget()

class RootWidget(Widget):
    def __init__(self):
        super(RootWidget,self).__init__()
        self.welPage = WelcomePage()
        self.mainPage = MainPage()
        self.add_widget(self.welPage)
    
    def nextPage(self):
        self.remove_widget(self.welPage)
        self.add_widget(self.mainPage)
    


class MainPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.height = Window.height
        self.width = Window.width
        self.fileChooser = MaddaWidget()
        self.fileChooser.height = Window.height
        self.fileChooser.width = Window.width
        self.add_widget(self.fileChooser)
    
    def remFileChooser(self,imgPath):
        self.remove_widget(self.fileChooser)
        fuka = LineScanner.process_lines(imgPath)
        print(fuka)
        self.image =Image(source=fuka[0])
        self.image.height = Window.height
        self.image.width = Window.width
        self.add_widget(self.image)
        os.remove(fuka[0])
        self.add_widget(Label(text = main.mainAlgo(fuka[1]),font_size='50sp',color=[1,0,0,1]))

Builder.load_string("""
<MaddaWidget>:
    id: my_widget
    Button
        text: "open"
        on_release: my_widget.open(filechooser.path, filechooser.selection)
    FileChooserListView:
        id: filechooser
        on_selection: my_widget.selected(filechooser.selection)
""")

class MaddaWidget(BoxLayout):
    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print(f.read())

    def selected(self, filename):
        print ("selected: %s" % filename[0])
        self.parent.remFileChooser(filename[0])

class WelcomePage(BoxLayout):
    def __init__(self):
        super(WelcomePage,self).__init__()
        self.orientation = "vertical"
        self.height = Window.height
        self.width = Window.width

    def on_touch_down(self, touch):
        self.parent.nextPage()


if __name__ == "__main__" :
    OrgChemITSApp().run()
