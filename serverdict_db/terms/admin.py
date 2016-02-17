from django.contrib import admin
from terms import models as term_models

# Register your models here.

admin.site.register(term_models.Author)
admin.site.register(term_models.APIToken)
admin.site.register(term_models.Category)
admin.site.register(term_models.Term)
