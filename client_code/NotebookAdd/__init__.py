from ._anvil_designer import NotebookAddTemplate
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
from ..NoteEdit import NoteEdit

class NotebookAdd(NotebookAddTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.validator = validation.Validator()
    self.validator.require_text_field(self.new_notebook_text_box, self.name_missing_lbl)
    
  def new_notebook_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.save_new_notebook()

  def save_notebook_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_new_notebook()

  def new_notebook_text_box_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.new_notebook_text_box.focus()

  def save_new_notebook(self):
    if self.validator.is_valid():
      new_notebook_name = self.new_notebook_text_box.text
      new_notebook = anvil.server.call('save_new_notebook', new_notebook_name)
      get_open_form().content_panel.clear()
      get_open_form().content_panel.add_component(NoteEdit(note=None))
      get_open_form().refresh_notebooks()
      get_open_form().notebooks_panel.get_components()[0].notebook_name_link_click()
      self.raise_event('x-close-alert')
      Notification("",title=f'You successfully created {new_notebook["name"]}.', timeout=2).show()
    else:
      self.validator.show_all_errors()