from django.db import models
from django import forms

# Create your models here.
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField


from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index
from wagtail.snippets.models import register_snippet


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]
    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
    ]

    def get_posts(self):
        return self.get_children()

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.get_posts()
        return context

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return BlogIndexPage.serve(self, request, *args, **kwargs)


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    quote = models.CharField(max_length=250, default='', blank=True)
    author = models.CharField(max_length=100)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('author')
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, "Common page configuration"),
        ImageChooserPanel('feed_image'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple)
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('quote'),
        FieldPanel('author')
    ]

    parent_page_types = ['blog.BlogIndexPage']

    @property
    def parent_page(self):
        return self.get_parent().specific

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['parent_page'] = self.parent_page
        return context
