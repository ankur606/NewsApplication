from django.urls import path
from django import views
from . import views

urlpatterns = [
   
    path('about-us-page', views.About_Us_Page.as_view(), name="aboutpage" ),
    path('privacy-policy', views.Privacy_Policy_Page.as_view(), name="aboutpage" ),
    path('api/welcome-screen', views.Welcome_Screen.as_view(), name="welcomeScreen" ),
    path("api/user-register", views.UserRegistration.as_view(), name='register'),
    path("api/user-login", views.UserLoginView.as_view(), name='userLogin'),
    path('api/verify-number', views.VerifyMobileNumber.as_view(), name="number"),
    path("api/categories-lists", views.ListCategories.as_view(), name='Listscategory'),
    path("api/sub-categories-lists", views.ListSubCategories.as_view(), name='SubcategoryLists'),
    path("api/user-profile", views.UserProfileUpdateView.as_view(), name='updateProfile'),
    path("api/calendario-lists", views.ListsCalendario.as_view(), name='calendarioLists'),
    path("api/giocatori-lists", views.ListsGiocatori.as_view(), name='GiocatoriLists'),
    path("api/squadre-lists", views.ListsSquadre.as_view(), name='SquadreLists'),
    path("api/post-lists/", views.PostLists.as_view(), name='PostLists'),
    path("api/post-details", views.PostDetails.as_view(), name='PostDetails'),
    path("api/post-comment", views.PostComment.as_view(), name="postComment"),
    path("api/recent-post-comment-lists", views.RecentPostComments.as_view(), name="RecentpostComment"),
    path("api/post-all-comment-lists", views.PostAllComments.as_view(), name="postComment"),
    path("api/welcome-screen-latest-news-lists", views.LatestNewsCarouselImageLists.as_view(), name='CarouselImageLists'),
    path("api/event-lists", views.EventsList.as_view(), name='PostLists'),
    path("api/latest-events-carousel-image-lists", views.LatestEventsCarouselImageLists.as_view(), name="Latest-Events"),
    path("api/event-cover-image-lists", views.EventCoverImages.as_view(),  name='EventCoverImage'),
    path("api/contact-us", views.ContactUs.as_view(), name="ContactUs"),
    path("api/category-details", views.CategoryDetails.as_view(), name="Categorydetails"),
    path("api/e-sport-details", views.E_SportDetails.as_view(), name="eSportCategorydetails"),
    path("api/fantacalcio-season-lists", views.FantacalcioSeasonsLists.as_view(), name="FantacalcioSeasonLists"),
    path('api/fantacalcio-images', views.Fantacalcio_Image.as_view(), name="FantaImages"),
    path("api/search-recoard", views.SearchRecoard.as_view(), name="SearchRecoard"),
    path('api/follow-category', views.Follow_Category.as_view(), name="FollowCategory"),
    path('api/follow-sub-category', views.Follow_Sub_Category.as_view(), name="FollowSubCategory"),
    path('api/favourite-events', views.FavouriteEventsView.as_view(), name="favouriteEvents"),
    path('api/favorite-events-lists', views.UserFavouriteEventsLists.as_view(), name="FvEvents" ),
    path('api/post-react', views.PostReactView.as_view(), name="PostReact"),
    path('api/post-react-details', views.PostReactDetails.as_view(), name="PostReactDetails"),
    path('api/giocateori-records-lists', views.GiocateoriLists.as_view(), name="RecordLists"),
    path('api/role-lists', views.RoleListsView.as_view(), name="RoleLists"),
    path('api/player-status', views.PlayerStatus.as_view(), name="PlayerStatus"),
    path('api/team-turn-record-lists', views.TurnsRecordsDetails.as_view(), name="TurnRecords"),
    path("api/season-all-teams", views.FcSeasonSquadreLists.as_view(), name="SeasonTeams" ),
    path('api/teams-players-lists', views.SeasonTeamsPlayers.as_view(), name="Players"),
    path("api/season-celender-lists", views.CelenderLists.as_view(), name="CelenderLists"),
    path("api/all-turns-lists", views.AllTurnsLists.as_view(), name="TurnsLists"),
    path('api/similar-post', views.SimilarPost.as_view(), name="SimilarPost"),
    path('api/welcome-screen-page', views.WelcomeScreenss.as_view(), name="Welcome"),
    path('api/settings-informations', views.InfomationSettings.as_view(), name="settings"), 
    path('terms-conditions', views.TermsConditionsPage.as_view(), name="Terms Conditions"),
    # path('update-images', views.UpdatePlayersRecords.as_view(), )

]





