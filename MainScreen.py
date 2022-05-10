import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.button import MDFillRoundFlatIconButton, MDRectangleFlatIconButton, MDIconButton
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivy.properties import BooleanProperty
from plyer import filechooser
import filetype
import Model as md
import webbrowser
import pandas as pd 
df = pd.read_csv('wiki_flower.csv') 

class MainScreen(Screen):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		self.name_flower = ""
		self.link_flower = ""
		self.origin_flower = ""
		self.description_flower = ""
		self.background = self.create_background()
		self.switch_theme = self.create_change_theme()
		self.button_image = self.create_button_image()
		self.button_upload = self.create_button_upload()
		self.animation_center = self.create_animation_center()
		self.back_button_show = self.create_back_button()
		self.icon_right = self.create_icon_right()
		self.icon_left = self.create_icon_left()
		self.image = Image()
		self.add_widget(self.background)
		self.add_widget(self.animation_center)
		self.add_widget(self.button_image)
		self.add_widget(self.button_upload)
		self.add_widget(self.switch_theme)
		self.add_widget(self.icon_right)
		self.add_widget(self.icon_left)
		self.button_upload.bind(on_release = self.change_display_uploadflower)
		self.button_image.bind(on_release = self.change_display_showflower)
		self.switch_theme.bind(active = self.change_dark_light)

	#Tạo hình nền cho ứng dụng
	def create_background(self):
		self.background = Image()
		self.background.source = 'background_mainscreen.gif'
		self.background.size = self.size
		self.background.pos = self.pos
		self.background.anim_delay = 1 / 12
		self.background.allow_stretch = True
		self.background.keep_ratio = False
		self.background.keep_data = True 
		return self.background

	#Tạo nút vào màn hình camera
	def create_button_image(self):
		self.button_image = MDFillRoundFlatIconButton()
		self.button_image.text = "      Open Camera"
		self.button_image.icon = "camera"
		self.button_image.size_hint = (.2, .1)
		self.button_image.pos_hint = {"center_x": .5, "center_y": .35}
		return self.button_image

	#Tạo nút tải hình ảnh lên
	def create_button_upload(self):
		self.button_upload = MDFillRoundFlatIconButton()
		self.button_upload.text = "      Upload Image"
		self.button_upload.icon = "upload"
		self.button_upload.size_hint = (.2, .1)
		self.button_upload.pos_hint = {"center_x": .5, "center_y": .2}
		return self.button_upload

	#Tạo ảnh động (chạy xe đạp) ở giữa màn hình chính
	def create_animation_center(self):
		self.animation_center = Image()
		self.animation_center.source = "anim_center.gif"
		self.animation_center.anim_delay = 1 / 7
		self.animation_center.size_hint = (.6, .55)
		self.animation_center.pos_hint = {"center_x": .5, "center_y": .65}
		return self.animation_center

	def create_change_theme(self):
		self.switch_theme = MDSwitch()
		self.switch_theme.pos_hint = {"right": .918, "top": .95}
		return self.switch_theme

	def create_icon_right(self):
		self.icon_right = MDIconButton()
		self.icon_right.icon = "theme-light-dark"
		self.icon_right.size_hint = (.06, .07)
		self.icon_right.pos_hint = {"right": .99, "top": .95}
		self.icon_right.allow_stretch = True
		self.icon_right.keep_ratio = False
		return self.icon_right

	def create_icon_left(self):
		self.icon_left = Image()
		self.icon_left.source = "iconleft.png"
		self.icon_left.size_hint = (.15, .2)
		self.icon_left.pos_hint = {"left": 1, "top": 1}
		self.icon_left.allow_stretch = True
		self.icon_left.keep_ratio = False
		self.icon_left.keep_data = True 
		return self.icon_left
		
	def change_dark_light(self, checkbox, value):
		if value:
			Camera2H().theme_cls.theme_style = "Dark"
		else:
			Camera2H().theme_cls.theme_style = "Light"

	def change_display_showflower(self, event):
		self.manager.current = "showflower"

	def change_display_uploadflower(self, event):
		filechooser.open_file(on_selection = self.select_file)

	def select_file(self, filename):
		if filetype.is_image(filename[0]) == False:
			filechooser.open_file(on_selection = self.select_file)
		else:
			self.model_path = 'model.ckpt'
			self.file_path = filename[0]
			print(self.file_path)
			clss, classname = md.test_model(self.file_path, self.model_path)
			for i in range(df.shape[0]):
				if df.iloc[i, 0] == classname:
					self.name_flower = df.iloc[i, 0]
					self.link_flower = df.iloc[i, 1]
					self.origin_flower = df.iloc[i, 2]
					self.description_flower = df.iloc[i, 3]
					self.image.source = f'{self.file_path}'
					self.image.size_hint = (.3, .3)
					self.image.pos_hint = {"center_x": .5, "y": .62}
					self.image.allow_stretch = True
					self.image.keep_ratio = False
					self.text_flower = self.create_text_flower()
					self.origin = self.create_origin_flower()
					self.description = self.create_description_flower()
					self.remove_widget(self.animation_center)
					self.remove_widget(self.button_image)
					self.remove_widget(self.button_upload)
					self.remove_widget(self.switch_theme)
					self.remove_widget(self.icon_right)
					self.remove_widget(self.icon_left)
					self.show_flower()
					break

	def create_text_flower(self):
		self.box_flower = MDRectangleFlatIconButton()
		self.box_flower.text = "The flower is:  " + str(self.name_flower.capitalize())
		self.box_flower.icon = "flower"
		self.box_flower.theme_text_color = "Custom"
		self.box_flower.text_color = 186/255, 85/255, 211/255, 1
		self.box_flower.size_hint = (.26, .1)
		self.box_flower.pos_hint = {"center_x": .5, "y": .5}
		return self.box_flower

	def create_back_button(self):
		self.back_button = MDIconButton()
		self.back_button.icon = "arrow-left-bold-circle-outline"
		self.back_button.user_font_size = "45sp"
		self.back_button.pos_hint = {"left": .8, "top": .95}
		self.back_button.allow_stretch = True
		self.back_button.keep_ratio = False
		return self.back_button

	def create_origin_flower(self):
		self.origin = MDLabel()
		self.origin.text = "Xuất xứ: " + str(self.origin_flower)
		self.origin.theme_text_color = "Custom"
		self.origin.text_color = 60/255, 179/255, 113/255, 1
		self.origin.size_hint = (.5, .6)
		self.origin.pos_hint = {"center_x": .5, "center_y": .43}
		return self.origin

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
		self.add_widget(self.text_flower)
		self.add_widget(self.origin)
		self.add_widget(self.description)
		self.add_widget(self.back_button_show)
		self.text_flower.bind(on_release = self.create_wiki_flower)
		self.back_button_show.bind(on_release = self.back_mainscreen)

	def back_mainscreen(self, event):
		self.remove_widget(self.image)
		self.remove_widget(self.text_flower)
		self.remove_widget(self.origin)
		self.remove_widget(self.description)
		self.remove_widget(self.back_button_show)
		self.add_widget(self.animation_center)
		self.add_widget(self.button_image)
		self.add_widget(self.button_upload)
		self.add_widget(self.switch_theme)
		self.add_widget(self.icon_right)
		self.add_widget(self.icon_left)

	def create_wiki_flower(self, event):
		webbrowser.open(f'{self.link_flower}', new = 2)


class Camera2H(MDApp):
	def build(self):
		return MainScreen()
