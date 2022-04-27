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

  # author = get_author_by_name(authorname)
  user = get_user_by_name(username)
 
  
  if request.POST: 
    # POST request received
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    if(data['type'] == 'claim'):
    #need to update listing as claimed
      claimed_post = Posting.objects.filter(item_name = data['claimed_post'])
      print("DEBUG: views post request, the claimed post is ", claimed_post)

      for object in claimed_post:
        object.claimed = True
        object.save()
      print("DEBUG view post req, claimed = ", claimed_post[0].claimed)
      #need to update user's claimed list 
      print(user.claimed)
      current_claimed = user.claimed
      if current_claimed == None:
        current_claimed = []
      current_claimed.append(str(claimed_post[0].item_name))
      user.claimed = current_claimed
      user.save()
    if(data['type'] == 'save'):
      bool_saved = data['bool_saved']
      saved_post = Posting.objects.filter(item_name = data['saved_post'])
      #need to update user's claimed list 
        # add to saved
      print(user.saved)
      current_saved = user.saved
      if(bool_saved == 'True'):
        if current_saved == None:
          current_saved = []
        current_saved.append(str(saved_post[0].item_name))
      if(bool_saved == 'False'):
        if current_saved == None:
          current_saved = []
        else: 
          current_saved.remove(str(saved_post[0].item_name))
      user.saved = current_saved
      user.save()
    return HttpResponse(True)

  else:  #GET Request
    all_postings = []
    friend_postings = []
    
    postings = Posting.objects.filter(active = True,claimed = False)
    for post in postings:
      
      post_info = [post.item_name, post.qty, post.qty_units, post.description, post.listing_user.username, json.dumps(post.unopened), json.dumps(post.og_packaging), json.dumps(post.store_bought), json.dumps(post.homemade),json.dumps(post.listing_user.verified)]
      if user.friends == None:
        user.friends = []
      if post.listing_user.username in user.friends:
        print("this works")
        friend_postings.append(post_info)
      all_postings.append(post_info)
    print(all_postings)
    if User.objects.filter(username = username).exists():
      data = {
        "user": user,
        "all_postings": all_postings,
        "friend_postings": friend_postings
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": [],
        "all_postings": all_postings,
        "friend_postings": friend_postings
      }
    
    return render(request, 'coloring/index.html', data)
    

def chatindex(request, username=""):
  # print("The authorname is:", authorname)
  # author = get_author_by_name(authorname)
  
  if request.POST: 
    # POST request received
    
    # demonstrating printing out the POST request & data
    print("Received POST request with data:")
    data = json.loads(request.body.decode('UTF-8'))
    print(data)
    return HttpResponse(True)
  
  data = {
      "user": username,
      "friends": [],
    }
  return render(request, 'coloring/chat-index.html', data)

    # creating a new listing
    
    
    
@csrf_exempt
def newlisting(request, username =""):
  # print("The authorname is:", authorname)
  # author = get_author_by_name(authorname)
  
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
      if(friends_list.count(str(data['friends'])) > 0):
        return HttpResponse() 
      else:
        friends_list.append(str(data['friends']))
        print("DEGBUG views.py: friends list updated", friends_list)
        user.friends=friends_list
        user.save(update_fields=['friends'])
        return HttpResponse(True) 

      
      #user.friends = user.friends.append(data['friends'])
      #user.save() 
      # print("friends list udpated: ", user.friends)
      # print("DEBUG views.py, friends: the updated friend list is ", user.friends)
      
    else:
      print("DEBUG views.py, friends: the user does not exist")
      return HttpResponse(False) 
    
    #return json response
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
      if user.total == None:
        total_points = 0
      else:
        total_points = user.total
        
      if user.rating == None:
        rating = 0
      else:
        rating = user.rating
      data = {
        "user": user,
        "friends": user.friends,
        "points": total_points,
        "rating": rating
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "friends": [],
        "points": total_points,
        "rating": rating
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
       post_info = [post.item_name, post.qty, post.qty_units, post.description, post.listing_user.username, json.dumps(post.unopened), json.dumps(post.og_packaging), json.dumps(post.store_bought), json.dumps(post.homemade),json.dumps(post.listing_user.verified)]
      #post_info = [post.item_name, post.description]
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

    if(data['type']=="pickedup"):
      print("in views registered as pickup")
      pickedup_post =Posting.objects.filter(item_name=data["pickup_post"])
      #need to update post.active = False
      # i dont think this needs a for loop if we treat each item name as unique
      for object in pickedup_post:
        object.active = False
        object.save()

      #remove from user's claimed list and add to their impact score
      user.claimed.remove(pickedup_post[0].item_name)
      print("updated user claim list,", user.claimed)
      if(user.total == None):
        user.total = 0
      user.total = user.total + 1 
      user.save()
      print("updated user claim list,", user.claimed)
      listing_user = pickedup_post[0].listing_user
      
      if(listing_user.total == None):
        listing_user.total = 0
      listing_user.total = listing_user.total + 1 
      listing_user.save()
    else: #type is rated
      # get listing user
      pickedup_post =Posting.objects.filter(item_name=data["rated_post"])
      print("here")
      print(pickedup_post)
      listing_user = pickedup_post[0].listing_user
      old_num = listing_user.rating_numer
      old_den = listing_user.rating_denom
      this_snum, this_sdenom = (data["score"]).split('/')
      this_num = int(this_snum)
      new_rating = round(((old_num+this_num)/(old_den + 5))*5,2)
      print("user being rated is ", listing_user.username)
      print("this is new rating!!!!", new_rating)
      listing_user.rating = new_rating
      listing_user.rating_numer = this_num + old_num
      listing_user.rating_denom = old_den + 5
      if listing_user.total_ratings == None:
        listing_user.total_ratings = 1
      else:
        listing_user.total_ratings += 1
      listing_user.save()
      # add to their rating in data base
      print("in views registered as rated")
    
    return HttpResponse(True)
  else: #GET request
    if User.objects.filter(username = username).exists():
      user_claimed = user.claimed
      if user.claimed == None:
        user_claimed = []
      my_claimed = []
      
      #claimed_postings = Posting.objects.filter(claimed=True)
    for posting in user_claimed:
      post = Posting.objects.filter(item_name = posting)
      print("post is", post)
      new_post = post[0]
      print("new post is", new_post)
      post_info = [new_post.item_name, new_post.qty, new_post.qty_units, new_post.description, new_post.listing_user.username, json.dumps(new_post.unopened), json.dumps(new_post.og_packaging), json.dumps(new_post.store_bought), json.dumps(new_post.homemade),json.dumps(new_post.listing_user.verified)]
      my_claimed.append(post_info)
      
      data = {
        "user": user,
        "my_claimed": my_claimed
      }
    else:
      print("DEBUG: user doesnt yet exist")
      data = {
        "user": user,
        "my_claimed": my_claimed
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

def startchat(request, username="", listinguser=""):
  if request.GET:
    # Start a new chat between us and the new guy
    data = json.loads(request.body.decode('UTF-8'))
    chat_storage = None
    if ChatStorage.objects.filter(user_one = username, user_two = listinguser).exists():
      chat_storage = ChatStorage.objects.get(user_one = username, user_two = listinguser)
    elif ChatStorage.objects.filter(user_one = listinguser, user_two = username).exists():
      chat_storage = ChatStorage.objects.get(user_one = listinguser, user_two = username)
    else:
      chat_storage = ChatStorage(user_one = username, user_two = listinguser)
      chat_storage.save()

  data = {
        "user": username,
        "listinguser": listinguser,
        "friends": [],
      }
  print(listinguser)
  return render(request, 'coloring/chat-index.html', data)
  #return chatindex(request, username)