from ._anvil_designer import NavBarTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ...NoteNew import NoteNew

class NavBar(NavBarTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
  def notebook_name_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.repeating_panel_1.items is None:
      self.repeating_panel_1.items = anvil.server.call('get_all_notes_in_the_notebook', self.item)
      if len(self.repeating_panel_1.items) == 0:
        pressed_new_note = alert(
          title=f"Notebook {self.item['name']} has no notes.",
          buttons=[("Create New Note", True), ("Cancel", False)])
        if pressed_new_note:
          get_open_form().content_panel.clear()
          get_open_form().content_panel.add_component(NoteNew())
        self.repeating_panel_1.items = None
    else:
      self.repeating_panel_1.items = None