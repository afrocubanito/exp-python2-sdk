
import unittest

from . import utils

class Test(utils.Device, utils.ResourceBase):

  get_name = 'get_data'
  find_name = 'find_data'
  create_name = 'create_data'
  class_ = utils.api.Data

  def create_valid (self):
    return self.create(group=self.generate_name(), key=self.generate_name(), value={ 'test': self.generate_name() })

  def create (self, group=None, key=None, value=None):
    return self.exp.create_data(group, key, value)

  def test_find (self):
    data = self.create_valid()
    [self.assert_isinstance(data) for data in self.find()]
    items = self.find({ 'group': data.group })
    if not data.key in [item.key for item in items]:
      raise Exception
    self.assert_isinstance(items[0])

  def test_create (self):
    data = self.exp.create_data('cats', 'fluffy', { 't': 'meow1' })
    if data.key != 'fluffy' or data.group != 'cats' or data.value['t'] != 'meow1':
      raise Exception

  def test_update (self):
    data = self.create_valid()
    data.value = { 'test2': 'a' }
    data.save()
    data = self.exp.get_data(data.group, data.key)
    if data.value['test2'] != 'a':
      raise Exception

  def test_delete (self):
    data = self.create_valid()
    key = data.key
    group = data.group
    data.delete()
    if self.exp.get_data(group, key):
      raise Exception
    data = self.create_valid()
    key = data.key
    group = data.group
    self.exp.delete_data(group, key)
    if self.exp.get_data(group, key):
      raise Exception
