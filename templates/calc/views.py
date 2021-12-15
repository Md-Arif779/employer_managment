
from django.http import request
from django.http.request import validate_host
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import TemplateView
from .models import Post, Comment
from .forms import PostFrom
from django.views.generic import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .templatetags import tag
# Create your views here.


def search(request):
    query=request.POST.get('search','')
    if query:
        queryset=(Q(Name__icontains=query)) | (Q(Email__icontains=query)) | (Q(Phone__icontains=query)) | (Q(Category__icontains=query))
        results=Post.objects.filter(queryset).distinct()
    else:
        results=[]
    context ={
        'results':results
    }        
    return render(request, 'search.html',context)

def posts(request):
    post=Post.objects.all()
    return render(request,'driver.html',{'post':post})

     
from django.views.generic import ListView
class PostListView(ListView):
    template_name='postlist.html'
    model=Post
    context_object_name='posts'
    

class PostCreateView(CreateView):
    model=Post
    form_class=PostFrom
    template_name='postcreate.html'
    # messages.success("Your post successfully created")
    success_url=HttpResponseRedirect('/')
    def form_valid(self,form): 
        try:
            form.instance.user = self.request.user
            return super().form_valid(form)
        except:
            return HttpResponse('your post succesfully')
            # messages.success(request,"Your post successfully created")
            # return redirect('/calc/posts/')   
        # '/calc/posts/'   

            
            
# def postcreate(request):
#     if request.method=="Post":
#         form=PostFrom(request.Post,request.FILES)
#         if form.is_valid():
#             obj=form.save(commit=False)
#             obj.user=request.user
#             obj.save()
#     else:
#         form=PostFrom()
#     return render(request,'postcreate.html',{'form':form})      



def post_details(request, pk):
    queryset = get_object_or_404(Post, id=pk)
    comments = Comment.objects.filter(post=queryset, parent=None)
    replies = Comment.objects.filter(post=queryset).exclude(parent=None)
    Dictofreply={}
    for reply in replies:
        if reply.parent.id not in Dictofreply.keys():
            Dictofreply[reply.parent.id]=[reply]
        else:
            Dictofreply[reply.parent.id].append(reply)   
    context = {"queryset": queryset, 'pk':pk, 'comments':comments,'Dictofreply':Dictofreply}
    return render(request, 'post_details.html', context)

#from django.views.generic import UpdateView,DeleteView
#class PostEditView( UpdateView):
    #template_name='postcreate.html'
    #model=Post 
    #form_class=PostFrom
    #def get_success_url(self):
        #id= self.object.id
        #return reverse_lazy('postdetails', kwargs={'pk':id})
        
        

        
from django.views.generic import DeleteView       
class PostDeleteView(DeleteView):
    model=Post
    template_name='delete.html'
    success_url=reverse_lazy('calc:posts')
    
def commentdelete(request, pk):
    comment=Comment.objects.get(id=pk)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
    
def UpdateEdit(request, pk):
    post = Post.objects.get(id=pk)
    form=PostFrom(instance=post)
    if request.method=='POST':
         form=PostFrom(request.POST,instance=post)
         print(form.errors)
         if form.is_valid():
          form.save()
          
    context = {'form':form}
    return render(request, 'postcreate.html',context) 
    
    
# def deletepost(request, pk): 
#     post = Post.objects.get(id=pk)
#     context = {'post':post}
#     if request.method=="Post":
#         post.delete()
        
#     return render(request, 'delete.html',context)    


from notifications.signals import notify
def addcomment(request):
    if request.method=="POST":
        comment=request.POST['comment']
        print(comment)
        parentid=request.POST['parentid']
        postid=request.POST['postid']
        post=Post.objects.get(id=postid)
        if parentid:
            parent=Comment.objects.get(id=parentid)
            newcom=Comment(text=comment,user=request.user,post=post,parent=parent)
            newcom.save()
        else:
             newcom=Comment(text=comment,user=request.user,post=post)
             newcom.save()  
             if request.user != post.user:
                notify.send(request.user, recipient=post.user, verb="has comment your post" + f''' <a href="/calc/post/details/{post.id}/"> Go </a>''')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

def notification(request):
    return render(request, 'now/notification.html')    



