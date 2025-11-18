from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .calc import calc
from .serializers import *
from .utils import get_draft_compression, get_user, get_moderator, identity_user


@api_view(["GET"])
def search_algorithms(request):
    algorithm_name = request.GET.get("algorithm_name", "")

    algorithms = Algorithm.objects.filter(status=1)
    if algorithm_name:
        algorithms = algorithms.filter(name__icontains=algorithm_name)

    serializer = AlgorithmsSerializer(algorithms, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_algorithm_by_id(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    algorithm = Algorithm.objects.get(pk=algorithm_id)
    serializer = AlgorithmSerializer(algorithm)

    return Response(serializer.data)


@api_view(["PUT"])
def update_algorithm(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    algorithm = Algorithm.objects.get(pk=algorithm_id)

    serializer = AlgorithmSerializer(algorithm, data=request.data, partial=True)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_algorithm(request):
    serializer = AlgorithmSerializer(data=request.data, partial=False)

    serializer.is_valid(raise_exception=True)

    Algorithm.objects.create(**serializer.validated_data)

    algorithms = Algorithm.objects.filter(status=1)
    serializer = AlgorithmSerializer(algorithms, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_algorithm(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    algorithm = Algorithm.objects.get(pk=algorithm_id)
    algorithm.status = 2
    algorithm.save()

    algorithms = Algorithm.objects.filter(status=1)
    serializer = AlgorithmSerializer(algorithms, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_algorithm_to_compression(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    algorithm = Algorithm.objects.get(pk=algorithm_id)

    draft_compression = get_draft_compression()

    if draft_compression is None:
        draft_compression = Compression.objects.create()
        draft_compression.owner = get_user()
        draft_compression.save()

    if AlgorithmCompression.objects.filter(compression=draft_compression, algorithm=algorithm).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = AlgorithmCompression.objects.create(
        compression=draft_compression,
        algorithm=algorithm
    )
    item.save()

    serializer = CompressionSerializer(draft_compression)
    return Response(serializer.data["algorithms"])


@api_view(["POST"])
def update_algorithm_image(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    algorithm = Algorithm.objects.get(pk=algorithm_id)

    image = request.data.get("image")
    if image is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    algorithm.image = image
    algorithm.save()

    serializer = AlgorithmSerializer(algorithm)
    return Response(serializer.data)


@api_view(["GET"])
def search_compressions(request):
    status = int(request.GET.get("status", 0))
    date_formation_start = request.GET.get("date_formation_start")
    date_formation_end = request.GET.get("date_formation_end")

    compressions = Compression.objects.exclude(status__in=[1, 5])

    if status > 0:
        compressions = compressions.filter(status=status)

    if date_formation_start and parse_datetime(date_formation_start):
        compressions = compressions.filter(date_formation__gt=parse_datetime(date_formation_start) - timedelta(days=1))

    if date_formation_end and parse_datetime(date_formation_end):
        compressions = compressions.filter(date_formation__lt=parse_datetime(date_formation_end) + timedelta(days=1))

    serializer = CompressionsSerializer(compressions, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_cart_info(request):
    resp = {
        "algorithms_count": 0,
        "draft_compression": 0
    }

    draft_compression = get_draft_compression()
    if draft_compression:
        algorithms = AlgorithmCompression.objects.filter(compression=draft_compression)
        resp = {
            "algorithms_count": algorithms.count(),
            "draft_compression": draft_compression.pk
        }

    return Response(resp)


@api_view(["GET"])
def get_compression_by_id(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    compression = Compression.objects.get(pk=compression_id)
    serializer = CompressionSerializer(compression, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_compression(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    compression = Compression.objects.get(pk=compression_id)
    serializer = CompressionSerializer(compression, data=request.data, partial=True)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return Response({
            "error": "сжатие не найден"
        }, status=status.HTTP_404_NOT_FOUND)

    compression = Compression.objects.get(pk=compression_id)

    if compression.status != 1:
        return Response({
            "error": "сжатие не в том статусе"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if not compression.data_type:
        return Response({
            "error": "поле data_type не заполнено"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    compression.status = 2
    compression.date_formation = timezone.now()
    compression.save()

    serializer = CompressionSerializer(compression)
    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])
    if request_status not in [3, 4]:
        return Response({
            "error": "некорректный status"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    compression = Compression.objects.get(pk=compression_id)

    if compression.status != 2:
        return Response({
            "error": "сжатие не в том статусе"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if request_status == 3:
        serializer = CompressionSerializer(compression)
        compression.volume_after = calc(serializer.data)

    compression.date_complete = timezone.now()
    compression.status = request_status
    compression.moderator = get_moderator()
    compression.save()

    serializer = CompressionSerializer(compression)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_compression(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    compression = Compression.objects.get(pk=compression_id)

    if compression.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    compression.status = 5
    compression.save()

    serializer = CompressionSerializer(compression, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_algorithm_from_compression(request, compression_id, algorithm_id):
    if not AlgorithmCompression.objects.filter(compression_id=compression_id, algorithm_id=algorithm_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = AlgorithmCompression.objects.get(compression_id=compression_id, algorithm_id=algorithm_id)
    item.delete()

    items = AlgorithmCompression.objects.filter(compression_id=compression_id)
    data = [AlgorithmItemSerializer(item.algorithm, context={"volume": item.volume}).data for item in items]

    return Response(data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_algorithm_in_compression(request, compression_id, algorithm_id):
    if not AlgorithmCompression.objects.filter(algorithm_id=algorithm_id, compression_id=compression_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    compression = Compression.objects.get(pk=compression_id)
    if compression.status != 1:
        return Response({
            "error": "Некорректный статус сжатия"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    item = AlgorithmCompression.objects.get(algorithm_id=algorithm_id, compression_id=compression_id)

    serializer = AlgorithmCompressionSerializer(item, data=request.data, partial=True)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.data)
    if user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout(request):
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def user_info(request):
    user = identity_user(request)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_user(request):
    user = identity_user(request)

    serializer = UserUpdateProfileSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)