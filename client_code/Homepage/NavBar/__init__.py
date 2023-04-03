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
# from HashRouting import routing

class NavBar(NavBarTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
  def notebook_name_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    if self.repeating_panel_1.items is None:
      self.repeating_panel_1.items = anvil.server.call('get_all_notes_in_the_notebook', self.item)
      if len(self.repeating_panel_1.items) == 0:
        pressed_new_note = alert(
          title=f"Notebook {self.item['name']} has no notes.",
          buttons=[("Create New Note", True), ("Cancel", False)])
        if pressed_new_note:
          # routing.set_url_hash('new-note')
          # get_open_form().content_panel = NoteNew()
          get_open_form().content_panel.clear()
          get_open_form().content_panel.add_component(NoteNew())
        self.repeating_panel_1.items = None
    else:
      self.repeating_panel_1.items = None
