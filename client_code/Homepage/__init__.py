from ._anvil_designer import HomepageTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil.js.window import location

from ..NoteNew import NoteNew
from ..NoteEdit import NoteEdit
from ..NotebookAdd import NotebookAdd
from ..SearchNotes import SearchNotes
from ..WelcomeAlert import WelcomeAlert
from ..About import About
from ..Help import Help

class Homepage(HomepageTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    anvil.users.login_with_form()
    current_user = anvil.users.get_user()
    if current_user['name'] == None:
      alert(content=WelcomeAlert(),
            buttons=[],
            dismissible=False)

    self.item = current_user
    self.notebooks_panel.items = anvil.server.call('get_all_notebooks')
    self.content_panel.clear()
    self.content_panel.add_component(NoteEdit(note=None))
    self.set_event_handler('x-delete-notebook', self.delete_notebook)
    
  def refresh_notebooks(self):
    self.notebooks_panel.items = anvil.server.call('get_all_notebooks')
    
  def edit_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert(content=NotebookAdd(),
          title="Add Notebook",
          large=True,
          buttons=[])
    
  def about_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(About())

  def help_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Help())

  def new_note_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(NoteNew())
    
  def search_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(SearchNotes())

  def log_out_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    location.href = ""
  
  def delete_note(self, note, **event_args):
    note_deleted = note['title']
    anvil.server.call('delete_note', note)
    Notification("",title=f"{note_deleted} is gone!", timeout=2).show()

  def delete_notebook(self, notebook, **event_args):
    anvil.server.call('delete_notebook', notebook)
    self.content_panel.clear()
    self.content_panel.add_component(NoteEdit(note=None))
    self.refresh_notebooks()