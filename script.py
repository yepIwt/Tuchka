#!/usr/bin/python

import confs
import vk_api.exceptions
class Driven_Main(object):

	__slots__ = ('config')

	def __init__(self):
		self.config = confs.Config()

	def make_new_cfg(self, token, passw):
		pass

d = Driven_Main()
if not d.config.data:
	token = input('New token: ')
	d.config.get_api(token)
	if type(d.config.api) == vk_api.exceptions.ApiError:
		print('Wrong api key!')
		print(d.config.api)
	else:
		passw = input('New cfg passw: ')
		d.config.new_cfg(token, passw)
		d.config.save()