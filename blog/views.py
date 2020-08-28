from django.shortcuts import render

# Create your views here.
# my-blog-page/

from django.http import HttpResponse

# importing loading from django template
from django.template import loader
from .models import Author


# our view which is a function named index
def index(request):
    # getting our template
    template = loader.get_template('blog/blog_authors.html')

    # rendering the template in HttpResponse
    ctx = {"authors": Author.objects.all()}
    return HttpResponse(template.render(context=ctx))
