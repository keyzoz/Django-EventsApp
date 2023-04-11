from .models import Category

menu = [{'title': "Add a new event", "url_name":'add_event'},
        {'title': "Send a new mail", "url_name":'send_mail'} ]



class DataMixin:
    def get_user_context(self,**kwargs):
        context = kwargs
        cats = Category.objects.all()   
        user_menu = menu.copy()
        if not self.request.user.is_superuser:
                user_menu.clear()
        context["menu"] = user_menu
        context["category"] = cats
        if 'cat_selected' not in context:
                context['cat_selected'] = 0
        return context
        