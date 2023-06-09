import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
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
def get_note_by_id(note):
  if current_user is not None:
    return app_tables.notes.get_by_id(note.get_id())
    
@anvil.server.callable
def add_user_to_notebook_users(notebook, user, read_only):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] += [user]
  notebook.update(users=notebook['users'])
  if read_only:
    app_tables.permission.add_row(notebook=notebook ,user=user ,can_edit=True)
  else:
    app_tables.permission.add_row(notebook=notebook ,user=user ,can_edit=False)
  
@anvil.server.callable
def remove_user_from_the_notebook_users(notebook):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] = [u for u in notebook['users'] if u != current_user]
  notebook.update(users=notebook['users'])
  permision = app_tables.permission.get(notebook=notebook, user=current_user)
  permision.delete()

@anvil.server.callable
def check_user_permission(note):
  user_permission = app_tables.permission.get(notebook=note['notebook'], user=current_user)
  return user_permission['can_edit']

@anvil.server.callable
def stop_sharing_notebook_with_user(notebook, user):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  notebook['users'] = [u for u in notebook['users'] if u != user]
  notebook.update(users=notebook['users'])
  permision = app_tables.permission.get(notebook=notebook, user=user)
  permision.delete()

@anvil.server.callable
def get_all_notebooks():
  if current_user is not None:
    all_notebooks = app_tables.notebooks.search(tables.order_by("updated", ascending=False), owner=current_user)
    if len(all_notebooks) == 0:
        new_notebook_name = 'Notebook: ' + (current_user['name'] if current_user['name'] else current_user['email'])
        save_new_notebook(new_notebook_name)
        all_notebooks = app_tables.notebooks.search(tables.order_by("updated", ascending=False), owner=current_user)
    return all_notebooks
  raise Exception("User is not logged in.")
  
@anvil.server.callable
def get_all_notebook_names():
  if current_user is not None:
    return [(nbook['name'], nbook) for nbook in app_tables.notebooks.search(tables.order_by("updated", ascending=False), users=[current_user])]
  raise Exception("User is not logged in.")

@anvil.server.callable
def get_issue_notebook():
  return app_tables.notebooks.get(name='Issues and Bugs', owner=app_tables.users.get(name='Maciek'))

@anvil.server.callable
def send_email(issue):
    anvil.email.send(
    to="maciek.anywhere@gmail.com",
    subject="Issue/bug Notebook anvil",
    text=issue
  )
  
@anvil.server.callable
def get_the_last_note(notebook): 
  if current_user is not None:
    try:
      return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=notebook)[0]
    except:
      return None
  raise Exception("User is not logged in.")

@anvil.server.callable
def get_one_before_the_last_note_from_the_notebook(note):
  try:
    return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=note['notebook'])[1]
  except:
    return None
  
@anvil.server.callable
def get_all_notes_in_the_notebook(notebook):
  notebook = app_tables.notebooks.get_by_id(notebook.get_id())
  return app_tables.notes.search(tables.order_by("updated", ascending=False), notebook=notebook)
  
def create_new_note(notebook):
  new_note = {}
  new_note['title'] = 'New Note'
  new_note['content_json'] = json.dumps([{"insert":"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"}])
  new_note['content'] = 'New Note'
  new_note['notebook'] = notebook
  save_new_note(new_note)

def create_welcoming_note(notebook):
  new_note = {}
  new_note['title'] = 'Your First Note'
  new_note['content_json'] = json.dumps([{"insert":"\n\n"},{"attributes":{"color":"#6b24b2"},"insert":"Welcome to Notebookkk!"},{"attributes":{"align":"center","header":1},"insert":"\n"},{"attributes":{"align":"center"},"insert":"\n"},{"insert":"To create a new notebook, click on the \"Add\" button on the \"Notebooks\" sidebar on the left-hand side of the homepage. Once you have created a notebook, you can add notes to it by clicking on the \"New Note\" button on the top right side of the homepage. When ready, click on \"Save\"."},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"To share a notebook, click the three dots next to the notebook and then the \"Share\" button. Then, enter the email addresses of the users you want to add and select the permission you want to grant them, such as editing access or read-only."},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"When an added user logs in, they will see the shared notebook on their homepage."},{"attributes":{"list":"ordered"},"insert":"\n"},{"insert":"\n "},{"attributes":{"align":"center","header":2},"insert":"\n"},{"insert":"\n\n\n\n\n\n"}])
  new_note['content'] = 'Welcoming Note'
  new_note['notebook'] = notebook
  save_new_note(new_note)

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
def save_new_notebook(notebook_name):
  notebook = app_tables.notebooks.add_row(
    name=notebook_name,
    updated=datetime.now(),
    owner=current_user,
    users=[current_user]
  )
  app_tables.permission.add_row(notebook=notebook ,user=current_user ,can_edit=True)
  create_new_note(notebook)
  return notebook
  
@anvil.server.callable
def create_notebook_with_welcoming_note():
  notebook = app_tables.notebooks.add_row(name=f'Welcome {current_user["name"]}!', updated=datetime.now() ,owner=current_user, users=[current_user])
  create_welcoming_note(notebook)
  app_tables.permission.add_row(notebook=notebook ,user=current_user ,can_edit=True)
        
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
    permissions = app_tables.permission.search(notebook=notebook)
    for permission in permissions:
      permission.delete()
    notebook.delete()
  else:
    raise Exception("Notebook does not exist or does not belong to this user")

@anvil.server.callable
def search_notes(query_text):
  all_notebooks = get_all_notebooks()
  found_notes = []
  if query_text:
    for notebook in all_notebooks:
      found_notes += app_tables.notes.search(
        q.any_of(
          title=q.ilike(f"%{query_text}%"),
          content=q.ilike(f"%{query_text}%"),
        ), 
        notebook=notebook)
    found_notes.sort(key=lambda note: note["updated"], reverse=True )
  return found_notes