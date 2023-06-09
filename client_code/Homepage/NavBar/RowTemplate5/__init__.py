from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....NoteEdit import NoteEdit

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    self.init_components(**properties)

  def note_title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(NoteEdit(self.item))