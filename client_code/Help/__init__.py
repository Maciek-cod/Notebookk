from ._anvil_designer import HelpTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from anvil.js.window import Quill
import json

from ..NoteEdit import NoteEdit

class Help(HelpTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
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
        'placeholder': 'Start typing here...' })

  def send_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.email.send(
    to="maciek.anywhere@gmail.com",
    subject="Issue/bug Notebook anvil",
    text=self.quill.getText()
  )
    # issue_note = {}
    # issue_note['title'] = 'Issue/bug'
    # try:
    #   issue_note['notebook'] = anvil.server.call('get_issue_notebook')
    #   issue_note['content_json'] = json.dumps(self.quill.getContents().ops)
    #   issue_note['content'] = self.quill.getText()
    #   anvil.server.call('save_new_note', issue_note)
    #   get_open_form().content_panel.clear()
    #   get_open_form().content_panel.add_component(NoteEdit(note=None))
    #   alert(
    #     title="Thanks for your feedback. I'll address this issue promptly and make sure it's resolved as soon as possible.",
    #     content=self.quill.getText()
    #   )
    # except:
    #   anvil.email.send(
    #       to="maciek.anywhere@gmail.com",
    #       subject="Issue/bug Notebook anvil",
    #       text=self.quill.getText()
    #     )