__version__ = '0.1'

import org.renpy.android.PythonActivity;
from kivy.app import App
from os.path import exists
from kivy.uix.widget import Widget
from functools import partial
from kivy.uix.button import Button
from kivy.clock import Clock
#Access java classes from python
from jnius import autoclass, cast
#from android import activity, mActivity
#Scatter is used to zoom, rotate and other wise interact with widgets (Image in this case)
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from PIL import Image

Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')
Environment = autoclass('andoird.os.Environment')

class Picture(Scatter):
	source  = StringProperty(None)


class CatOrCheeseApp(App):
	def build(self):
		self.index = 0
		activity = autoclass('org.renpy.android.PythonActivity')
		activity.bind(on_activity_result=self.on_activity_result)

	def get_img_filename(self):
		while True:
			self.index += 1
			fn = (Environment.getExternalStorageDirectory.getPath() +
				'/catOrCheese{}.jpg'.format(self.index))
			if not exists(fn):
				return fn

	def take_picture(self):
		intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
		self.last_fn = self.get_img_filename()
		self.uri = Uri.parse('file://' + self.last_fn)
		self.uri = cast('android.os.Parcelable', self.uri)
		intent.putExtra(MediaStore.EXTRA_OUTPUT, self.uri)
		currentActivity = cast('android.app.Activity', PythonActivity.mActivity)
		currentActivity.startActivityForResult(intent,123)

	def on_activity_result(self, requestCode, resultCode, intent):
		if requestCode == 0x123:
			Clock.schedule_once(partial(self.add_picture, self.last_fn), 0)

	def add_picture(self, fn, *args):
		im = Image.open(fn)
		width, height = im.size
		im.thumbnail((width / 4, height / 4), Image.ANTIALIAS)
		im.save(fn, quality=95)
		self.root.add_widget(Picture(source=fn, center=self.root.center))

	def on_pause(self):
		return True

if __name__ == '__main__':
	CatOrCheeseApp().run()