from ._anvil_designer import SearchNotesTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..NoteEdit import NoteEdit
from anvil.js.window import Quill
import json

class SearchNotes(SearchNotesTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.note_panel.visible = False
    element = anvil.js.get_dom_node(self.quill_editor_panel)
    self.quill = Quill( element, {
          'modules': { 'toolbar': {
            'container': [
              [{'header': [1, 2, 3, 4, 5, 6, False]}],
              [{'color': []}, {'background': []}],
              ['bold', 'italic', 'underline', 'strike'],
              [{'list': 'ordered'}, {'list': 'bullet'}],
              [{'script': 'sub'}, {'script': 'super'}],
              [{'indent': '-1'}, {'indent': '+1'}],
              [{'direction': 'rtl'}],
              [{'align': []}],
              ['blockquote', 'code-block'],
              ['link', 'image'],
              ['clean']
            ]}},
          'theme': 'snow',
          'placeholder': 'Start typing here...'})
    
    self.quill.keyboard.addBinding({
        'key': 'S',
        'shortKey': True
        }, self.handle_quill_keydown_ctrl_s)

  def handle_quill_keydown_ctrl_s(self, event_name, els):
    self.save_button_click()
    
  def show_or_hide_editor(self, show):
    if show:
      self.note_panel.visible = True
      self.title_text_box.visible = True
      self.delete_note_button.visible = True
      self.save_button.visible = True
      self.updated_label.visible = True
      self.author_label.visible = True
      self.notebook_label.visible = True
      self.notebooks_drop_down.visible = True
      self.quill_editor_panel.visible = True
    else:
      self.note_panel.visible = False
      self.data_grid_1.visible = False
      self.title_text_box.visible = False
      self.delete_note_button.visible = False
      self.save_button.visible = False
      self.updated_label.visible = False
      self.author_label.visible = False
      self.notebook_label.visible = False
      self.notebooks_drop_down.visible = False
      self.quill_editor_panel.visible = False
  
  def show_searched_note(self, note, **event_args):    
    try:
      self.item = note
      # Check the permission the current user has
      editable = anvil.server.call('check_user_permission', note=self.item)
      if not editable:
        anvil.js.call('hideQuillToolbar')
        self.quill.enable(False)
        self.save_button.enabled = False
        self.delete_note_button.enabled = False
        self.notebooks_drop_down.enabled = False
      else:
        anvil.js.call('showQuillToolbar')
        self.quill.enable(True)
        self.save_button.enabled = True
        self.delete_note_button.enabled = True
        self.notebooks_drop_down.enabled = True
      self.quill.setContents(json.loads(self.item['content_json']))
      self.notebooks_drop_down.items = anvil.server.call('get_all_notebook_names')
      self.show_or_hide_editor(True)  
    except:
      self.show_or_hide_editor(False)

  def title_text_box_focus(self, **event_args):
    """This method is called when the TextBox gets focus"""
    if self.title_text_box.text == 'Title...':
      self.title_text_box.text = ''

  def close_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(NoteEdit(note=None))

  def search_text_box_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.search_text_box.focus()
    self.search_text_box.select()   
    
  def search_text_box_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if self.search_text_box.text.strip() == '' or self.search_text_box.text == None:
      self.show_or_hide_editor(False)
    else:
      result = anvil.server.call('search_notes', self.search_text_box.text)
      if result:
        self.repeating_panel_1.items = result
        self.data_grid_1.visible = True
      else:
        self.show_or_hide_editor(False)
        
  def delete_note_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to delete: {}?".format(self.item['title'])):
      get_open_form().delete_note(note=self.item)
      self.search_text_box_change()
      self.show_searched_note(self.repeating_panel_1.items[0])
      get_open_form().refresh_notebooks()

  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    note_edited = {}
    note_edited['title'] = 'New Note' if self.title_text_box.text.strip() == '' or self.title_text_box.text == None else self.title_text_box.text.strip()
    note_edited['notebook'] = self.notebooks_drop_down.selected_value
    note_edited['content_json'] = json.dumps(self.quill.getContents().ops)
    note_edited['content'] = self.quill.getText()
    anvil.server.call('update_note', self.item, note_edited)
    get_open_form().refresh_notebooks()
    self.search_text_box_change()
    Notification("",title=f"{note_edited['title']} saved!", timeout=2).show()