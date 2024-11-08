from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from .models import MatchHistory
from .models import UserProfile
from .models import Friend
from .models import Tournament
from .models import MatchHistory2v2
from .models import CowboyMatchHistory


from .web3 import get_tournament_data, add_tournament_data


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=False)
	old_password = serializers.CharField(write_only=True, required=True)
	class Meta:
		model = User
		fields = [
			'id',
			'username',
			'email',
			'password',
			'old_password',
			'first_name',
			'last_name',
			'is_active',
		]

	def validate(self, data):
		user = self.instance

		if 'email' in data:
			email = data.get('email')
			if email is None or email.strip() == "":
				raise serializers.ValidationError({"email": "Email cannot be empty"})
			try:
				validate_email(email)
			except ValidationError:
				raise serializers.ValidationError({"email": "Invalid email address"})
			if user and user.email == email:
				raise serializers.ValidationError({"email": "New email cannot be the same as the old email"})

		if 'old_password' in data:
			old_password = data.get('old_password')
			if old_password is None:
				raise serializers.ValidationError({"old_password": "You need to validate old password"})
			if user and not user.check_password(old_password):
				raise serializers.ValidationError({"old_password": "Old password is incorrect"})

		if 'password' in data:
			password = data.get('password')
			if password is None:
				raise serializers.ValidationError({"password": "Password cannot be empty"})
			if len(password) < 8:
				raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})
			if not any(char.isdigit() for char in password):
				raise serializers.ValidationError({"password": "Password must contain at least one digit"})
			if not any(char.isalpha() for char in password):
				raise serializers.ValidationError({"password": "Password must contain at least one letter"})
			if user and user.check_password(password):
				raise serializers.ValidationError({"password": "New password cannot be the same as the old password"})

		return data

	def create(self, validate_data):
		password = validate_data.pop('password')
		user = User(**validate_data)
		user.set_password(password)
		user.save()

		return user
	
	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)

		for attr, value in validated_data.items():
			setattr(instance, attr, value)

		if password:
			instance.set_password(password)

		instance.save()
		return instance


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	wins = serializers.SerializerMethodField()
	losses = serializers.SerializerMethodField()
	cowboy_wins = serializers.SerializerMethodField()
	cowboy_losses = serializers.SerializerMethodField()
	avatar = serializers.ImageField(required=False)

	class Meta:
		model = UserProfile
		fields = [
			'user',
			# 'oauth',
			'wins',
			'losses',
			'cowboy_wins',
			'cowboy_losses',
			'match_history',
			'avatar',
			'is_online',
		]

	def get_wins(self, obj):
		return obj.calculate_wins()
	
	def get_losses(self, obj):
		return obj.calculate_losses()
	
	def get_cowboy_wins(self, obj):
		return obj.calculate_cowboy_wins()
	
	def get_cowboy_losses(self, obj):
		return obj.calculate_cowboy_losses()
	
	def validate_avatar(self, value):
		max_size = 2 * 1024 * 1024
		valid_content_types = ['image/jpeg', 'image/png']

		if value.size > max_size:
			raise ValidationError("Avatar image size should not exceed 2 MB.")

		if value.content_type not in valid_content_types:
			raise ValidationError("Avatar image must be in JPEG or PNG format.")

		return value
	
	def update(self, instance, validated_data):
		user_data = validated_data.pop('user', None)
		avatar = validated_data.pop('avatar', None)

		super().update(instance, validated_data)

		if user_data:
			user = instance.user
			user_serializer = UserSerializer(instance=user, data=user_data, partial=True)
			if user_serializer.is_valid(raise_exception=True):
				user_serializer.save()

		if avatar:
			instance.avatar = avatar
			instance.save()

		return instance

class MatchHistorySerializer(serializers.ModelSerializer):
	player1_username = serializers.SerializerMethodField()
	class Meta:
		model = MatchHistory
		fields = [
			'player1',
			'player2',
			'player1_username',
			'winner',
			'match_date',
			'match_score'
		]
		read_only_fields = ['winner']

	def get_player1_username(self, obj):
		return obj.player1.username

	def validate_match_score(self, value):
		try:
			player1_score, player2_score = map(int, value.strip().split('-'))
			if player1_score < 0 or player2_score < 0:
				raise serializers.ValidationError("Scores must be non-negative integers.")
		except ValueError:
			raise serializers.ValidationError("Match score must be in the format 'int-int' (e.g., '10-5').")
		return value
	
	def validate(self, data):
		# Ensure player1 and player2 are not the same user
		if data['player1'] == data['player2']:
			raise serializers.ValidationError("A player cannot play against themselves.")
		return data
	

class MatchHistory2v2Serializer(serializers.ModelSerializer):
	player1_username = serializers.SerializerMethodField()
	class Meta:
		model = MatchHistory2v2
		fields = [
			'player1',
			'player2',
			'player3',
			'player4',
			'player1_username',
			'winner1',
			'winner2',
			'match_date',
			'match_score'
		]
		read_only_fields = ['winner1', 'winner2']

	def get_player1_username(self, obj):
		return obj.player1.username

	def validate_match_score(self, value):
		try:
			team1_score, team2_score = map(int, value.strip().split('-'))
			if team1_score < 0 or team2_score < 0:
				raise serializers.ValidationError("Scores must be non-negative integers.")
		except ValueError:
			raise serializers.ValidationError("Match score must be in the format 'int-int' (e.g., '10-5').")
		return value
	
	def validate(self, data):
		players = [data.get('player1'), data.get('player2'), data.get('player3'), data.get('player4')]
		if len(players) != len(set(players)):
			raise serializers.ValidationError("All players must be unique.")
		return data
	

class CowboyMatchHistorySerializer(serializers.ModelSerializer):
	player1_username = serializers.SerializerMethodField()
	class Meta:
		model = CowboyMatchHistory
		fields = [
			'player1',
			'player2',
			'player1_username',
			'winner',
			'match_date',
			'match_score'
		]
		read_only_fields = ['winner']

	def get_player1_username(self, obj):
		return obj.player1.username

	def validate_match_score(self, value):
		try:
			player1_score, player2_score = map(int, value.strip().split('-'))
			if player1_score < 0 or player2_score < 0:
				raise serializers.ValidationError("Scores must be non-negative integers.")
		except ValueError:
			raise serializers.ValidationError("Match score must be in the format 'int-int' (e.g., '10-5').")
		return value
	
	def validate(self, data):
		if data['player1'] == data['player2']:
			raise serializers.ValidationError("A player cannot play against themselves.")
		return data


class IsOnlineField(serializers.Field):
    def get_attribute(self, instance):
        user = super().get_attribute(instance)
        return user

    def to_representation(self, user):
        if user is None:
            return False
        try:
            profile = UserProfile.objects.get(user=user)
            return profile.is_online
        except UserProfile.DoesNotExist:
            return False


class FriendSerializer(serializers.ModelSerializer):
	friend_username = serializers.CharField(write_only=True, required=False)
	friend_detail = UserSerializer(source='friend', read_only=True)
	user_detail = UserSerializer(source='user', read_only=True)
	is_friend_online = IsOnlineField(source='friend', read_only=True)
	is_user_online = IsOnlineField(source='user', read_only=True)

	class Meta:
		model = Friend
		fields = [
			'id',
			'user',
			'friend',
			'friend_username',
			'friend_detail',
			'is_friend_online',
			'user_detail',
			'is_user_online',
			'status',
			'created_at'
		]
		read_only_fields = ['id', 'user', 'user_detail', 'friend', 'friend_detail', 'created_at']

	def validate(self, data):
		user = self.context['request'].user
		friend_username = data.get('friend_username')

		if self.context['request'].method == 'POST':
			if not friend_username:
				raise serializers.ValidationError("Friend username is required.")

			try:
				friend = User.objects.get(username=friend_username)
			except User.DoesNotExist:
				raise serializers.ValidationError("Friend with this username does not exist.")

			if user == friend:
				raise serializers.ValidationError("You cannot send a friend request to yourself.")

			if Friend.objects.filter(user=user, friend=friend).exists() or Friend.objects.filter(user=friend, friend=user).exists():
				raise serializers.ValidationError("A friend request already exists between these users.")

			data['friend_instance'] = friend

		return data

	def create(self, validated_data):
		user = self.context['request'].user
		friend = validated_data.pop('friend_instance')  # Retrieve the friend instance

		friend_request = Friend.objects.create(
			user=user,
			friend=friend,
			status='pending'
		)
		return friend_request


class TournamentSerializer(serializers.ModelSerializer):
    winners_order = serializers.ListField(child=serializers.CharField(), write_only=True)
    winners_order_display = serializers.SerializerMethodField()

    class Meta:
        model = Tournament
        fields = [
            'owner',
            'tournament_id',
            'match_date',
            'winners_order',
            'winners_order_display',
            'blockchain_tx_hash',
        ]
        read_only_fields = ['blockchain_tx_hash', 'winners_order_display']

    def get_winners_order_display(self, obj):
        try:
            blockchain_data = get_tournament_data(obj.tournament_id)
            print("Blockchain data:", blockchain_data)
            return blockchain_data
        except Exception as e:
            return {'error': str(e)}

    def create(self, validated_data):
        winners_order = validated_data.pop('winners_order', None)
        try:
            tournament = Tournament.objects.create(**validated_data)

            if winners_order:
                tournament_id = tournament.id + 60055
                tournament.tournament_id = tournament_id
                tx_hash = add_tournament_data(tournament_id, winners_order, settings.METAMASK_PRIVATE_KEY)
                tournament.blockchain_tx_hash = tx_hash
                tournament.save()

            return tournament
        except Exception as e:
            raise serializers.ValidationError(f"Error creating tournament: {e}")
	

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
	def validate(self, attrs):
		request = self.context.get('request')
		refresh_token = request.COOKIES.get('refresh_token')

		if not refresh_token:
			raise serializers.ValidationError({'detail': 'Refresh token not found in cookies'})

		attrs['refresh'] = refresh_token
		return super().validate(attrs)