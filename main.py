import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
import MainScreen as ms 
import ShowFlower as sf 


class WindowsManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowsManager, self).__init__(**kwargs)


class Camera2H(MDApp):
	def build(self):
		screenmanager = ScreenManager()
		screenmanager.transition = FadeTransition()
		screenmanager.add_widget(ms.MainScreen(name = "mainscreen"))
		screenmanager.add_widget(sf.ShowFlower(name = "showflower"))
		return screenmanager

Camera2H().run()

