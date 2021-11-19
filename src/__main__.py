# import kivy
# from kivy.app import App
# from kivy.uix.label import Label
from core.main import main

# class MyApp(App):
#     def build(self):
#         return Label(text = main.mainAlgo([[0,0,1,1],[2,0,1,1]]))


# if __name__ == "__main__" :
#     MyApp().run()

testCompounds = [[[0,0,1,1],[2,0,1,1],[2,0,5,5]]]

# for node in main.mainAlgo(testCompounds[0]):
#     print(node.getCords())
#     x = node.getConnectedNodes()
#     for lol in x:
#         print(lol.getCords())
#     print("next node")

print(main.mainAlgo(testCompounds[0]))