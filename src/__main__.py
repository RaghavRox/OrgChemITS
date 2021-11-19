# import kivy
# from kivy.app import App
# from kivy.uix.label import Label
from core.main import main

# class MyApp(App):
#     def build(self):
#         return Label(text = main.mainAlgo([[0,0,1,1],[2,0,1,1]]))


# if __name__ == "__main__" :
#     MyApp().run()

testCompounds = [[[0,0,1,1],[1,1,2,2],[1,1,1,0],[1,0,3,2],[1,0,3,1]],[[0,0,1,1]],[[0,0,1,1],[2,0,1,1]],[[0,0,1,1],[2,0,1,1],[2,0,5,5]],[[0,0,1,1],[2,0,1,1],[2,0,5,5],[5,5,9,9]],[[0,0,1,1],[2,0,1,1],[2,0,5,5],[5,5,9,9],[6,7,9,9]],[[0,0,1,1],[2,0,1,1],[2,0,5,5],[5,5,9,9],[6,7,9,9],[5,5,12,12]],[[0,0,1,1],[2,0,1,1],[2,0,5,5],[5,5,9,9],[6,7,9,9],[5,5,12,12],[5,5,78,78]]]

# for node in main.mainAlgo(testCompounds[len(testCompounds)-1]):
#     print(node.getCords())
#     x = node.getConnectedNodes()
#     for lol in x:
#         print(lol.getCords())
#     print("next node")

for test in testCompounds:
    print(main.mainAlgo(test))