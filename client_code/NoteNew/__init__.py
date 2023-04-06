from ._anvil_designer import NoteNewTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.js.window import Quill
from .. import validation
import json
from ..NoteEdit import NoteEdit

class NoteNew(NoteNewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.notebooks_drop_down.items = anvil.server.call('get_all_notebook_names')
    current_user = anvil.users.get_user()
    
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
        'placeholder': 'Start typing here...'
    })
    
    json_string_z_bazy = '[{"insert":"\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n\\n"}]'
    deltas_z_bazy = json.loads(json_string_z_bazy)
    self.quill.setContents(deltas_z_bazy)
    
    self.validator = validation.Validator()
    self.validator.require_text_field(self.title_text_box, self.title_missing_lbl)
    self.validator.require(self.notebooks_drop_down, ['change'],
                            lambda notebook_picker: notebook_picker.selected_value is not None,
                            self.notebook_missing_lbl)

    self.quill.keyboard.addBinding({
          'key': 'S',
          'shortKey': True
          }, self.handle_quill_keydown_ctrl_s)

  def handle_quill_keydown_ctrl_s(self, event_name, els):
    self.save_button_click()

  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.validator.is_valid():
      new_note = {'title': self.title_text_box.text.strip(), 
                  'content': self.quill.getText(),
                  'content_json': json.dumps(self.quill.getContents().ops), 
                  'notebook': self.notebooks_drop_down.selected_value}
      anvil.server.call('save_new_note', new_note)
      get_open_form().refresh_notebooks()
      get_open_form().notebooks_panel.get_components()[0].notebook_name_link_click()
      get_open_form().content_panel.clear()
      get_open_form().content_panel.add_component(NoteEdit(note=None))
    else:
      self.validator.show_all_errors()

  def title_text_box_show(self, **event_args):
    """This method is called when the TextBox is shown on the screen"""
    self.title_text_box.focus()

  def go_back_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().content_panel.clear()
    get_open_form().content_panel.add_component(NoteEdit(note=None))