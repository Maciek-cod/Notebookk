from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import SearchNotes

class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    column_panel_node = anvil.js.get_dom_node(self.column_panel_1)
    column_panel_node.addEventListener('click', self.handle_column_panel_click)
    column_panel_node.addEventListener('mouseover', self.handle_mouseover)
    column_panel_node.addEventListener('mouseout', self.handle_mouseout)

  def handle_mouseover(self, els, **event_args):
    column_panel_node = anvil.js.get_dom_node(self.column_panel_1)
    column_panel_node.style.cursor = "pointer"
    
  def handle_mouseout(self, els, **event_args):
    column_panel_node = anvil.js.get_dom_node(self.column_panel_1)
    column_panel_node.style.cursor = "default"

  def handle_column_panel_click(self, els, **event_args):
    self.note_name_link_click()
    
  def note_name_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    note = anvil.server.call('get_note_by_id', self.item)
    self.parent.parent.parent.show_searched_note(note=note) # BUT this one does??????