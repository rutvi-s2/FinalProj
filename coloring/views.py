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

  author = get_author_by_name(authorname)
  user = get_user_by_name(username)
 
  
  if request.POST: 
    # POST request received
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)

    #need to update listing as claimed
    claimed_post = Posting.objects.filter(item_name = data['claimed_post'])
    print("DEBUG: views post request, the claimed post is ", claimed_post)

    for object in claimed_post:
      object.claimed = True
      object.save()
    #claimed_post.claimed = True
    #claimed_post.save()
    
    print("DEBUG view post req, claimed = ", claimed_post[0].claimed)
    #need to update user's claimed list 
    print(user.claimed)
    current_claimed = user.claimed
    if current_claimed == None:
      current_claimed = []
    current_claimed.append(str(claimed_post[0].item_name))
    user.claimed = current_claimed
    user.save()
    
    return HttpResponse(True)

  else:  #GET Request
    all_postings = []
    postings = Posting.objects.filter(active = True,claimed = False)
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

    if user.friends == None:
      #this shouldn;t be happening, debug later
      print("in a post req")
      user.friends = []
      user.save(update_fields=['friends'])
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
      if user.friends == None:
        user.friends = []
        
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
@csrf_exempt
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



@csrf_exempt  
def mylistings(request, username =""):
  user = get_user_by_name(username)
 
  
  if request.POST: 
    # POST request received
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)

  else:  #GET
    my_curr = []
    my_pickup = []
    my_archive = []
    my_postings = Posting.objects.filter(listing_user=user)
    for post in my_postings:
      # post_info = [post.item_name, post.qty, post.qty_units, post.best_by, post.description, post.unopened, post.og_packaging, post.store_bought, post.homemade]
      post_info = [post.item_name, post.description]
      if(post.active == True):
        # add to my_curr or my_pickup
        if(post.claimed == False):
          my_curr.append(post_info)
        else:
          my_pickup.append(post_info)
      else: 
        # add to archive
        my_archive.append(post_info)
    print("my acrhive!!!!!!!!!!!!", my_archive)
    print("my curr!!!!!!!!!!!!!!", my_curr)
    print("my pickup!!!!!!!!!!!!!!", my_pickup)
    if User.objects.filter(username = username).exists():
      data = {
        "user": user,
        "my_archive": my_archive,
        "my_curr": my_curr,
        "my_pickup": my_pickup
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "my_archive": my_archive,
        "my_curr": my_curr,
        "my_pickup": my_pickup
      }
    
    return render(request, 'coloring/mylistings.html', data)
    
@csrf_exempt
def claimed(request, username =""):
  user = get_user_by_name(username)

  if request.POST: 
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)

    pickedup_post = Posting.objects.filter(item_name=data["pickup_post"])
    #need to update post.active = False
    for object in pickedup_post:
      object.active = False
      object.save()
    
    #remove from user's claimed list
    user.claimed.remove(pickedup_post[0].item_name)
    user.save()
    #pop up with rating
    
    return HttpResponse(True)
  else: #GET request
    if User.objects.filter(username = username).exists():
      user_claimed = user.claimed
      my_claimed = []
      
      #claimed_postings = Posting.objects.filter(claimed=True)
      for post in user_claimed:
        print("CLAIMED POSTING", post)
        post_details = Posting.objects.filter(item_name=post)
        post_info = [post_details[0].item_name, post_details[0].description]
        my_claimed.append(post_info)
        print("DEBUG my_claimed", my_claimed)
      
      data = {
        "user": user,
        "my_claimed": my_claimed
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "my_claimed": []
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