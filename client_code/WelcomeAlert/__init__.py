from ._anvil_designer import WelcomeAlertTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import validation

class WelcomeAlert(WelcomeAlertTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.validator = validation.Validator()
    self.validator.require_text_field(self.name_text_box, self.name_error_lbl)

  def save_user_name(self, **event_args):
    if self.validator.is_valid():
      anvil.server.call('save_user_name', self.name_text_box.text.strip())
      anvil.server.call('create_notebook_with_welcoming_note')
      self.raise_event("x-close-alert")
    else:
      self.validator.show_all_errors()
      
  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.save_user_name()

  def name_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.save_user_name()
