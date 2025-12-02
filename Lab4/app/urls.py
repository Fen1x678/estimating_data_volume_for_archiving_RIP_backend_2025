from django.urls import path
from .views import *

urlpatterns = [
    path('api/algorithms/', search_algorithms),  # GET
    path('api/algorithms/<int:algorithm_id>/', get_algorithm_by_id),  # GET
    path('api/algorithms/<int:algorithm_id>/update/', update_algorithm),  # PUT
    path('api/algorithms/<int:algorithm_id>/update_image/', update_algorithm_image),  # POST
    path('api/algorithms/<int:algorithm_id>/delete/', delete_algorithm),  # DELETE
    path('api/algorithms/create/', create_algorithm),  # POST
    path('api/algorithms/<int:algorithm_id>/add_to_compression/', add_algorithm_to_compression),  # POST

    path('api/compressions/', search_compressions),  # GET
    path('api/compressions/cart/', get_cart_info),  # GET
    path('api/compressions/<int:compression_id>/', get_compression_by_id),  # GET
    path('api/compressions/<int:compression_id>/update/', update_compression),  # PUT
    path('api/compressions/<int:compression_id>/update_status_user/', update_status_user),  # PUT
    path('api/compressions/<int:compression_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/compressions/<int:compression_id>/delete/', delete_compression),  # DELETE

    path('api/compressions/<int:compression_id>/update_algorithm/<int:algorithm_id>/', update_algorithm_in_compression),  # PUT
    path('api/compressions/<int:compression_id>/delete_algorithm/<int:algorithm_id>/', delete_algorithm_from_compression),  # DELETE

    path('api/users/register/', register), # POST
    path('api/users/update/', update_user), # PUT
    path("api/users/info/", user_info), # GET
    path('api/users/login/', login), # POST
    path('api/users/logout/', logout), # POST
]
