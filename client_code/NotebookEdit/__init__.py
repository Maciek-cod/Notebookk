from ._anvil_designer import NotebookEditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..SharedWith import SharedWith

class NotebookEdit(NotebookEditTemplate):
  def __init__(self, notebook, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = notebook
    if self.item['owner'] != anvil.users.get_user():
      self.edit_button.enabled = False
      self.delete_notebook_button.enabled = False

  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.notebook_name_label.visible = False
    self.edit_button.visible = False
    self.delete_notebook_button.visible = False
    self.shared_with_button.visible = False
    self.undo_button.visible = True
    self.notebook_name_text_box.visible = True
    self.update_notebook_name_button.visible = True

  def undo_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.notebook_name_text_box.visible = False
    self.update_notebook_name_button.visible = False
    self.undo_button.visible = False
    self.notebook_name_label.visible = True
    self.edit_button.visible = True
    self.delete_notebook_button.visible = True
    self.shared_with_button.visible = True

  def delete_notebook_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to delete: {} and all its notes?".format(self.item['name'])):
      notebook_name = self.item['name']
      get_open_form().raise_event('x-delete-notebook', notebook=self.item)
      self.raise_event("x-close-alert")
      Notification("",title=f'{notebook_name} is now gone.', timeout=2).show()

  def shared_with_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    shared_with_form = SharedWith(self.item, notebook_edit_form=None)
    alert(content=shared_with_form,
               title=f"{self.item['name']} Notebook",
               buttons=[])

  def update_notebook_name(self):
    updated_notebook = {'name': self.notebook_name_text_box.text}
    anvil.server.call('update_notebook', self.item, updated_notebook)
    self.refresh_data_bindings()
    get_open_form().refresh_notebooks()
    self.notebook_name_label.visible = True
    self.edit_button.visible = True
    self.delete_notebook_button.visible = True
    self.notebook_name_text_box.visible = False
    self.update_notebook_name_button.visible = False
    self.undo_button.visible = False
    self.shared_with_button.visible = True
    
  def update_notebook_name_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.update_notebook_name()

  def notebook_name_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.update_notebook_name()