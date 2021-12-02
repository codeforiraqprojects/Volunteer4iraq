from django.urls import path
from . import views, IntitiesViews ,UserViews
from volunteer import settings
from django.conf.urls.static import static
from django.contrib.auth import views as authviews
from .IntitiesViews import Intities, LikeViewUser,SearchIntitiesResultsView,SearchPosterEduResultsView,SearchPosterEnvResultsView,SearchPosterHeaResultsView,SearchPosterArtResultsView,SearchPosterOthResultsView,LikeView
from .UserViews import SearchIntitiesResultsView1,SearchPosterEduResultsView1,SearchPosterEnvResultsView1,SearchPosterHeaResultsView1,SearchPosterArtResultsView1,SearchPosterOthResultsView1,LikeView1,LikeViewUser1
# from django.contrib.auth.views import LogoutView

# # from .IntitiesViews import IntitiesCreateView,IntitiesUpdateView

urlpatterns = [

# url Path For Intities
    path('dashboard/', IntitiesViews.dashboard, name='dashboard'),
    path('admin_home',IntitiesViews.admin_home,name="admin_home"),
    path('profile/',IntitiesViews.Profile,name="profile"),
    path('profile_update/<str:user_id>', IntitiesViews.ProfileUpdate, name='profile_update'),
    path('profile_edit_admin', IntitiesViews.ProfileEdit, name='profile_edit_admin'),
    path('details1/', IntitiesViews.Details, name='details1'),
    path('intities1/', IntitiesViews.Intities, name='intities1'),
    path('view_imageP/', IntitiesViews.ViewImageP, name='view_imageP'),
    path('more_read_intities/<str:intity_id>', IntitiesViews.More_Read_Intities, name='more_read_intities'),
    path('profile_intities/', IntitiesViews.Profile_Intities,name="profile_intities"),
    path('add_intities_save',IntitiesViews.Add_Intities_Save,name="add_intities_save"),
    path('update_intities/<str:intity_id>',IntitiesViews.Update_Intities,name='update_intities'),
    path('edit_intities',IntitiesViews.Edit_Intities_Save,name='edit_intities'),
    path('delete_intities/<str:intity_id>',IntitiesViews.delete_intities,name='delete_intities'),
    path('search_Intities/', SearchIntitiesResultsView.as_view(), name='search_Intities_results'),

    path('poster/', IntitiesViews.Declaration, name='poster'),
    path('my_poster/<str:poster_id>', IntitiesViews.my_declaration, name='my_poster'),
    path('search_PosterEdu_results/', SearchPosterEduResultsView.as_view(), name='search_PosterEdu_results'),
    path('search_PosterEnv_results/', SearchPosterEnvResultsView.as_view(), name='search_PosterEnv_results'),
    path('search_PosterHea_results/', SearchPosterHeaResultsView.as_view(), name='search_PosterHea_results'),
    path('search_PosterArt_results/', SearchPosterArtResultsView.as_view(), name='search_PosterArt_results'),
    path('search_PosterOth_results/', SearchPosterOthResultsView.as_view(), name='search_PosterOth_results'),
    path('save_poster', IntitiesViews.Save_Poster, name='save_poster'),
    path('delete_poster/<str:poster_id>', IntitiesViews.DeletePoster, name='delete_poster'),
    path('update_poster/<str:poster_id>', IntitiesViews.update_poster, name='update_poster'),
    path('edit_poster' , IntitiesViews.edit_poster, name='edit_poster'),
    
    path('notification/', IntitiesViews.Notification, name='notification'),
    path('add_volunteer', IntitiesViews.AddVolunteer, name='add_volunteer'),
    path('delete_volunteer/<str:notification_id>', IntitiesViews.DeleteVolunteer, name='delete_volunteer'),
    path('about1/', IntitiesViews.About, name='about1'),
    path('comments/',IntitiesViews.comments, name='comments'),
    path('like/<int:pk>',LikeView,name='like_comment'),
    path('like_user/<int:pk>',LikeViewUser,name='like_comment_user'),
    path('add_comment_save', IntitiesViews.Add_Comment_Save , name='add_comment_save'),
    path('delete_comment/<str:comment_id>' ,IntitiesViews.delete_comment, name='delete_comment'),
    path('delete_comment_user/<str:comment_user_id>' ,IntitiesViews.delete_comment_user, name='delete_comment_user'),
    # path('reply',IntitiesViews.ComReply, name='reply'),
    # path('search_members/', SearchMemberView, name='search_members'),
    path('manage_members/<str:member_id>',IntitiesViews.Manage_Members,name="manage_members"),
    path('add_member_save',IntitiesViews.Add_Member_Save,name="add_member_save"),
    path('update_member/<str:member_id>' , IntitiesViews.update_member, name='update_member'),
    path('edit_member' , IntitiesViews.edit_member, name='edit_member'),
    path('delete_member/<str:member_id>' , IntitiesViews.delete_member, name='delete_member'),
    path('deletes' , IntitiesViews.deletes, name='deletes'),
    









# # url Path For user
    path('user_home',UserViews.user_home,name="user_home"),
    path('profile1',UserViews.Profile1,name="profile1"),
    path('profile_update1/<str:user_id>', UserViews.ProfileUpdate1, name='profile_update1'),
    path('profile_edit_user', UserViews.ProfileEdit1, name='profile_edit_user'),
    path('details2/', UserViews.Details2, name='details2'),
    path('intities2/', UserViews.Intities2, name='intities2'),
    path('more_read_intities1/<str:intity_id>', UserViews.More_Read_Intities1, name='more_read_intities1'),
    path('search_Intities1/', SearchIntitiesResultsView1.as_view(), name='search_Intities_results1'),
    path('profile_intities1/', UserViews.Profile_Intities1,name="profile_intities1"),

    path('poster1/', UserViews.Declaration1, name='poster1'),
    path('search_PosterEdu_results1/', SearchPosterEduResultsView1.as_view(), name='search_PosterEdu_results1'),
    path('search_PosterEnv_results1/', SearchPosterEnvResultsView1.as_view(), name='search_PosterEnv_results1'),
    path('search_PosterHea_results1/', SearchPosterHeaResultsView1.as_view(), name='search_PosterHea_results1'),
    path('search_PosterArt_results1/', SearchPosterArtResultsView1.as_view(), name='search_PosterArt_results1'),
    path('search_PosterOth_results1/', SearchPosterOthResultsView1.as_view(), name='search_PosterOth_results1'),

    path('add_notification/', UserViews.Add_Notification, name='add_notification'),
    path('send_notification', UserViews.Send_Notification, name='send_notification'),
    path('about2/', UserViews.About2, name='about2'),
    path('comments1/',UserViews.comments1, name='comments1'),
    path('like1/<int:pk>',LikeView1,name='like_comment1'),
    path('like_user1/<int:pk>',LikeViewUser1,name='like_comment_user1'),
    path('add_comment_save1', UserViews.Add_Comment_Save_User , name='add_comment_save1'),
    # path('delete_comment/<str:comment_id>' ,IntitiesViews.delete_comment, name='delete_comment'),
    path('delete_comment_user1/<str:comment_user_id>' ,UserViews.delete_comment_user1, name='delete_comment_user1'),
#     # path('dashboard/', UserViews .dashboard, name='dashboard'),
#     # path('add_intities_save',UserViews .Add_Intities_Save,name="add_intities_save"),
#     # path('edit_information',UserViews .Edit_Information,name="edit_information"),
#     # path('manage_members',UserViews .Manage_Members,name="manage_members"),
#     # path('add_member_save',UserViews .Add_Member_Save,name="add_member_save"),
#     # path('update_member/<str:member_id>' , IntitiesViews.update_member, name='update_member'),
#     # path('edit_member' , UserViews .edit_member, name='edit_member'),
#     # path('delete_member/<str:member_id>' , IntitiesViews.delete_member, name='delete_member'),


]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


