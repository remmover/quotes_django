from django.core.paginator import Paginator
from django.shortcuts import render
from .utils import get_quotes_with_details

# Create your views here.


def main(request, page=1):
    quotes = get_quotes_with_details()
    per_page = 10
    paginator = Paginator(list(quotes), per_page=per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})
