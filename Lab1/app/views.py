from django.shortcuts import render

algorithms_mock = [
    {
        "id": 1,
        "name": "LZW",
        "description": "Алгори́тм Ле́мпеля — Зи́ва — Уэлча (Lempel-Ziv-Welch, LZW) — это универсальный алгоритм сжатия данных без потерь, созданный Авраамом Лемпелем, Яаковом Зивом и Терри Велчем. Он был опубликован Велчем в 1984 году в качестве улучшенной реализации алгоритма LZ78, опубликованного Лемпелем и Зивом в 1978 году.",
        "ratio": 1.51,
        "image": "http://localhost:9000/images/1.png"
    },
    {
        "id": 2,
        "name": "Алгоритм Хаффмана",
        "description": "Алгоритм Хаффмана — это метод оптимального префиксного кодирования данных, который сжимает информацию, присваивая более короткие битовые коды часто встречающимся символам и более длинные — редким",
        "ratio": 2.73,
        "image": "http://localhost:9000/images/2.png"
    },
    {
        "id": 3,
        "name": "RLE",
        "description": "RLE (от англ. Run-Length Encoding, кодирование длин серий) — это простой алгоритм сжатия данных без потерь, который заменяет последовательности (серии) одинаковых данных на пару из самого значения и количества его повторений",
        "ratio": 5.5,
        "image": "http://localhost:9000/images/3.png"
    },
    {
        "id": 4,
        "name": "LZMA",
        "description": "LZMA — алгоритм сжатия данных, разрабатываемый с 1996 или 1998 года Игорем Павловым. Используется в архиваторе 7-Zip того же автора для создания сжатых архивов в формате 7z.",
        "ratio": 7.8,
        "image": "http://localhost:9000/images/4.png"
    },
    {
        "id": 5,
        "name": "JPEG",
        "description": "Алгоритм сжатия JPEG использует дискретное косинусное преобразование (ДКП) для преобразования изображения в частотную область, затем квантование удаляет менее важные детали, и, наконец, применяет вторичное сжатие с потерями или без потерь для получения конечного файла",
        "ratio": 14.3,
        "image": "http://localhost:9000/images/5.png"
    },
    {
        "id": 6,
        "name": "MP3",
        "description": "В формате MP3 используется алгоритм сжатия с потерями, разработанный для существенного уменьшения размера данных, необходимых для воспроизведения записи и обеспечения качества воспроизведения звука, близкого к оригинальному (по мнению большинства слушателей), но с ощутимыми потерями качества при прослушивании на качественной звуковой системе",
        "ratio": 11.1,
        "image": "http://localhost:9000/images/6.png"
    }
]

compressions_mock = [
    {
        "id": 1,
        "status": "Черновик",
        "date_created": "5 сентября 2025г",
        "data_type": "Звук",
        "volume_after": "",
        "algorithms": [
            {
                "id": 1,
                "volume": 2331
            },
            {
                "id": 2,
                "volume": 4123
            },
            {
                "id": 3,
                "volume": 1321
            }
        ]
    },
    {
        "id": 2,
        "status": "В работе",
        "date_created": "3 сентября 2025г",
        "data_type": "Звук",
        "volume_after": 1232,
        "algorithms": [
            {
                "id": 1,
                "volume": 3234
            },
            {
                "id": 3,
                "volume": 2234
            }
        ]
    },
    {
        "id": 3,
        "status": "Завершена",
        "date_created": "27 августа 2025г",
        "data_type": "Графика",
        "volume_after": 64,
        "algorithms": [
            {
                "id": 2,
                "volume": 421
            }
        ]
    }
]


def get_algorithm(algorithm_id):
    for algorithm in algorithms_mock:
        if algorithm["id"] == algorithm_id:
            return algorithm


def get_algorithms():
    return algorithms_mock


def search_algorithms(algorithm_name):
    res = []

    for algorithm in algorithms_mock:
        if algorithm_name.lower() in algorithm["name"].lower():
            res.append(algorithm)

    return res


def get_draft_compression():
    for compression in compressions_mock:
        if compression["status"] == "Черновик":
            return compression


def get_compression(compression_id):
    for compression in compressions_mock:
        if compression["id"] == compression_id:
            return compression


def index(request):
    algorithm_name = request.GET.get("algorithm_name", "")
    algorithms = search_algorithms(algorithm_name) if algorithm_name else get_algorithms()
    draft_compression = get_draft_compression()

    context = {
        "algorithms": algorithms,
        "algorithm_name": algorithm_name,
        "algorithms_count": len(draft_compression["algorithms"]),
        "draft_compression": draft_compression
    }

    return render(request, "algorithms_page.html", context)


def algorithm_page(request, algorithm_id):
    context = {
        "algorithm": get_algorithm(algorithm_id),
    }

    return render(request, "algorithm_page.html", context)


def compression_page(request, compression_id):
    compression = get_compression(compression_id)
    algorithms = [
        {**get_algorithm(algorithm["id"]), "volume": algorithm["volume"]}
        for algorithm in compression["algorithms"]
    ]

    context = {
        "compression": compression,
        "algorithms": algorithms
    }

    return render(request, "compression_page.html", context)
