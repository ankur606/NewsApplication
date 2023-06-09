from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.html import strip_tags
class UserRegistrationSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Users
        fields = ['full_name', 'email', 'mobile_number']
        extra_kwargs = {
            'full_name':{'required': True,},
            'email':{'required': True,},
            'mobile_number':{'required': True,},
        }
    
    def create(self, validate_data):
        return Users.objects.create_user(**validate_data)  

class UserLoginSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()
  
    class Meta:
        model = Users
        fields = ['mobile_number']
        extra_kwargs = {
            'mobile_number':{'required': True,},
        }
class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id',  'name',  'surname', 'nickname', 'email', 'mobile_number', 'image_url' ]   

class ListsCategoriesSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField()
    sub = serializers.SerializerMethodField()

    def get_follow(self, obj):
        user = self.context.get('user')
        follows = FavouriteCategories.objects.filter(category_id=obj.id, user_id = user)
        if follows:
            return 1
        else: 
            return 0
    def get_sub(self, obj):
      
        sub = Categories.objects.filter(parent_id=obj.id)

        if Categories.objects.filter(parent_id=obj.id).exists():
            sub = Categories.objects.filter(parent_id=obj.id).count()
            return sub
        else:
            sub = 0
            return sub
    class Meta:
        model = Categories
        fields = ['id','image_url', 'title', 'follow', 'sub' ]        
                      
class ListsSubCategoriesSerializer(serializers.ModelSerializer):
    follow = serializers.SerializerMethodField()

    def get_follow(self, obj):
        user = self.context.get('user')
        follows = FavouriteCategories.objects.filter(category_id=obj.id, user_id = user)
        if follows:
            return 1
        else: 
            return 0
    class Meta:
        model = Categories
        fields = ['id','created_at' , 'image_url' , 'title', 'follow']  

class GiocatoriDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Giocatori
        fields = ['id','image_url', 'nome', 'data_nascita', 'ruolo', 'squadra']   

class CalendarioDetailsSerializer(serializers.ModelSerializer):
    casa_image = serializers.SerializerMethodField()
    trasferta_image = serializers.SerializerMethodField()

    def get_casa_image(self, obj):
        casa_image = self.context.get('casa_image')
      
        return casa_image
    def get_trasferta_image(self, obj):
        trasferta_image = self.context.get('trasferta_image')
        return trasferta_image
    
    class Meta:
        model = Calendario
        fields = ['id', 'casa', 'casa_image', 'trasferta', 'trasferta_image', 'data_ora', 'gol_casa', 'gol_trasferta', 'giornata', 'stagione' ]   
        extra_kwargs = {
            'stagione':{'required': True,},
            }
class SquadreDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Squadre
        fields = [ 'image_url', 'title', 'bg_color_rgba', 'app_bg_color_rgba' ]   

class PostDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'guid', 'provider_profile_id', 'category_id', 'title', 'description', 'about', 'address', 'start_date', 'end_date', 'image_url', 'link', 'data', 'video', 'created_at', 'updated_at', 'active' ]   
        extra_kwargs = {
            'id':{'required': True,},
        }

class PostCommentSerializer(serializers.ModelSerializer):
    review = serializers.CharField()    
    class Meta:
        model = Ratings
        fields = ['review', 'provider_id', 'user', 'post_id', 'is_online', 'created_at']
        extra_kwargs = {
            'review':{'required': True,},
            'provider_id':{'required': True,},
            'user':{'required': True,},
            'post_id':{'required': True,},
        }                        

             
class EventListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'title', 'about', 'address', 'start_date', 'end_date', 'interested_count', 'image_url', 'video', 'featured' ]   

class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id',  'image_url', 'title']   

class TblPostCoverListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TblPostCover
        fields = ['id', 'event_id',  'image_file' ]   


class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id','image_url', 'title',   ] 
        extra_kwargs = {
            'id':{'required': True,},
        }

class EsportDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id','provider_profile_id', 'title', 'about', 'address', 'start_date', 'end_date', 'image_url',  'video', 'created_at', 'updated_at', ]   
        
        extra_kwargs = {
            'id':{'required': True,},
        }

class FantacalcioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ['id', 'guid', 'provider_profile_id', 'category_id', 'title', 'description', 'about', 'address', 'start_date', 'end_date', 'image_url', 'link', 'data', 'video', 'created_at', 'updated_at', 'active' ]   
        
        extra_kwargs = {
            'id':{'required': True,},
        }
class SeasonListsSerializer(serializers.ModelSerializer):
    GIOCATORI = serializers.SerializerMethodField()
    SQUADRE = serializers.SerializerMethodField()
    CALENDARIO = serializers.SerializerMethodField()
    giocatori_image = serializers.SerializerMethodField()
    celendrio_image = serializers.SerializerMethodField()
    squadre_image = serializers.SerializerMethodField()

    def get_GIOCATORI(self, obj):
        GIOCATORI = "GIOCATORI" 
        return GIOCATORI
    
    def get_SQUADRE(self, obj):
        SQUADRE = "SQUADRE" 
        return SQUADRE
    
    def get_CALENDARIO(self, obj):
        CALENDARIO = "CALENDARIO" 
        return CALENDARIO
    
    def get_giocatori_image(self, obj):
        giocatori_image = "/media/player.png" 
        return giocatori_image
    
    def get_celendrio_image(self, obj):
        celendrio_image = "/media/celender.png" 
        return celendrio_image
    
    def get_squadre_image(self, obj):
        squadre_image = "/media/team.png" 
        return squadre_image
    class Meta:
        model = FcSeasons
        fields = [ 'id', 'code_id', 'synced', 'image_url', 'season_api', 'title', 'image_url', 'bg_color_rgba', 'app_bg_color_rgba', 'GIOCATORI','giocatori_image', 'SQUADRE', 'celendrio_image', 'CALENDARIO', 'squadre_image', 'created_at', 'updated_at' ]   
      
class FollowCategorySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = FavouriteCategories
        fields = ['category_id', 'user_id',]   
        extra_kwargs = {
            'category_id':{'required': True,},
            'user_id':{'required': True,},
        }

class PostReactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReact
        fields = ['user_id', 'post_id', 'reaction']   
        extra_kwargs = {
            'user_id':{'required': True,},
            'post_id':{'required': True,},
            'reaction':{'required': True,}, 
        }
class PostReactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReact
        fields = ['post_id']   
        extra_kwargs = {
            'post_id':{'required': True,},
         
        }
class GiocatoriRecordsLists(serializers.ModelSerializer):
    class Meta:
        model = FcPlayerStats
        fields = ['p_first_name', 'p_last_name', 'p_birth_date', 'r_name', 'p_url_xs', 'p_number', 'pr_role', 'player_code_id', 'turn_code_id']

class SeasonPlayerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcPlayerStats
        fields = [ 'id',  'player_code_id', 'turn_code_id',  'pns_played', 'pns_goal', 'pi_overall_season_index', 'p_lineup_rating', 'pns_assist', 'pns_yellow_card', 'pns_played_draw', 'pl_predicted_note', 'pns_goal_subout', 'pns_penalty_failed', 'pi_expected_penalty', 'pns_note_win', 'pns_note_lose', 'pns_note_last5', 'pns_score_last5', 'pns_note', 'pr_role', 'r_name', 'p_url_xs', 'pl_predicted_note', 'pns_goal_full', 'pi_match_played_perc']   


class SeasonTeamsSerializer(serializers.ModelSerializer):
   class Meta:
        model = FcTeams
        fields = [ 'id',  'title', 'image_url',]   

class PlayersListsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FcPlayers
        fields = [ 'first_name',  'last_name', 'birth_date', 'code_role', 'image_url', 'main_role', 'code_id']   

class CelenderRecordsLists(serializers.ModelSerializer):
    class Meta:
        model = FcTurns
        fields = ['id']

class WelcomeScreenSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Introductions
        fields = [ 'id',  'title','description', 'image_url',]   

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['description'] = strip_tags(instance.description)
        return data

class SettingsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ['id', 'key', 'value']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['value'] = strip_tags(instance.value)
        return data


class SquadreSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField()
    title = serializers.CharField()
    bg_color_rgba = serializers.CharField()
    app_bg_color_rgba = serializers.CharField()

    class Meta:
        model = Squadre
        fields = ['image_url', 'title', 'bg_color_rgba', 'app_bg_color_rgba']
