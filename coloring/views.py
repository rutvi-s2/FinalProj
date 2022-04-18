from django.shortcuts import render
from coloring.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

def get_author_by_name(authorname): 
  author = None
  
  # check if an Author with name 'authorname' already exists
  if Author.objects.filter(name = authorname).exists():
    # if so, fetch that object from the database
    author = Author.objects.get(name=authorname)
    
  else: 
    # otherwise, create a new Author with the name authorname
    author = Author(name = authorname)
    # save the created object
    author.save()

  return author




def get_user_by_name(name): 
  user = None
  
  # check if an User with name 'username' already exists
  if User.objects.filter(username = name).exists():
  
    # if so, fetch that object from the database
    user = User.objects.get(username=name)
    print("DEBUG: get_user_by_name: username exists: ", user.username)
    
  else: 
    # otherwise, create a new User with the name name
    user = User(username = name)
    # save the created object
    user.save()

  return user
@csrf_exempt
def index(request, authorname="DefaultAuthor", username =""):

  print("The authorname is:", authorname)
  author = get_author_by_name(authorname)
  user = get_user_by_name(username)
 # print("DEBUG: view.py- index, The username is ", user.username)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)


    
    return HttpResponse(True)

  else: 
    # GET request received

    # if a drawing by the author already exists,
    # send the drawing conent and title with the data below
    
    data = {
      "author": author
    }
    
    return render(request, 'coloring/index.html', data)
    
@csrf_exempt
def newlisting(request, username =""):
  # print("The authorname is:", authorname)
  user = get_user_by_name(username)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)

    # creating a new listing
    item = data.get('item')
    quantity = data.get('quantity')
    units = data.get('units')
    exp_date = data.get('exp_date')
    dscrpt = data.get('description')
    uno = data.get('unopened')
    sb = data.get('storebought')
    hm = data.get('homemade')
    op = data.get('og_packaging')
    
    posting = Posting(item_name = item, qty = quantity, qty_units = units, best_by = exp_date, description = dscrpt, unopened = uno, og_packaging = op, store_bought = sb, homemade = hm)
    posting.save()
    # itemName = data.get('item')
    
    
    

    # find out if a Drawing with the Author and Title already exists?
    # if it doesn't exist, you may create a new Drawing object
    # if it does exist, you may update an existing Drawing object
    
    # make sure to save your object after creating or updating 
    # for more information, see get_author_by_name() and reference below
    # https://docs.djangoproject.com/en/4.0/ref/models/instances/#saving-objects
    
    return HttpResponse(True)

  else: 
    # GET request received

    # if a drawing by the author already exists,
    # send the drawing conent and title with the data below
    
    data = {
      "item": "shouldnt get here"
    }
  return render(request, 'coloring/newlisting.html')

@csrf_exempt
def friends(request, username =""):
  user = get_user_by_name(username)
  print("DEBUG: friends-profile, The username is ", user.username)
  if request.POST: 
    #get the data from the post request
    data = json.loads(request.body.decode('UTF-8'))
    print("Data recieved", data)

  
    if user.friends == None:
      user.friends = {}

    #check if user exists
    if User.objects.filter(username = data['friends']).exists():
  
      list_len = len(user.friends)
      user.friends[list_len] = data['friends']
      user.save() 
      print("DEBUG views.py, friends: the updated friend list is ", user.friends)
    else:
      print("DEBUG views.py, friends: the user does not exist")
    
    return HttpResponse(True)
  else:
    data = {
      "user": user
    }
    return render(request, 'coloring/friends.html', data)

def profile(request, username =""):
  user = get_user_by_name(username)
  print("DEBUG: views-profile, The username is ", user.username)

  if request.POST: 
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)
  else:
    data = {
      "user": user
    }
    
    
  
    return render(request, 'coloring/profile.html', data)
  
  