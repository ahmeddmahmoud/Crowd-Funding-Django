from django.urls import path,include
from users.views import user_details,login_form,register,index, user_delete,activate,featured_projects,add_to_featured,user_edit,admin_dashboard,category_index,delete_category,edit_category,add_category,tag_index,add_tag,edit_tag,delete_tag,user_index,delete_user_by_admin,add_user_by_admin,edit_user_by_admin,user_donations,user_projects,categories_project,user_logout

urlpatterns = [
    path('register/', register, name="user.register"),
    path('edit/<int:id>', user_edit, name="user.edit"),
    path('', index, name="index"),
    path('login/', login_form, name="user.login"),
    path('details/<int:id>',user_details , name="user.details"),
    path('delete/<int:id>',user_delete , name="user.delete"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('admin/', admin_dashboard , name="admin.dashboard"),
    path('admin/category/', category_index , name="category.index"),
    path('admin/category/<int:id>/delete', delete_category, name='category.delete'),
    path('admin/category/<int:id>/edit', edit_category, name='category.edit'),
    path('admin/category/add', add_category, name='category.add'),
    path('admin/tag/', tag_index, name='tag.index'),
    path('admin/tag/add', add_tag, name='tag.add'),
    path('admin/tag/<int:id>/edit', edit_tag, name='tag.edit'),
    path('admin/tag/<int:id>/delete', delete_tag, name='tag.delete'),
    path('admin/featured/', featured_projects, name="featured"),
    path('admin/user/', user_index, name='user.index'),
    path('admin/user/<int:id>/delete', delete_user_by_admin, name='user.delete.by.admin'),
    path('admin/user/add/', add_user_by_admin, name='add.user.by.admin'),
    path('admin/user/<int:id>/edit', edit_user_by_admin, name='edit.user.by.admin'),
    path('featured/', featured_projects , name="featured"),
    path('add_to_featured/<int:id>', add_to_featured, name="add.to.featured"),
    path('donations/<int:id>', user_donations , name="user.donations"),
    path('projects/<int:id>', user_projects , name="user.projects"),
    path('categories', categories_project , name="categories.projects"),
    path('logout/', user_logout, name='logout'),

]