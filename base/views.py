from django.shortcuts import render,redirect
# from django.http import HttpResponse # remove because we will use class based view
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


# since it's login and will come first, write at the start
class CustomLoginView(LoginView):
	template_name = 'base/login.html'
	fields = '__all__'
	redirect_authenticated_user = True # user should not be here if authenticated already

	#overwrite success url
	def get_success_url(self):
		#if success, go to list page
		return reverse_lazy('tasks')

class RegisterPage(FormView):
	template_name = 'base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user = True
	success_url = reverse_lazy('tasks')

	# redirect user if submit success
	def form_valid(self,form):
		user = form.save() # coz we are creating user form
		if user is not None: # if user can be created
			login(self.request,user)
		return super(RegisterPage,self).form_valid(form)

	# if trying to register with logged in, redirect to task list
	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('tasks')
		return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin,ListView): # inherit it
	model = Task
	context_object_name = 'tasks' # without it, will just look for object_list

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs) # all fields in model as default
		context['tasks'] = context['tasks'].filter(user=self.request.user) # filter so that task can be only the ones created by user
		context['count'] = context['tasks'].filter(complete=False).count()

		search_input = self.request.GET.get('search-area') or '' # text box name
		if search_input: # if we search, we will give only search items.. if not searched.. as filtered for all users
			context['tasks'] = context['tasks'].filter(title__startswith=search_input)

		context['search_input'] = search_input
		return context


class TaskDetail(LoginRequiredMixin,DetailView):
	model = Task
	context_object_name = 'task' # without it, will just look for object
	template_name = 'base/task.html' #without it, will just look for task_detail.html

class TaskCreate(LoginRequiredMixin,CreateView):
	model = Task
	# fields = '__all__' # all fields will show
	fields=['title','description','complete']
	success_url = reverse_lazy('tasks') # if all ok, just send user back to list.. tasks is the url name of list in urls.py

	def form_valid(self,form):
		form.instance.user = self.request.user
		return super(TaskCreate,self).form_valid(form)



class TaskUpdate(LoginRequiredMixin,UpdateView):
	model = Task
	fields=['title','description','complete']
	success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin,DeleteView):
	model = Task
	context_object_name = 'task'
	success_url = reverse_lazy('tasks')
