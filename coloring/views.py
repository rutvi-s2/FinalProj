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
 
  
  if request.POST: 
    # POST request received
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)

  else:  
    all_postings = []
    postings = Posting.objects.all()
    for post in postings:
      post_info = [post.item_name, post.description]
      all_postings.append(post_info)
      
    if User.objects.filter(username = username).exists():
      data = {
        "user": user,
        "all_postings": all_postings
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": [],
        "all_postings": all_postings
      }
    
    return render(request, 'coloring/index.html', data)
    
@csrf_exempt
def newlisting(request, username =""):
  
  user = get_user_by_name(username)
  print(user.username)
  if request.POST: 
    # POST request received
 
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
    
    posting = Posting(item_name = item, qty = quantity, qty_units = units, best_by = exp_date, description = dscrpt, unopened = uno, og_packaging = op, store_bought = sb, homemade = hm, listing_user = user)
    posting.save()
    # itemName = data.get('item')
      
    return HttpResponse(True)

  else: 
    # GET request received
    if User.objects.filter(username = username).exists():
      print("DEBUG: def newlisting, inside get request user does exist")
      print("the user friends are ", user.friends)
      
      data = {
        "user": user,
        "friends": user.friends
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": []  
      }
  return render(request, 'coloring/newlisting.html', data)

@csrf_exempt
def friends(request, username =""):
  user = get_user_by_name(username)
  print("DEBUG views.py: friends, The username is ", user.username)
  print("DEBUG views.py: friends, friends are ", user.friends)
  if request.POST: 
    data = json.loads(request.body.decode('UTF-8'))
    print("Data recieved", data)

    if user.friends == None: #this shouldn;t be happening, debug later
      user.friends = []
      print(user.friends)

    #check if user exists (can't add user that doesn't exist)
    if User.objects.filter(username = data['friends']).exists():
      friends_list = user.friends
      friends_list.append(str(data['friends']))
      print("DEGBUG views.py: friends list updated", friends_list)
      user.friends=friends_list
      user.save(update_fields=['friends'])

      
      #user.friends = user.friends.append(data['friends'])
      #user.save() 
      print("friends list udpated: ", user.friends)
      print("DEBUG views.py, friends: the updated friend list is ", user.friends)
    else:
      print("DEBUG views.py, friends: the user does not exist")
    
    return HttpResponse(True)
  else: #GET request
    if User.objects.filter(username = username).exists():
      print("DEBUG: def freinds, inside get request user does exist")
      print("the user friends are ", user.friends)
      
      data = {
        "user": user,
        "friends": user.friends
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": []
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
    if User.objects.filter(username = username).exists():
      print("DEBUG: def freinds, inside get request user does exist")
      print("the user friends are ", user.friends)
      
      data = {
        "user": user,
        "friends": user.friends
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": []
      }
  
    return render(request, 'coloring/profile.html', data)



  
def mylistings(request, username =""):
  user = get_user_by_name(username)
 
  
  if request.POST: 
    # POST request received
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)

  else:  
    # all_postings = []
    # postings = Posting.objects.all()
    # for post in postings:
    #   post_info = [post.item_name, post.description]
    #   all_postings.append(post_info)
    my_active = []
    my_archive = []
    my_postings = Posting.objects.filter(listing_user=user)
    for post in my_postings:
      post_info = [post.item_name, post.description]
      if(post.active == True):
        # add to active
        my_active.append(post_info)
      else: 
        # add to archive
        my_archive.append(post_info)
    print("my acrhive!!!!!!!!!!!!", my_archive)
    print("my active!!!!!!!!!!!!!!", my_active)
    if User.objects.filter(username = username).exists():
      data = {
        "user": user,
        "archive": my_archive,
        "actives": my_active
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": [],
        "all_postings": all_postings
      }
    
    return render(request, 'coloring/mylistings.html', data)

def claimed(request, username =""):
  user = get_user_by_name(username)

  if request.POST: 
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)
  else:
    if User.objects.filter(username = username).exists():
      
      data = {
        "user": user
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user
      }
  
    return render(request, 'coloring/claimed.html', data)
def saved(request, username =""):
  user = get_user_by_name(username)

  if request.POST: 
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)
  else:
    if User.objects.filter(username = username).exists():
      
      data = {
        "user": user
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user
      }
  
    return render(request, 'coloring/saved.html', data)