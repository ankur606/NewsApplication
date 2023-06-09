from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self , full_name, email, mobile_number, password = '12345'):
   
        if not mobile_number:
            raise ValueError('The Mobile Number must be Set')
      
        user = self.model(
            email = self.normalize_email(email),
            mobile_number = mobile_number,
            
        )
        name_parts = full_name.split(' ')
        
     
        # for i in range(len(name_parts)):
        #     if i == 0:
        #         user.surname = name_parts[i]
        #     elif i == 1:
        #         user.nickname = name_parts[1] + ' ' + name_parts[2] + ' ' + name_parts[3]

        if len(name_parts) > 0:
            user.surname = name_parts[0]
        if len(name_parts) > 1:
            nickname_parts = name_parts[1:]
            user.name = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
        if len(name_parts) > 1:
            nickname_parts = name_parts[1:]
            user.nickname = ' '.join(nickname_parts) if len(nickname_parts) > 1 else nickname_parts[0]
        
        user.mobile_verified = 1
        user.active = 1
        user.confirmation_code = 1
        
        user.set_password(password)
        user.save(using=self._db)
        UsersRoles.objects.create(user=user, role=Roles.objects.get(name='customer'))
        return user

    def create_superuser(self, full_name,  email,mobile_number, password = '12345' ):
        """
        Creates and saves a superuser with the given email, name, 'category and password.
        """
        user = self.create_user(
            email = self.normalize_email(email),
            full_name = full_name,
            mobile_number = mobile_number,
            
            password = password,
        )
        user.is_admin = True
        user.is_superuser = True

        user.save(using = self._db)
        return user    

class Users(AbstractBaseUser, BaseUserManager):
    
    surname = models.CharField(max_length=191, blank=True, null=True, default=" ")
    name = models.CharField(max_length=191, blank=True, null=True, default="") 

    nickname = models.CharField(max_length=191, blank=True, null=True, default= ' ')
    gender = models.CharField(max_length=1, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    email = models.CharField(unique=True, max_length=191, blank=True, null=True)
    password = models.CharField(max_length=191, blank=True, null=True)
    image_url = models.FileField(default="/about.jpg",  blank=True)
    mobile_number = models.CharField(unique=True, max_length=15, blank=True, null=True )
    mobile_verified = models.IntegerField(default=0, blank=True, null=True)
    active = models.PositiveIntegerField(default=1,blank=True, null=True)
    confirmation_code = models.CharField(max_length=500, blank=False, null=False)
    confirmed = models.IntegerField(default=1)
    fcm_registration_id = models.CharField(max_length=191, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)    
    note = models.TextField(blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'users'

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name','email']

    def __str__(self):
      return self.mobile_number

    def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

    def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

    @property
    def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin 

class Categories(models.Model):
    title = models.CharField(max_length=191)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    parent_id = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    app_bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'categories'

class CategoriesProviderProfiles(models.Model):
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    provider_profile = models.ForeignKey('ProviderProfiles', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories_provider_profiles'
        unique_together = (('category', 'provider_profile'),)

class Diffidati(models.Model):
    id_giocatore = models.IntegerField()
    giornata = models.IntegerField(blank=True, null=True)
    stagione = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'diffidati'

class Events(models.Model):
    provider_profile = models.ForeignKey('ProviderProfiles', models.DO_NOTHING)
    title = models.CharField(max_length=191)
    about = models.TextField()
    address = models.CharField(max_length=191, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=7)
    latitude = models.DecimalField(max_digits=15, decimal_places=7)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interested_count = models.IntegerField()
    image_url = models.CharField(max_length=500, blank=True, null=True)
    video = models.CharField(max_length=50, blank=True, null=True)
    featured = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'events'
class Faq(models.Model):
    title = models.CharField(max_length=191)
    short_description = models.CharField(max_length=191)
    description = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'faq'
class FavouriteCategories(models.Model):
    user_id = models.PositiveIntegerField()
    category_id = models.PositiveIntegerField()
    sub_category_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)    
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta: 
        managed = False
        db_table = 'favourite_categories'   
        unique_together = (('user_id', 'category_id'),)
class FavouriteEvents(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    event_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite_events'
        unique_together = (('user', 'event_id'),)

class FavouriteOffers(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    offer = models.ForeignKey('Offers', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favourite_offers'
        unique_together = (('user', 'offer'),)

class Favourites(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    provider = models.ForeignKey('ProviderProfiles', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'favourites'
        unique_together = (('user', 'provider'),)


class FcPlayerStats(models.Model):
    player_code_id = models.IntegerField()
    turn_code_id = models.IntegerField()
    season_code = models.ForeignKey('FcSeasons', models.DO_NOTHING, to_field='code_id')
    team_code_id = models.IntegerField()
    season_match_code = models.ForeignKey('FcSeasonMatches', models.DO_NOTHING, to_field='code_id')
    p_first_name = models.CharField(max_length=50)
    p_last_name = models.CharField(max_length=50)
    p_birth_date = models.DateField()
    p_number = models.IntegerField(blank=True, null=True)
    p_kapitals = models.FloatField()
    p_value = models.IntegerField(blank=True, null=True)
    p_rating = models.FloatField(blank=True, null=True)
    p_lineup_rating = models.FloatField(blank=True, null=True)
    p_field_position = models.IntegerField(blank=True, null=True)
    p_penalty = models.IntegerField(blank=True, null=True)
    p_set_pieces = models.IntegerField(blank=True, null=True)
    p_exp_assist = models.IntegerField(blank=True, null=True)
    p_exp_goal = models.IntegerField(blank=True, null=True)
    p_url_xs = models.CharField(max_length=191, blank=True, null=True)
    p_injured_until = models.DateField(blank=True, null=True)
    pr_role = models.IntegerField(blank=True, null=True)
    r_name = models.CharField(max_length=50, blank=True, null=True)
    pl_predicted_note = models.FloatField(blank=True, null=True)
    pns_goal_full = models.IntegerField(blank=True, null=True)
    pns_minutes_easy = models.IntegerField(blank=True, null=True)
    pns_goal_easy = models.IntegerField(blank=True, null=True)
    pns_note = models.FloatField(blank=True, null=True)
    pns_score = models.FloatField(blank=True, null=True)
    pns_note_65 = models.FloatField(blank=True, null=True)
    pns_note_55 = models.FloatField(blank=True, null=True)
    pns_note_last5 = models.FloatField(blank=True, null=True)
    pns_note_home = models.FloatField(blank=True, null=True)
    pns_note_away = models.FloatField(blank=True, null=True)
    pns_note_easy = models.FloatField(blank=True, null=True)
    pns_played = models.IntegerField(blank=True, null=True)
    pns_played_65 = models.IntegerField(blank=True, null=True)
    pns_played_55 = models.IntegerField(blank=True, null=True)
    pns_played_last5 = models.IntegerField(blank=True, null=True)
    pns_played_home = models.IntegerField(blank=True, null=True)
    pns_played_away = models.IntegerField(blank=True, null=True)
    pns_played_easy = models.IntegerField(blank=True, null=True)
    pns_goal = models.IntegerField(blank=True, null=True)
    pns_winning_goal = models.IntegerField(blank=True, null=True)
    pns_tie_goal = models.IntegerField(blank=True, null=True)
    pns_penalty_scored = models.IntegerField(blank=True, null=True)
    pns_lost_goal = models.IntegerField(blank=True, null=True)
    pns_owngoal = models.IntegerField(blank=True, null=True)
    pns_assist = models.IntegerField(blank=True, null=True)
    pns_assist_kick = models.IntegerField(blank=True, null=True)
    pns_assist_alt = models.IntegerField(blank=True, null=True)
    pns_assist_post = models.IntegerField(blank=True, null=True)
    pns_assist_own_goal = models.IntegerField(blank=True, null=True)
    pns_yellow_card = models.IntegerField(blank=True, null=True, default=0)
    pns_red_card = models.IntegerField(blank=True, null=True)
    pns_penalty_failed = models.IntegerField(blank=True, null=True)
    pns_penalty_saved = models.IntegerField(blank=True, null=True)
    pns_penalty_won = models.IntegerField(blank=True, null=True)
    pns_penalty_conceded = models.IntegerField(blank=True, null=True)
    pns_started = models.IntegerField(blank=True, null=True)
    pns_bench = models.IntegerField(blank=True, null=True)
    pns_sub_in = models.IntegerField(blank=True, null=True)
    pns_sub_out = models.IntegerField(blank=True, null=True)
    pns_minutes = models.IntegerField(blank=True, null=True)
    pns_post_scoring_att = models.IntegerField(blank=True, null=True)
    pns_error_lead_to_goal = models.IntegerField(blank=True, null=True)
    pns_error_lead_to_shot = models.IntegerField(blank=True, null=True)
    pns_turn_id = models.IntegerField(blank=True, null=True)
    pns_notplayed_consecutive = models.IntegerField(blank=True, null=True)
    pns_played_note = models.IntegerField(blank=True, null=True)
    pns_played_win = models.IntegerField(blank=True, null=True)
    pns_note_win = models.FloatField(blank=True, null=True)
    pns_played_draw = models.IntegerField(blank=True, null=True)
    pns_note_draw = models.FloatField(blank=True, null=True)
    pns_played_lose = models.IntegerField(blank=True, null=True)
    pns_note_lose = models.FloatField(blank=True, null=True)
    pns_goal_home = models.IntegerField(blank=True, null=True)
    pns_goal_away = models.IntegerField(blank=True, null=True)
    pns_goal_lose = models.IntegerField(blank=True, null=True)
    pns_goal_subout = models.IntegerField(blank=True, null=True)
    pns_minutes_home = models.IntegerField(blank=True, null=True)
    pns_minutes_away = models.IntegerField(blank=True, null=True)
    pns_minutes_win = models.IntegerField(blank=True, null=True)
    pns_minutes_lose = models.IntegerField(blank=True, null=True)
    pns_subout_80 = models.IntegerField(blank=True, null=True)
    pns_score_easy = models.FloatField(blank=True, null=True)
    pns_score_65 = models.FloatField(blank=True, null=True)
    pns_score_55 = models.FloatField(blank=True, null=True)
    pns_score_home = models.FloatField(blank=True, null=True)
    pns_score_away = models.FloatField(blank=True, null=True)
    pns_score_last5 = models.FloatField(blank=True, null=True)
    pns_score_win = models.FloatField(blank=True, null=True)
    pns_score_lose = models.FloatField(blank=True, null=True)
    pns_score_30 = models.FloatField(blank=True, null=True)
    pns_score_80 = models.FloatField(blank=True, null=True)
    pns_played_score = models.IntegerField(blank=True, null=True)
    pns_played_score_easy = models.IntegerField(blank=True, null=True)
    pns_played_score_home = models.IntegerField(blank=True, null=True)
    pns_played_score_away = models.IntegerField(blank=True, null=True)
    pns_played_score_last5 = models.IntegerField(blank=True, null=True)
    pns_played_score_win = models.IntegerField(blank=True, null=True)
    pns_played_score_lose = models.IntegerField(blank=True, null=True)
    pns_yellow_card_home = models.IntegerField(blank=True, null=True)
    pns_yellow_card_away = models.IntegerField(blank=True, null=True)
    pns_red_card_home = models.IntegerField(blank=True, null=True)
    pns_red_card_away = models.IntegerField(blank=True, null=True)
    pns_assist_home = models.IntegerField(blank=True, null=True)
    pns_assist_away = models.IntegerField(blank=True, null=True)
    pi_overall_index = models.FloatField(blank=True, null=True)
    pi_opponent_index = models.FloatField(blank=True, null=True)
    pi_rating_index = models.FloatField(blank=True, null=True)
    pi_lineup_index = models.FloatField(blank=True, null=True)
    pi_sentiment_index = models.FloatField(blank=True, null=True)
    pi_performance_index = models.FloatField(blank=True, null=True)
    pi_lineup_ratio_index = models.FloatField(blank=True, null=True)
    pi_performance_last5_index = models.FloatField(blank=True, null=True)
    pi_lineup_starting_ratio_index = models.FloatField(blank=True, null=True)
    pi_kapitals_index = models.FloatField(blank=True, null=True)
    pi_squad_ratio_index = models.FloatField(blank=True, null=True)
    pi_marketvar_index = models.FloatField(blank=True, null=True)
    pi_overall_season_index = models.FloatField(blank=True, null=True)
    pi_lineup_season_index = models.FloatField(blank=True, null=True)
    pi_rating_season_index = models.FloatField(blank=True, null=True)
    pi_sentiment_season_index = models.FloatField(blank=True, null=True)
    pi_mod_dif_index = models.FloatField(blank=True, null=True)
    pi_mod_cen_index = models.FloatField(blank=True, null=True)
    pi_mod_att_index = models.FloatField(blank=True, null=True)
    pi_overall_index_dif = models.FloatField(blank=True, null=True)
    pi_overall_index_cen = models.FloatField(blank=True, null=True)
    pi_overall_index_att = models.FloatField(blank=True, null=True)
    pi_overall_season_index_dif = models.FloatField(blank=True, null=True)
    pi_overall_season_index_cen = models.FloatField(blank=True, null=True)
    pi_overall_season_index_att = models.FloatField(blank=True, null=True)
    pi_turn_fantavoto = models.FloatField(blank=True, null=True)
    pi_expected_played = models.IntegerField(blank=True, null=True)
    pi_expected_goal = models.IntegerField(blank=True, null=True)
    pi_expected_penalty = models.IntegerField(blank=True, null=True)
    pi_expected_goal_max = models.IntegerField(blank=True, null=True)
    pi_expected_assist_max = models.IntegerField(blank=True, null=True)
    pi_upcoming_goal_max = models.IntegerField(blank=True, null=True)
    pi_upcoming_assist_max = models.IntegerField(blank=True, null=True)
    pi_upcoming_penalty = models.IntegerField(blank=True, null=True)
    pi_upcoming_played = models.IntegerField(blank=True, null=True)
    pi_current_played = models.IntegerField(blank=True, null=True)
    pi_current_goal = models.IntegerField(blank=True, null=True)
    pi_current_assist = models.IntegerField(blank=True, null=True)
    pi_current_penalty = models.IntegerField(blank=True, null=True)
    pi_projected_played = models.IntegerField(blank=True, null=True)
    pi_projected_goal = models.IntegerField(blank=True, null=True)
    pi_projected_assist = models.IntegerField(blank=True, null=True)
    pi_projected_penalty = models.IntegerField(blank=True, null=True)
    pi_match_played_perc = models.FloatField(blank=True, null=True)
    pi_match_started_perc = models.FloatField(blank=True, null=True)
    pi_fanta_factor = models.FloatField(blank=True, null=True)
    pi_fantasy_rating = models.FloatField(blank=True, null=True)
    pi_vip_bonusmalus = models.FloatField(blank=True, null=True)
    sm_notes = models.IntegerField(blank=True, null=True)
    sm_played = models.IntegerField(blank=True, null=True)
    sm_home_score = models.IntegerField(blank=True, null=True)
    sm_away_score = models.IntegerField(blank=True, null=True)
    sm_match_status = models.CharField(max_length=10, blank=True, null=True)
    sm_match_timer = models.IntegerField(blank=True, null=True)
    sm_realteam_id_home = models.IntegerField(blank=True, null=True)
    sm_realteam_id_away = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fc_player_stats'
        unique_together = (('season_code', 'turn_code_id', 'player_code_id'),)
class FcPlayers(models.Model):
    code_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    birth_date = models.DateField(blank=True, null=True)
    code_role = models.IntegerField(blank=True, null=True)
    main_role = models.CharField(max_length=1, blank=True, null=True)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fc_players'

class FcSeasonMatchPlayers(models.Model):
    season_code = models.ForeignKey('FcSeasons', models.DO_NOTHING, to_field='code_id')
    season_match_code = models.ForeignKey('FcSeasonMatches', models.DO_NOTHING, to_field='code_id')
    player_code_id = models.IntegerField()
    team_code_id = models.IntegerField()
    turn_code_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fc_season_match_players'
        unique_together = (('season_code', 'turn_code_id', 'player_code_id'),)

class FcSeasonMatches(models.Model):
    code_id = models.IntegerField(unique=True)
    turn_code = models.ForeignKey('FcTurns', models.DO_NOTHING, to_field='code_id')
    season_code = models.ForeignKey('FcSeasons', models.DO_NOTHING, to_field='code_id')
    match_date = models.DateTimeField()
    realteam_id_home = models.IntegerField()
    realteam_id_away = models.IntegerField()
    home_score = models.IntegerField(blank=True, null=True)
    away_score = models.IntegerField(blank=True, null=True)
    played = models.IntegerField()
    notes = models.IntegerField()
    match_status = models.CharField(max_length=10)
    match_timer = models.IntegerField()
    match_ht_score = models.CharField(max_length=20)
    match_ft_score = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fc_season_matches'

class FcSeasonTeams(models.Model):
    season_code = models.ForeignKey('FcSeasons', models.DO_NOTHING, to_field='code_id')
    team_code_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'fc_season_teams'
        unique_together = (('season_code', 'team_code_id'),)

class  FcSeasons(models.Model):
    code_id = models.IntegerField(unique=True)
    synced = models.IntegerField()
    season_api = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=191)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    app_bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False 
        db_table = 'fc_seasons'

class FcTeams(models.Model):
    code_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=191)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    app_bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fc_teams'

class FcTurns(models.Model):
    code_id = models.IntegerField(unique=True)
    season_code = models.ForeignKey(FcSeasons, models.DO_NOTHING, to_field='code_id')
    synced = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=191)
    turn_date = models.DateTimeField(blank=True, null=True)
    preview = models.IntegerField()
    finished = models.IntegerField()
    live = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'fc_turns'

class Giocatori(models.Model):
    nome = models.CharField(max_length=255)
    data_nascita = models.DateField()
    ruolo = models.CharField(max_length=1)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    squadra = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'giocatori'

class Calendario(models.Model):
    casa = models.CharField(max_length=255)
    trasferta = models.CharField(max_length=255, blank=True, null=True)
    data_ora = models.DateTimeField(blank=True, null=True)
    gol_casa = models.IntegerField(blank=True, null=True)
    gol_trasferta = models.IntegerField(blank=True, null=True)
    giornata = models.IntegerField()
    stagione = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calendario'

class Infortunati(models.Model):
    id_giocatore = models.IntegerField()
    giornata = models.IntegerField()
    stagione = models.IntegerField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'infortunati'
class Introductions(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    active = models.IntegerField()
    image_url = models.CharField(max_length=999)

    class Meta:
        managed = False
        db_table = 'introductions'
class Newsfeeds(models.Model):
    src_id = models.PositiveIntegerField()
    total_items = models.PositiveIntegerField()
    toadd_posts = models.PositiveIntegerField()
    added_posts = models.PositiveIntegerField()
    toadd_cats = models.PositiveIntegerField()
    added_cats = models.PositiveIntegerField()
    req_type = models.PositiveIntegerField(blank=True, null=True)
    publication_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'newsfeeds'
        unique_together = (('src_id', 'publication_date'),)

class NewsfeedsSrc(models.Model):
    link = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=191)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'newsfeeds_src'

class Offers(models.Model):
    provider_profile = models.ForeignKey('ProviderProfiles', models.DO_NOTHING)
    title = models.CharField(max_length=191)
    about = models.TextField()
    address = models.CharField(max_length=191, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=7)
    latitude = models.DecimalField(max_digits=15, decimal_places=7)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    interested_count = models.IntegerField()
    image_url = models.CharField(max_length=500, blank=True, null=True)
    video = models.CharField(max_length=50, blank=True, null=True)
    featured = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'offers'

class PasswordResets(models.Model):
    email = models.CharField(max_length=191)
    token = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'

class Plans(models.Model):
    name = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    currency = models.CharField(max_length=191)
    duration = models.IntegerField()
    metadata = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans'

class PlansFeatures(models.Model):
    plan_id = models.IntegerField()
    name = models.CharField(max_length=191)
    code = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=7)
    limit = models.IntegerField()
    metadata = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans_features'

class PlansSubscriptions(models.Model):
    plan_id = models.IntegerField()
    model_id = models.IntegerField()
    model_type = models.CharField(max_length=191)
    payment_method = models.CharField(max_length=6, blank=True, null=True)
    is_paid = models.IntegerField()
    charging_price = models.FloatField(blank=True, null=True)
    charging_currency = models.CharField(max_length=191, blank=True, null=True)
    is_recurring = models.IntegerField()
    recurring_each_days = models.IntegerField()
    starts_on = models.DateTimeField(blank=True, null=True)
    expires_on = models.DateTimeField(blank=True, null=True)
    cancelled_on = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans_subscriptions'

class PlansUsages(models.Model):
    subscription_id = models.IntegerField()
    code = models.CharField(max_length=191)
    used = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans_usages'

class Posts(models.Model):
    guid = models.PositiveIntegerField(unique=True, blank=True, null=True)
    provider_profile_id = models.PositiveIntegerField()
    category_id = models.IntegerField()
    title = models.CharField(max_length=191)
    description = models.TextField(blank=True, null=True)
    about = models.TextField()
    address = models.CharField(max_length=191, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    data = models.DateTimeField()
    video = models.CharField(max_length=999)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'posts'

class ProviderProfiles(models.Model):
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    shop_name = models.CharField(max_length=191, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=191, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=7)
    latitude = models.DecimalField(max_digits=15, decimal_places=7)
    opens_at = models.TimeField(blank=True, null=True)
    closes_at = models.TimeField(blank=True, null=True)
    opening_days = models.CharField(max_length=50, blank=True, null=True)
    note = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=7)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    video = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provider_profiles'

class Ratings(models.Model):
    review = models.CharField(max_length=140)
    provider_id = models.PositiveIntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    is_online = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(blank=True, null=True)
    post_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'

class Roles(models.Model):
    name = models.CharField(unique=True, max_length=191)
    weight = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'roles'

class Settings(models.Model):
    key = models.CharField(unique=True, max_length=191)
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'settings'

class SocialAccounts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    provider = models.CharField(max_length=32)
    provider_id = models.CharField(max_length=191)
    token = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'social_accounts'

class Squadre(models.Model):
    title = models.CharField(max_length=191)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    app_bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'squadre'

class Squalificati(models.Model):
    id_giocatore = models.IntegerField()
    giornata = models.IntegerField()
    stagione = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'squalificati'

class Stagioni(models.Model):
    title = models.CharField(max_length=191)
    image_url = models.CharField(max_length=191, blank=True, null=True)
    bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    app_bg_color_rgba = models.CharField(max_length=100, blank=True, null=True)
    season_api = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stagioni'

class StagioniSquadre(models.Model):
    id_stagione = models.IntegerField()
    id_squadra = models.IntegerField()
    turnover = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stagioni_squadre'

class StripeCustomers(models.Model):
    model_id = models.IntegerField()
    model_type = models.CharField(max_length=191)
    customer_id = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stripe_customers'

class Supports(models.Model):
    name = models.CharField(max_length=191)
    email = models.CharField(max_length=191)
    message = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_read = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'supports'

class Tags(models.Model):
    title = models.CharField(max_length=191)
    category = models.ForeignKey(Categories, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags'

class TagsProviderProfiles(models.Model):
    tag_id = models.IntegerField()
    provider_profile_id = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tags_provider_profiles'

class TagsUsers(models.Model):
    tag = models.ForeignKey(Tags, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tags_users'
        unique_together = (('tag', 'user'),)

class TblNotification(models.Model):
    titolo = models.CharField(max_length=300)
    messaggio = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)
    recipients = models.IntegerField()
    users_id_list = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_notification'

class TblPostCover(models.Model):
    event_id = models.IntegerField()
    image_file = models.TextField(db_collation='utf8mb3_general_ci')

    class Meta:
        managed = False
        db_table = 'tbl_post_cover'

class Titolari(models.Model):
    id_match = models.IntegerField()
    id_giocatore = models.IntegerField()
    titolare = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    voto = models.FloatField(blank=True, null=True)
    indice = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'titolari'

class UsersRoles(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_roles'
        unique_together = (('user', 'role'),)


class PostReact(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    post_id = models.IntegerField()
    reaction = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'post_react'


class PrivacyPolicy(models.Model):
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'privacy_policy'


class WelcomeScreen(models.Model):
    heading = models.CharField(max_length=230)
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'welcome_screen'

    
class FantacalcioImages(models.Model):
    heading = models.CharField(max_length=500)
    image_url = models.FileField()

    class Meta:
        managed = False
        db_table = 'fantacalcio_images'