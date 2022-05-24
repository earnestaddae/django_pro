from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.jinja'

class AboutPageView(TemplateView):
    template_name = 'about.jinja'
