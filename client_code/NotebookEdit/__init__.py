from ._anvil_designer import NotebookEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import validation
from ..Homepage.NavBar import NavBar

class NotebookEdit(NotebookEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

    self.notebooks_names_panel.items = anvil.server.call('get_all_notebooks')

    self.validator = validation.Validator()
    self.validator.require_text_field(self.new_notebook_text_box, self.name_missing_lbl)
    self.notebooks_names_panel.set_event_handler('x-delete-notebook', self.delete_notebook)
    
  def refresh_notebooks(self, **event_args):
    self.notebooks_names_panel.items = anvil.server.call('get_all_notebooks')

  def delete_notebook(self, notebook, **event_args):
    anvil.server.call('delete_notebook', notebook)
    get_open_form().content_panel.raise_event_on_children('x-refresh-notes', notebook=anvil.server.call('get_all_notebooks')[0])
    get_open_form().refresh_notebooks()
    self.refresh_notebooks()

  def new_notebook_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.new_notebook_text_box.visible = True
    self.save_notebook_button.visible = True
    self.cancel_button.visible = True
    self.new_notebook_button.visible = False

  def cancel_button_click(self, **event_args):
    """This method is called when the button is clicked"""    
    self.new_notebook_text_box.visible = False
    self.save_notebook_button.visible = False
    self.cancel_button.visible = False
    self.name_missing_lbl.visible = False
    self.new_notebook_button.visible = True
    self.new_notebook_text_box.text = ''

  def save_new_notebook(self):
    if self.validator.is_valid():
      new_notebook_name = self.new_notebook_text_box.text
      new_notebook = anvil.server.call('seve_new_notebook', new_notebook_name)
      self.refresh_notebooks()
      get_open_form().refresh_notebooks()
      get_open_form().notebooks_panel.get_components()[0].notebook_name_link_click()
      get_open_form().content_panel.raise_event_on_children('x-refresh-notes', notebook=anvil.server.call('get_all_notebooks')[0])
      self.new_notebook_text_box.text = ''
      self.new_notebook_text_box.visible = False
      self.save_notebook_button.visible = False
      self.cancel_button.visible = False
      self.new_notebook_button.visible = True
    else:
      self.validator.show_all_errors()

  def new_notebook_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.save_new_notebook()

  def save_notebook_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_new_notebook()

  def new_notebook_text_box_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.new_notebook_text_box.focus()