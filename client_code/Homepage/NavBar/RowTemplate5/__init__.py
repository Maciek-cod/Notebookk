from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# from HashRouting import routing
from ....NoteEdit import NoteEdit

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def note_title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().new_note_button.visible = True
    get_open_form().search_button.visible = True
    get_open_form().content_panel.raise_event_on_children('x-clear-input-fields')
    # routing.set_url_hash(f'note?id={self.item["id"]}')
    # get_open_form().content_panel = NoteEdit(self.item["id"])
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(NoteEdit(self.item["id"]))


