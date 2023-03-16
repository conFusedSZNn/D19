
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormMixin
from .models import Post , Category
from .forms import PostForm, CommentForm, AuthUserForm, RegisterUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages



class CustomSuccessMessageMixin:

    @property
    def success_msg(self):
        return False

    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)



class PostList(ListView):
    model = Post
    template_name = 'mmorpj/index.html'
    context_object_name = 'list_posts'


class CategoryList(ListView):
    model = Category
    template_name = 'mmorpj/post_edit.html'
    context_object_name = 'category_list'

class PostDetail(DetailView, FormMixin,):
    model = Post
    template_name = 'mmorpj/1post.html'
    context_object_name = 'get_post'
    form_class = CommentForm
    success_url = 'Отклик отправлен'

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail_page', kwargs = {'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.reply_link_post = self.get_object()
        self.object.author_reply = self.request.user
        self.object.save()
        return super().form_valid(form)

class CustomSuccessMessageMixin:

    @property
    def success_msg(self):
        return False

    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

class PostCreate(CreateView, CustomSuccessMessageMixin, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'mmorpj/post_edit.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Объявление создано'

    def get_context_data(self, **kwargs):
        kwargs['list_posts'] = Post.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class PostEdit(UpdateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'mmorpj/post_edit.html'
    success_url = reverse_lazy('edit_page')


    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs

class D19LoginView(LoginView):
    template_name = 'mmorpj/login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')
    def get_success_url(self):
        return self.success_url

class D19LogoutView(LogoutView):
    next_page = reverse_lazy('edit_page')


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'mmorpj/register_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Пользователь успешно создан'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username = username, password= password)
        login(self.request, aut_user)
        return form_valid
