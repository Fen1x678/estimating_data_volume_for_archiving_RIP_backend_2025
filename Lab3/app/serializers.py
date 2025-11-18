from rest_framework import serializers

from .models import *


class AlgorithmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ("id", "name", "status", "ratio", "image")


class AlgorithmSerializer(AlgorithmsSerializer):
    class Meta(AlgorithmsSerializer.Meta):
        fields = "__all__"


class CompressionsSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    moderator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Compression
        fields = "__all__"


class CompressionSerializer(CompressionsSerializer):
    algorithms = serializers.SerializerMethodField()
            
    def get_algorithms(self, compression):
        items = compression.algorithmcompression_set.all()
        return [AlgorithmItemSerializer(item.algorithm, context={"volume": item.volume}).data for item in items]


class AlgorithmItemSerializer(AlgorithmSerializer):
    volume = serializers.SerializerMethodField()

    def get_volume(self, _):
        return self.context.get("volume")

    class Meta:
        model = Algorithm
        fields = ("id", "name", "status", "ratio", "image", "volume")


class AlgorithmCompressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmCompression
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', "is_superuser")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        instance = super().update(instance, validated_data)

        if password and password.strip() and not self.instance.check_password(password):
            instance.set_password(password)
            instance.save()

        return instance