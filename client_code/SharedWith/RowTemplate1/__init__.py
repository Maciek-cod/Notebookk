from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def remove_user_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to stop sharing with: {}?".format(self.item['name'])):
      self.parent.parent.parent.raise_event('x-stop_sharing_notebook_with_user', user=self.item) # How to change parent.parent.parent ???????? 
