from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# responses gop here

def index(request):
    return render(request,'soles/index.html')

def validate(request):
    # Email Validation
    hasError = False
    if len(request.POST['first_name']) < 3:
        messages.error(request,'Yo cuh, you need more than 2 characters for first name,letters only')
        hasError = True
    if len(request.POST['last_name']) < 3:
        messages.error(request,'Yo cuh, you need more than 2 characters for last name,letters only')
        hasError = True
    if len(request.POST['user_name']) < 4:
        messages.error(request,'Yo cuh, you need more than 3 characters for user name,letters only')
        hasError = True
    if len(request.POST['email']) < 1:
        messages.error(request,'Yo cuh, you need more than 1 character for an email')
        hasError = True
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Yo cuh, email is not valid!!')
        hasError = True
    if len(User.objects.filter(email = request.POST['email'])) > 0:
        messages.error(request, 'Email already in db')
        hasError = True
    if len(request.POST['password']) < 8:
        messages.error(request,'Yo cuh, password must be at least 8 characters!!')
        hasError = True
    if not request.POST['password'] == request.POST['confirmpw']:
        messages.error(request,'Yo cuh, passwords dont match!!')
        hasError = True

    if hasError:
        return redirect('/')
    else:
        # password hash
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')
        usr=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],user_name=request.POST['user_name'],email=request.POST['email'],password=correct_hashed_pw)
        request.session['userID']=usr.id
        messages.success(request,'Yo, you succesfully created an account')
        print(usr)
    return redirect('/')

# when user signs in
def log(request):
     # Query db
    user = User.objects.filter(email=request.POST['emaillog'])
    print(user)
    # if no match
    if len(user) == 0:
        print("user not in DB")
        messages.error(request,'Invalid Login')
        return redirect('/')
    # if a match
    else:
        # hash it
        matched = bcrypt.checkpw(request.POST['pwlog'].encode(),user[0].password.encode())
        print("matched = " , matched)
        # if they do match
        if matched:
            print("matched!")
            # store user id in session
            request.session['user_id'] = user[0].id
            return redirect('/dashboard')
            # return redirect('/')
            # else error message 
        else:
            print('not matched')
            messages.error(request,'No match')
            return redirect('/')
# loads up the dash/home page
def dash(request):
    # checks if signed in
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    
    context ={
        'user': User.objects.get(id=request.session['user_id']),
        'reviews': Post.objects.all(),
    }
    return render(request,'soles/dashboard.html', context)

def review(request):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    return render(request,'soles/addreview.html')

# creates the review
def create_review(request):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    # validations
    if len(request.POST['brand']) < 2:
        messages.error(request,'Yo cuh, Brand name needs to be at least 2 characters')
    if len(request.POST['model'])  < 2:
        messages.error(request,'Yo cuh, Model name needs to be at least 2 characters')
    if len(request.POST['review']) < 50:
        messages.error(request,'Yo cuh, your review must be at least 50 characters')
    if len(request.FILES) == 0:
        messages.error(request,'Yo cuh, you must select an image to upload')

    else:
        user = User.objects.get(id=request.session['user_id'])
        print(user)
        post = Post.objects.create(shoe_brand=request.POST['brand'], shoe_model=request.POST['model'],post_pic= request.FILES['image'],recommend=request.POST['rec'], purchase_link=request.POST['link'],life_span=request.POST['life'],content=request.POST['review'],user_post=user)
        print(post)
        messages.success(request,'Succesfully created a review homie!')
        post.save()
        return redirect('/review')

    return redirect('/review')
# about page
def about(request):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    return render(request,'soles/about.html')

# renders edit form
def edit(request,id):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    context={
        'rev': Post.objects.get(id=id)
    }
    return render(request,'soles/editrev.html',context)

# updates the post
def update_post(request,id):
    # validations
    if len(request.POST['brand']) < 2:
        messages.error(request,'Yo cuh, Brand name needs to be at least 2 characters')
    if len(request.POST['model'])  < 2:
        messages.error(request,'Yo cuh, Model name needs to be at least 2 characters')
    if len(request.POST['review']) < 50:
        messages.error(request,'Yo cuh, your review must be at least 50 characters')

    else:
        post = Post.objects.get(id=id)
        print(post)
        post.shoe_brand = request.POST['brand']
        post.shoe_model = request.POST['model']
        # this if Gets rid of multivaluedictkey error
        if len(request.FILES) == 0:
            print('sick')
        else:
            post.post_pic = request.FILES['imagenew']
        post.purchase_link = request.POST['link']
        post.recommend = request.POST['rec']
        post.life_span = request.POST['life']
        post.content = request.POST['review']
        post.save()
        messages.success(request,'Succesfully edited your review homie!')
        return redirect('/edit/{}'.format(post.id))

    return redirect('/review')

# displays post
def display_post(request,id):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    context = {
        'p': Post.objects.get(id=id)
    }
    return render(request, 'soles/viewpost.html',context)

# delete post
def delete_post(request,id):
    Post.objects.get(id=id).delete()
    return redirect('/dashboard')



# logout
def logout(request):
    request.session.clear()
    return redirect('/')
# makes query for profile signed in then goes to profile
def go_profile(request):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    # query to find current user
    context ={
        'u': User.objects.get(id=request.session['user_id']),
        'reviews': Post.objects.filter(user_post__id = request.session['user_id'])
    }
    return render(request, 'soles/profile.html',context)

# loads edit page and makes a query 
def edit_prof(request):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    user=User.objects.get(id=request.session['user_id'])
    context={
        'user': user
    }
    return render(request, 'soles/editprof.html', context)

# update user info
def update_user(request, id):
    if len(request.POST['f_name']) < 2:
        messages.error(request,'Yo cuh, yo first name needs to be at least 2 characters')
    if len(request.POST['l_name']) < 2:
        messages.error(request,'Yo cuh, yo last name needs to be at least 2 characters')
    if not EMAIL_REGEX.match(request.POST['new_email']):
        messages.error(request,'Yo cuh, email is not valid!!')
    if len(request.POST['new_username']) < 4:
        messages.error(request,'Yo cuh, yo username needs to be at least 4 characters')
    if len(request.POST['favskater']) < 4:
        messages.error(request,'Yo cuh, yo fav skater needs to be at least 4 characters')
    if len(request.POST['favshoe']) < 4:
        messages.error(request,'Yo cuh, yo fav skater needs to be at least 4 characters')
    if len(request.POST['newpw']) < 8:
        messages.error(request,'Yo cuh, password must be at least 8 characters!!')
    
    else:
        user = User.objects.get(id=id)
        print('found user', user)
        # new password hash
        hashed_pw = bcrypt.hashpw(request.POST['newpw'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')
        user.first_name = request.POST['f_name']
        user.last_name = request.POST['l_name']
        user.email = request.POST['new_email']
        user.user_name = request.POST['new_username']
        user.fav_skater = request.POST['favskater']
        user.fav_shoe = request.POST['favshoe']
        user.password = correct_hashed_pw
        user.save()
        messages.success(request,'Succesfully edited your profile homie!')
        return redirect('/profile/edit')

    return redirect('/dash')

# def search(request):
#     posts = Post.objects.filter(shoe_brand__icontains=request.POST['shoesearch']) or Post.objects.filter(shoe_model__icontains=request.POST['shoesearch'])
#     print(posts)
#     return render(request, 'soles/option.html',{'shoeposts': posts})
def search_shoes(request):
    print('got to the server')
    posts = Post.objects.filter(shoe_brand__startswith=request.POST['shoesearch']) or Post.objects.filter(shoe_model__startswith=request.POST['shoesearch'])
    print(posts)
    context = {'shoeposts': posts}
    return render(request, 'soles/option.html',context)

# for a user profile 
def get_pofile(request, id):
    if not 'user_id' in request.session:
        messages.error(request,'You must sign in first')
        return redirect('/')
    context ={
        'u': User.objects.get(id=id),
        'reviews': Post.objects.filter(user_post__id = id)
    }
    return render(request, 'soles/user_prof.html', context)