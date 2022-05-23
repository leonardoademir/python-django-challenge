from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import validators
import random, string
import datetime
from .models import Url, Click
from django_user_agents.utils import get_user_agent


def index(request):
    urls = Url.objects.order_by('-created_at')
    
    nxt_mnth = datetime.datetime.today().replace(day=28) + datetime.timedelta(days=4)
    last_day = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    first_day = datetime.datetime.today().replace(day=1)

    for url in urls:
        clicks = Click.objects.filter(created_at__gte=first_day).filter(created_at__lte=last_day).filter(url=url)

        url.month_clicks = clicks.count()

        #platforms
        url.windows_clicks = clicks.filter(platform='Windows').count()
        url.linux_clicks = clicks.filter(platform='Linux').count()
        url.mac_clicks = clicks.filter(platform='Mac').count()

        #browsers
        url.chrome_clicks = clicks.filter(browser='Chrome').count()
        url.firefox_clicks = clicks.filter(browser='Firefox').count()
        url.opera_clicks = clicks.filter(browser='Opera').count()

    context = {'urls': urls}
    return render(request, 'heyurl/index.html', context)

def store(request):
    original_url = request.POST['original_url']
    if not validators.url(original_url):
        return HttpResponseNotFound("This is not a valid URL.")

    short_url = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(1,5)))

    url = Url(short_url=short_url, original_url=original_url, clicks=0, created_at=datetime.date.today(), updated_at=datetime.date.today())
    url.save()

    return HttpResponse("Storing a new URL object into storage")

def short_url(request, short_url):
    platform = get_user_agent(request).os.family
    browser = get_user_agent(request).browser.family

    url = Url.objects.filter(short_url=short_url)

    if (not url):
        return HttpResponseNotFound("This short URL does not exists.")
    
    url = url.get()
    url.clicks = url.clicks + 1
    url.updated_at = datetime.date.today()
    url.save()

    click = Click(url=url, browser=browser, platform=platform, created_at=datetime.date.today(), updated_at=datetime.date.today())
    click.save()
    return HttpResponseRedirect(url.original_url)
