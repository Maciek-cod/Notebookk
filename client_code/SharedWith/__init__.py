from ._anvil_designer import SharedWithTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# from HashRouting import routing
from ..NotebookEdit import NotebookEdit

class SharedWith(SharedWithTemplate):
  def __init__(self, notebook, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.notebook = notebook
    self.open_alert()

    self.add_event_handler('x-stop_sharing_notebook_with_user', self.stop_sharing_notebook_with_user)
    
  def open_alert(self, **event_args):
    if self.notebook['owner'] != anvil.users.get_user():
      self.shared_by_other_user_lbl.text = f'This Notebook is shared with you by {self.notebook["owner"]["name"]}. Only the owner of the notebook can share it.'
      self.shared_by_other_user_lbl.visible = True
      self.leave_button.visible = True
      self.members_label.visible = True
      self.members_repeating_panel.items = self.notebook['users']
      self.is_shared_with_lbl.visible = False
      self.not_shared_yet_label.visible = False
      self.share_with_text_box.visible = False
      self.share_button.visible = False
    else:
      self.members_label.visible = False
      self.shared_by_other_user_lbl.visible = False
      self.leave_button.visible = False
      self.members_repeating_panel.items = None
      users = []
      for user in self.notebook['users']:
        if user != anvil.users.get_user(): 
          users.append(user)
      if users == []:
        self.not_shared_yet_label.visible = True
        self.is_shared_with_lbl.visible = False
        self.repeating_panel_1.items = None
      else:
        self.not_shared_yet_label.visible = False
        self.is_shared_with_lbl.visible = True
        self.repeating_panel_1.items = users
    
  def share_with_text_box_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.share_with_text_box.focus()

  def check_if_user_exist(self):
    user_exist = anvil.server.call('find_user', self.share_with_text_box.text)
    if user_exist:
      # if current_user try to share notebook with himself 
      if user_exist == anvil.users.get_user():
        self.user_in_notebook_label.text = 'You can’t share this notebook with yourself.'
        self.user_in_notebook_label.visible = False
        self.invalid_name_lbl.visible = False
        self.share_with_text_box.text = ''
        return user_exist
      else:
        self.user_in_notebook_label.text = f'You sharing this notebook with {self.share_with_text_box.text} already.'
        self.user_in_notebook_label.visible = False
        self.invalid_name_lbl.visible = False
        self.share_with_text_box.text = ''
        return user_exist
    else:
      self.invalid_name_lbl.visible = True
      self.user_in_notebook_label.visible = False
      return False

  def check_if_user_is_not_sharing_the_notebook_already(self, user, notebook):
    for u in notebook['users']:
      if user == u:
        return True
    return False
  
  def add_user_to_notebook_users(self, user):
    anvil.server.call('add_user_to_notebook_users', self.notebook, user)
    alert(f'You successfully shared {self.notebook["name"]} with {user["name"]}')
    self.open_alert()
    
  def share_with_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    user = self.check_if_user_exist()
    if user:
      sharing = self.check_if_user_is_not_sharing_the_notebook_already(user, self.notebook)
      if sharing:
        self.user_in_notebook_label.visible = True
      else:
        self.add_user_to_notebook_users(user)

  def share_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    user = self.check_if_user_exist()
    if user:
      sharing = self.check_if_user_is_not_sharing_the_notebook_already(user, self.notebook)
      if sharing:
        self.user_in_notebook_label.visible = True
      else:
        self.add_user_to_notebook_users(user)

  def leave_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to leave: {}?".format(self.notebook['name'])):
      anvil.server.call('remove_user_from_the_notebook_users', self.notebook)
      # routing.reload_page(hard=True)
      self.members_label.visible = False
      self.leave_button.visible = False
      self.members_repeating_panel.items = None
      get_open_form().refresh_notebooks()
      get_open_form().content_panel.raise_event_on_children('x-refresh-notes', notebook=None)
      self.shared_by_other_user_lbl.text = f'You are no longer an user of {self.notebook["name"]} shared by {self.notebook["owner"]["name"]}.'
      # get_open_form().close_alert() How to refresh notebooks on NotebookEdit????????????????
      

  def stop_sharing_notebook_with_user(self, user, **event_args):
    anvil.server.call('stop_sharing_notebook_with_user', self.notebook, user)
    self.user_in_notebook_label.visible = False
    self.open_alert()