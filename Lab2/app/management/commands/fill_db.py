from django.core.management.base import BaseCommand

from app.calc import calc
from app.models import *
from app.utils import *


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}",
                                      last_name=f"user{i}")


def add_algorithms():
    Algorithm.objects.create(
        name="LZW",
        description="Алгори́тм Ле́мпеля — Зи́ва — Уэлча (Lempel-Ziv-Welch, LZW) — это универсальный алгоритм сжатия данных без потерь, созданный Авраамом Лемпелем, Яаковом Зивом и Терри Велчем. Он был опубликован Велчем в 1984 году в качестве улучшенной реализации алгоритма LZ78, опубликованного Лемпелем и Зивом в 1978 году.",
        ratio=1.51,
        image="1.png"
    )

    Algorithm.objects.create(
        name="Алгоритм Хаффмана",
        description="Алгоритм Хаффмана — это метод оптимального префиксного кодирования данных, который сжимает информацию, присваивая более короткие битовые коды часто встречающимся символам и более длинные — редким",
        ratio=2.73,
        image="2.png"
    )

    Algorithm.objects.create(
        name="RLE",
        description="RLE (от англ. Run-Length Encoding, кодирование длин серий) — это простой алгоритм сжатия данных без потерь, который заменяет последовательности (серии) одинаковых данных на пару из самого значения и количества его повторений",
        ratio=5.5,
        image="3.png"
    )

    Algorithm.objects.create(
        name="LZMA",
        description="LZMA — алгоритм сжатия данных, разрабатываемый с 1996 или 1998 года Игорем Павловым. Используется в архиваторе 7-Zip того же автора для создания сжатых архивов в формате 7z.",
        ratio=7.8,
        image="4.png"
    )

    Algorithm.objects.create(
        name="JPEG",
        description="Алгоритм сжатия JPEG использует дискретное косинусное преобразование (ДКП) для преобразования изображения в частотную область, затем квантование удаляет менее важные детали, и, наконец, применяет вторичное сжатие с потерями или без потерь для получения конечного файла",
        ratio=14.3,
        image="5.png"
    )

    Algorithm.objects.create(
        name="MP3",
        description="В формате MP3 используется алгоритм сжатия с потерями, разработанный для существенного уменьшения размера данных, необходимых для воспроизведения записи и обеспечения качества воспроизведения звука, близкого к оригинальному (по мнению большинства слушателей), но с ощутимыми потерями качества при прослушивании на качественной звуковой системе",
        ratio=11.1,
        image="6.png"
    )


def add_compressions():
    users = User.objects.filter(is_staff=False)
    moderators = User.objects.filter(is_staff=True)
    algorithms = Algorithm.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        owner = random.choice(users)
        add_compression(status, algorithms, owner, moderators)

    add_compression(1, algorithms, users[0], moderators)
    add_compression(2, algorithms, users[0], moderators)


def add_compression(status, algorithms, owner, moderators):
    compression = Compression.objects.create()
    compression.status = status

    if status in [3, 4]:
        compression.moderator = random.choice(moderators)
        compression.date_complete = random_date()

        compression.date_formation = compression.date_complete - random_timedelta()
        compression.date_created = compression.date_formation - random_timedelta()
    else:
        compression.date_formation = random_date()
        compression.date_created = compression.date_formation - random_timedelta()

    compression.data_type = random.choice(["Графика", "Звук", "Видео"])

    compression.owner = owner

    for algorithm in random.sample(list(algorithms), 3):
        item = AlgorithmCompression(
            compression=compression,
            algorithm=algorithm,
            volume=random.randint(10, 10000)
        )
        item.save()

    if status == 3:
        compression.volume_after = calc(compression.algorithmcompression_set.all())

    compression.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_algorithms()
        add_compressions()
        print("База данных заполнена")
