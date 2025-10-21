from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect

from app.models import Algorithm, Compression, AlgorithmCompression


def index(request):
    algorithm_name = request.GET.get("algorithm_name", "")
    algorithms = Algorithm.objects.filter(status=1)

    if algorithm_name:
        algorithms = algorithms.filter(name__icontains=algorithm_name)

    context = {
        "algorithm_name": algorithm_name,
        "algorithms": algorithms
    }

    draft_compression = get_draft_compression()
    if draft_compression:
        context["algorithms_count"] = len(draft_compression.algorithmcompression_set.all())
        context["draft_compression"] = draft_compression

    return render(request, "algorithms_page.html", context)


def algorithm_page(request, algorithm_id):
    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return redirect("/")

    context = {
        "algorithm": Algorithm.objects.get(id=algorithm_id)
    }

    return render(request, "algorithm_page.html", context)


def compression_page(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return redirect("/")

    compression = Compression.objects.get(id=compression_id)
    if compression.status == 5:
        return render(request, "compression_removed.html")

    context = {
        "compression": compression,
        "items": compression.algorithmcompression_set.all()
    }

    return render(request, "compression_page.html", context)


def add_algorithm_to_draft_compression(request, algorithm_id):
    algorithm_name = request.POST.get("algorithm_name")
    redirect_url = f"/?algorithm_name={algorithm_name}" if algorithm_name else "/"

    if not Algorithm.objects.filter(pk=algorithm_id).exists():
        return redirect(redirect_url)

    draft_compression = get_draft_compression()
    if draft_compression is None:
        draft_compression = Compression.objects.create()
        draft_compression.owner = get_current_user()
        draft_compression.save()

    algorithm = Algorithm.objects.get(pk=algorithm_id)
    if AlgorithmCompression.objects.filter(compression=draft_compression, algorithm=algorithm).exists():
        return redirect(redirect_url)

    item = AlgorithmCompression(
        compression=draft_compression,
        algorithm=algorithm
    )
    item.save()

    return redirect(redirect_url)


def delete_compression(request, compression_id):
    if not Compression.objects.filter(pk=compression_id).exists():
        return redirect("/")

    with connection.cursor() as cursor:
        cursor.execute("UPDATE compressions SET status=5 WHERE id = %s", [compression_id])

    return redirect("/")


def get_draft_compression():
    return Compression.objects.filter(status=1).first()


def get_current_user():
    return User.objects.filter(is_superuser=False).first()
