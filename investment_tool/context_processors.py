from .forms import SearchForm


def my_cp(request):
    search = SearchForm()
    ctx = {
        'search': search
           }
    return ctx
