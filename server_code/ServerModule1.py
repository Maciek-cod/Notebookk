import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

import json

current_user = anvil.users.get_user()

@anvil.server.callable
def save_user_name(name):
  user = app_tables.users.get_by_id(anvil.users.get_user().get_id())
  user.update(name=name)

@anvil.server.callable
def find_user(email):
  user = app_tables.users.get(email=email)
  return user if user else False

@anvil.server.callable
def add_user_to_notebook_users(notebook, user, read_only):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] += [user]
  if read_only:
    if notebook['users_read_only'] is None:
      notebook['users_read_only'] = []
    notebook['users_read_only'] += [user]
  notebook.update(users=notebook['users'])

@anvil.server.callable
def remove_user_from_the_notebook_users(notebook):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] = [u for u in notebook['users'] if u != current_user]
  notebook.update(users=notebook['users'])

@anvil.server.callable
def stop_sharing_notebook_with_user(notebook, user):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] = [u for u in notebook['users'] if u != user]
  if notebook['users_read_only'] is not None:
    notebook['users_read_only'] = [u for u in notebook['users_read_only'] if u != user]
  notebook.update(users=notebook['users'])

@anvil.server.callable
def get_all_notebooks():
  if current_user is not None:
    return app_tables.notebooks.search(tables.order_by("updated", ascending=False), users=[current_user])
  raise Exception("User is not logged in.")
  
@anvil.server.callable
def get_all_notebook_names():
  if current_user is not None:
    nbook = app_tables.notebooks.search(tables.order_by("updated", ascending=False), users=[current_user])
    lis = []
    for nbk in nbook:
      if nbk['users_read_only'] is None: lis.append(nbk)
      else:
        donot = False
        for user in nbk['users_read_only']:
          if user == current_user: donot = True
        if not donot: lis.append(nbk)
    return [(nbook['name'], nbook) for nbook in lis]
  raise Exception("User is not logged in.")
  
@anvil.server.callable
def get_the_last_note(notebook): 
  if current_user is not None:
    return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=notebook)[0]
  raise Exception("User is not logged in.")

@anvil.server.callable
def get_one_before_the_last_note_from_the_notebook(note):
  try:
    return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=note['notebook'])[1]
  except:
    return None
    
@anvil.server.callable
def get_note_by_id(note):
  if current_user is not None:
    return app_tables.notes.get_by_id(note.get_id())
  
@anvil.server.callable
def get_all_notes_in_the_notebook(notebook):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=notebook)
  
def create_new_note(notebook):
  new_note = {}
  new_note['title'] = 'New Note 📝'
  new_note['content_json'] = json.dumps([{"insert":"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"}])
  new_note['content'] = 'New Note'
  new_note['notebook'] = notebook
  anvil.server.call('save_new_note', new_note)

def create_welcoming_note(notebook):
  new_note = {}
  new_note['title'] = 'Your First Note 📝'
  new_note['content_json'] = json.dumps([{"insert":"\n\n"},{"attributes":{"color":"#6b24b2"},"insert":"Welcome to Notebookkk!"},{"attributes":{"align":"center","header":1},"insert":"\n"},{"attributes":{"align":"center"},"insert":"\n\n"},{"insert":"Open the sidebar, and click the edit Notebooks button to create a new notebook. "},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"Click the New Note button on the top right side of the page and create notes."},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"Share your notebooks with others by clicking the share button next to the notebook at Edit Notebooks."},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"Enjoy using the Notebookkk! "},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"\n "},{"attributes":{"align":"center","header":2},"insert":"\n"},{"insert":"\n\n\n\n\n\n"}])
  new_note['content'] = 'Welcoming Note'
  new_note['notebook'] = notebook
  anvil.server.call('save_new_note', new_note)

@anvil.server.callable
def save_new_note(note_dict):
  app_tables.notes.add_row(
          updated=datetime.now(), 
          edited_by=current_user, 
          **note_dict
  )
  # update notebook 'updated time'
  notebook = app_tables.notebooks.get_by_id(note_dict['notebook'].get_id())
  notebook.update(updated=datetime.now())
  
@anvil.server.callable
def seve_new_notebook(notebook_name):
  notebook = app_tables.notebooks.add_row(name=notebook_name, updated=datetime.now(), owner=current_user, users=[current_user])
  create_new_note(notebook)
  return notebook

@anvil.server.callable
def create_notebook_with_welcoming_note():
  notebook = app_tables.notebooks.add_row(name=f'Welcome {current_user["name"]}!', updated=datetime.now() ,owner=current_user, users=[current_user])
  create_welcoming_note(notebook)
        
def verify_user_permission_notebook(notebook):
  if current_user is not None:
    for user in notebook['users']: 
      if user == current_user and app_tables.notebooks.has_row(notebook): return True
        
@anvil.server.callable
def update_note(note, note_dict):  
  if verify_user_permission_notebook(note['notebook']):
    # update note
    note_dict['updated'] = datetime.now()
    note_dict['edited_by'] = current_user
    note.update(**note_dict)
    # update notebook 'updated' time field
    notebook = app_tables.notebooks.get_by_id(note['notebook'].get_id())
    notebook.update(updated=datetime.now())
  else:
    raise Exception("Note does not exist or does not belong to this user")

@anvil.server.callable
def update_notebook(notebook, notebook_dict):
  if verify_user_permission_notebook(notebook):
    notebook.update(**notebook_dict)
  else:
    raise Exception("Notebook does not exist or does not belong to this user")
    
@anvil.server.callable
def delete_note(note):
  if verify_user_permission_notebook(note['notebook']):
    # Change 'updated' in notebook table to the last note
    notebook = app_tables.notebooks.get_by_id(note['notebook'].get_id())
    last_note = app_tables.notes.search(tables.order_by("updated", ascending=False))[:2]
    last_note_l = list(last_note)
    if note == last_note_l[0]: notebook.update(updated=last_note_l[1]['updated'])
    note.delete()
  else:
    raise Exception("Note does not exist or does not belong to this user")

def delete_notes_assigned_to_the_deleting_notebook(notebook):
  notes = app_tables.notes.search(notebook=notebook)
  for note in notes: note.delete()

@anvil.server.callable
def delete_notebook(notebook):
  if verify_user_permission_notebook(notebook):
    delete_notes_assigned_to_the_deleting_notebook(notebook)
    notebook.delete()
  else:
    raise Exception("Notebook does not exist or does not belong to this user")

@anvil.server.callable
def search_notes(query):
  all_notebooks = get_all_notebooks()
  all_notes = []
  for notebook in all_notebooks:
    all_notes += get_all_notes_in_the_notebook(notebook)

  result = all_notes
  if query:
    result = [
      x for x in result
      if query.casefold() in x['title'].casefold()
      or query.casefold() in x['content'].casefold()]
  return result