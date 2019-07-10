from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"


class FormsView(TemplateView):
    template_name = "forms.html"
