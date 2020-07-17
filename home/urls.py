from django.urls import path
from .views import login_view, faculty_register_view, home_view, logout_view, examblock_view\
    , assessment_view, faculty_details_view, examblock_add, examblock_edit, assessment_add, assessment_edit, faculty_assement_edit

urlpatterns= [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
    path('register', faculty_register_view, name='register'),
    path('logout', logout_view, name='logout'),
    path('examblock', examblock_view, name='exam_block'),
    path('assessment', assessment_view, name='assessment'),
    path('faculty', faculty_details_view, name='faculty_details'),
    path('examblock/add', examblock_add, name='exam_block_add'),
    path('examblock/<int:id>', examblock_edit, name='exam_block_edit'),
    path('assessment/add', assessment_add, name='assessment_add'),
    path('assessment/<int:id>', assessment_edit, name='assessment_edit'),
    path('faculy_assessment/<int:id>', faculty_assement_edit, name='faculty_assessment_edit')

]
