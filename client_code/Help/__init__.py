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
    