from .dental_problem import urlpatterns as dental_problem_urls
from .dentist import urlpatterns as dentist_urls
from .patient import urlpatterns as patient_urls
from .settings import urlpatterns as settings_urls
from .settings import urlpatterns as settings_urls
from .treatment import urlpatterns as treatment_urls
from .user import urlpatterns as user_urls

urlpatterns = [
    *dentist_urls,
    *patient_urls,
    *settings_urls,
    *dental_problem_urls,
    *user_urls,
    *treatment_urls,
]
