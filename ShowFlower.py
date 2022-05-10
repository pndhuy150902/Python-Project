import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy_garden.xcamera import XCamera
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatIconButton, MDIconButton, MDFloatingActionButton
import Model as md
import webbrowser
import os
import pandas as pd 
df = pd.read_csv('wiki_flower.csv') 


class ShowFlower(Screen):
	def __init__(self, **kwargs):
		super(ShowFlower, self).__init__(**kwargs)
		self.name_flower = ""
		self.link_flower = ""
		self.origin_flower = ""
		self.description_flower = ""
		self.camera = XCamera()
		self.image = Image()
		self.add_widget(self.camera)
		self.background = self.create_background()
		self.text_flower = self.create_text_flower()
		self.back_button_show = self.create_back_button()
		self.back_button_camera = self.create_back_button()
		self.add_widget(self.back_button_camera)
		self.back_button_camera.bind(on_release = self.from_camera_to_main)
		self.camera.on_picture_taken = self.picture_taken

	#Lấy đường dẫn file hình
	def picture_taken(self, filename):
		model_path = 'model.ckpt'
		file_path = os.path.dirname(os.path.abspath(filename)) + "/" + filename
		str_file_path = '{}'.format(file_path)
		clss, classname = md.test_model(str_file_path,model_path)
		self.image.source = str_file_path
		self.image.size_hint = (.3, .3)
		self.image.pos_hint = {"center_x": .5, "y": .62}
		self.image.allow_stretch = True
		self.image.keep_ratio = False
		for i in range(df.shape[0]):
			if (df.iloc[i, 0] == classname):
				self.name_flower = df.iloc[i, 0]
				self.link_flower = df.iloc[i, 1]
				self.origin_flower = df.iloc[i, 2]
				self.description_flower = df.iloc[i, 3]
				print(self.name_flower)
				print(self.link_flower)
				self.text_flower = self.create_text_flower()
				self.origin = self.create_origin_flower()
				self.description = self.create_description_flower()
				self.remove_widget(self.back_button_camera)
				self.remove_widget(self.camera)
				self.show_flower()
				break

	#Tạo ra khung in tên loài hoa 
	def create_text_flower(self):
		self.box_flower = MDRectangleFlatIconButton()
		self.box_flower.text = "The flower is:  " + str(self.name_flower.capitalize())
		self.box_flower.icon = "flower"
		self.box_flower.theme_text_color = "Custom"
		self.box_flower.text_color = 186/255, 85/255, 211/255, 1
		self.box_flower.size_hint = (.26, .1)
		self.box_flower.pos_hint = {"center_x": .5, "y": .5}
		return self.box_flower 

	#Tạo ra khung in xuất xứ của loài hoa
	def create_origin_flower(self):
		self.origin = MDLabel()
		self.origin.text = "Xuất xứ: " + str(self.origin_flower)
		self.origin.theme_text_color = "Custom"
		self.origin.text_color = 60/255, 179/255, 113/255, 1
		self.origin.size_hint = (.5, .6)
		self.origin.pos_hint = {"center_x": .5, "center_y": .43}
		return self.origin

	#Tạo ra khung in mô tả của loài hoa
	def create_description_flower(self):
		self.description = MDLabel()
		self.description.text = "Mô tả: " + str(self.description_flower)
		self.description.theme_text_color = "Custom"
		self.description.text_color = 60/255, 179/255, 113/255, 1
		self.description.size_hint = (.5, .7)
		self.description.pos_hint = {"center_x": .5, "center_y": .2}
		return self.description

	def show_flower(self):
		self.add_widget(self.image)
		self.add_widget(self.background)
		self.add_widget(self.text_flower)
		self.add_widget(self.origin)
		self.add_widget(self.description)
		self.add_widget(self.back_button_show)
		self.text_flower.bind(on_release=self.create_wiki_flower)
		self.back_button_show.bind(on_release=self.from_show_to_main)

	#Tạo ra khung in đường dẫn wikipedia của loài hoa đó
	def create_wiki_flower(self, event):
		webbrowser.open(f'{self.link_flower}', new = 2)

	#Tạo hình nền cho màn hình hiển thị loài hoa đã dự đoán 
	def create_background(self):
		self.background = Image()
		self.background.source = "background_mainscreen.gif"
		self.background.size = self.size
		self.background.pos = self.pos
		self.background.anim_delay = 1 / 12
		self.background.allow_stretch = True 
		self.background.keep_ratio = False 
		self.background.keep_data = True
		return self.background

	def create_back_button(self):
		self.back_button = MDIconButton()
		self.back_button.icon = "arrow-left-bold-circle-outline"
		self.back_button.user_font_size = "45sp"
		self.back_button.pos_hint = {"left": .8, "top": .95}
		self.back_button.allow_stretch = True
		self.back_button.keep_ratio = False
		return self.back_button

	def create_icon_change_camera(self):
		self.icon_change = MDFloatingActionButton()
		self.icon_change.icon = "camera-retake"
		self.icon_change.user_font_size = "35sp"
		self.icon_change.pos_hint = {"right": .95, "top": .94}
		self.icon_change.allow_stretch = True
		self.icon_change.keep_ratio = False
		self.icon_change.md_bg_color = Camera2H().theme_cls.primary_color
		return self.icon_change

	def from_show_to_main(self, event):
		self.remove_widget(self.image)
		self.remove_widget(self.background)
		self.remove_widget(self.back_button_show)
		self.remove_widget(self.text_flower)
		self.remove_widget(self.origin)
		self.remove_widget(self.description)
		self.add_widget(self.camera)
		self.add_widget(self.back_button_camera)
		self.manager.current = "mainscreen"

	def from_camera_to_main(self, event):
		self.remove_widget(self.camera)
		self.remove_widget(self.back_button_camera)
		self.change_main()

	def change_main(self):
		self.add_widget(self.camera)
		self.add_widget(self.back_button_camera)
		self.manager.current = "mainscreen"

class Camera2H(MDApp):
    def build(self):
        return ShowFlower()
