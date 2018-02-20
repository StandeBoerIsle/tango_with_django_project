from django.core.urlresolvers import reverse
from django.test import TestCase
from rango.models import Category, Page
from django.utils import timezone
from django.contrib.staticfiles import finders


class CategoryMethodTests(TestCase):
    # Tests that focus on ensuring the integrity of the data housed in the models.

    def test_ensure_views_are_positive(self):
        """
        ensure_views_are_positive should results True for categories where views are zero or positive
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        """
        slug_line_creation checks to make sure that when we add
        a category an appropriate slug line is created
        i.e. "Random Category String" -> "random-category-string"
        """
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


class IndexViewTests(TestCase):
    # Tests to check the views
    def test_index_view_with_no_categories(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        """
        If some categories exist, they should be displayed.
        """
        add_cat('test', 1, 1)
        add_cat('temp', 1, 1)
        add_cat('tmp', 1, 1)
        add_cat('tmp test temp', 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tmp test temp")
        self.assertEqual(len(response.context['categories']), 4)


class AddPageTest(TestCase):
    def test_visits_are_not_future(self):
        category = Category.objects.get_or_create(name='Python')[0]
        page = Page.objects.get_or_create(category=category, title="Main", url="www.python.org")[0]
        self.assertGreaterEqual(timezone.now(), page.last_visit)
        self.assertGreaterEqual(timezone.now(), page.first_visit)

    def test_last_visit_is_later_than_first(self):
        category = Category.objects.get_or_create(name='Python')[0]
        page = Page.objects.get_or_create(category=category, title="Main", url="www.python.org")[0]
        self.assertGreaterEqual(page.last_visit, page.first_visit)
