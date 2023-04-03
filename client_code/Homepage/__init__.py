from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..NoteNew import NoteNew
from ..NoteEdit import NoteEdit
from ..NotebookEdit import NotebookEdit
from ..SearchNotes import SearchNotes
from ..WelcomeAlert import WelcomeAlert


class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # New user reqire a name
    anvil.users.login_with_form()
    current_user = anvil.users.get_user()
    if current_user['name'] == None:
      alert(content=WelcomeAlert(),
            buttons=[],
            dismissible=False)
      
    self.notebooks_panel.items = anvil.server.call('get_all_notebooks')

    self.content_panel.clear()
    self.content_panel.add_component(NoteEdit(note_nr=None))
    
  def refresh_notebooks(self):
    self.notebooks_panel.items = anvil.server.call('get_all_notebooks')

  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(
      content=NotebookEdit(),
      title="Edit Notebooks",
      large=True,
      buttons=[])
    
  def new_note_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(NoteNew())
    
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(SearchNotes())

  def delete_note(self, note, **event_args):
    note_deleted = note['title']
    anvil.server.call('delete_note', note)
    Notification("",title=f"{note_deleted} is gone!", timeout=2).show()