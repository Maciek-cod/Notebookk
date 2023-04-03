from ._anvil_designer import NoteEditTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# from HashRouting import routing
from anvil.js.window import Quill
import json


# @routing.route('', title='Notebook - Home')
# @routing.route('note', url_keys=['id'], title="Notebook - Notes")
class NoteEdit(NoteEditTemplate):
  def __init__(self, note_nr, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.notebooks_drop_down.items = anvil.server.call('get_all_notebook_names')
    
    element = anvil.js.get_dom_node(self.quill_editor)
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
      
    self.quill.keyboard.addBinding({
        'key': 'S',
        'shortKey': True
      }, self.handle_quill_keydown_ctrl_s)
    
    if not note_nr:
      self.item = anvil.server.call('get_the_last_note', anvil.server.call('get_all_notebooks')[0])
      self.quill.setContents(json.loads(self.item['content_json']))
    else:
      try:
        self.item = anvil.server.call('get_note_by_id', note_nr ) # self.url_dict['id'])
        self.quill.setContents(json.loads(self.item['content_json']))
      except:
        # the item doesn't exist!
        # routing.set_url_hash('', replace_current_url=True)
        # get_open_form().content_panel = NoteEdit()
        get_open_form().content_panel.clear()
        get_open_form().content_panel.add_component(NoteEdit())
        raise Exception(f"It looks like Note {self.url_dict['id']} doesn't exist")

    self.set_event_handler('x-refresh-notes', self.refresh_notes)
    
  def handle_quill_keydown_ctrl_s(self, event_name, els):
    self.save_button_click()
        
  def refresh_notes(self, notebook, **event_args):
    self.notebooks_drop_down.items = anvil.server.call('get_all_notebook_names')
    try:
      self.item = anvil.server.call('get_the_last_note', notebook)
      self.quill.setContents(json.loads(self.item['content_json']))
    except:
      self.item = anvil.server.call('get_the_last_note', notebook=anvil.server.call('get_all_notebooks')[0])
      self.quill.setContents(json.loads(self.item['content_json']))

  def delete_note_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to delete: {}?".format(self.item['title'])):
      to_delete_note = self.item
      notebook_of_deleted_note = to_delete_note['notebook']
      get_open_form().delete_note(note=to_delete_note)
      get_open_form().refresh_notebooks()
      self.refresh_notes(notebook_of_deleted_note)
        
  def save_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    note_edited = {}
    note_edited['title'] = 'New Note' if self.title_text_box.text.strip() == '' or self.title_text_box.text == None else self.title_text_box.text.strip()
    note_edited['notebook'] = self.notebooks_drop_down.selected_value
    note_edited['content_json'] = json.dumps(self.quill.getContents().ops)
    note_edited['content'] = self.quill.getText()
    anvil.server.call('update_note', self.item, note_edited)
    get_open_form().refresh_notebooks()
    
    # Aby zobaczyc co jest w srodku obiektu python uzyj 'dir()':
    # print(dir(get_open_form().notebooks_panel))
    # print(get_open_form().notebooks_panel.get_components()[0])
    
    get_open_form().notebooks_panel.get_components()[0].notebook_name_link_click()  
    self.refresh_data_bindings()
    Notification("",title=f"{note_edited['title']} saved!", timeout=2).show()