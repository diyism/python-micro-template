import kivy
kivy.require('1.0.8')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

import python_micro_template

class ScrollViewApp(App):

    def build(self):
        kvml=open('example_kivy_scrollview.kvml', 'r').read()
        kvml=python_micro_template.tpl.parse(kvml)
        grid=Builder.load_string(kvml)
        grid.bind(minimum_height=grid.setter('height'))

        # create a scroll view, with a size < size of the grid
        root = ScrollView(size_hint=(None, None), size=(500, 320),
                pos_hint={'center_x': .5, 'center_y': .5}
                , do_scroll_x=False)
        root.add_widget(grid)

        return root

if __name__ == '__main__':

    ScrollViewApp().run()
