import json
import requests
import mandrill
import hashlib

from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from social.apps.django_app.default.models import UserSocialAuth

from .models import Item, Nest, Request, CraigPost, Message, Profile
from .forms import ItemForm
from .scrape import scrape_craigslist

# from .delivery import postmate, Location, DeliveryQuote
from . import delivery

def update_nest_status(user):
    nest = Nest.objects.filter(user=user).first()
    if nest is None:
        return False, 'home'

    response = requests.get('https://developer-api.nest.com/structures?auth={0}'.format(nest.access_token))
    data = response.json()
    nest.home = data[data.keys()[0]]['away']
    nest.save()
    return True, nest.home


@csrf_exempt
def home(request):
    if request.user.is_authenticated():
        return redirect('/search')

    if 'mandrill_events' in request.POST:

        msg = json.loads(request.POST.get('mandrill_events'))[0]

        msg_text = msg['msg']['text']
        from_email = msg['msg']['from_email']

        post = CraigPost.objects.filter(email=from_email).all()[0]

        the_msg = Message(text=msg_text, from_us=False)
        the_msg.post = post
        the_msg.save()

    return render(request, 'home.html', None)


@login_required
def me(request):
    data = {
        'items': Item.objects.filter(owner=request.user).order_by('possessor'),
        'success': 'success' in request.GET,
    }

    profile = Profile.objects.filter(user=request.user).first()
    if profile is None:
        return redirect("/address")

    if 'topup' in request.GET:
        profile.balance += int(request.GET.get('topup'))
        profile.save()

    # social = request.user.social_auth.get(provider='facebook')
    # response = requests.get(
    #     'https://graph.facebook.com/me',
    #     params={'access_token': social.extra_data['access_token']}
    # )
    # print response.json()

    print

    return render(request, 'me.html', data)


@login_required
def new_item(request):
    i = ItemForm(request.POST, request.FILES)
    if i.is_valid():
        new_item = i.save(commit=False)
        new_item.owner = new_item.possessor = request.user
        new_item.save()
        return redirect('/me?success')
    return redirect('/me?fail')


@login_required
def nest(request):
    print request.GET

    if request.GET.get('state') == "STATE" and 'code' in request.GET:
        nest, created = Nest.objects.get_or_create(user=request.user)
        nest.code = request.GET.get('code')

        response = requests.post('https://api.home.nest.com/oauth2/access_token?client_id=6ccafabb-4945-4590-9fa9-b8f7e2b5d613&code={0}&client_secret=5bHqEETnOkuNIsFKLSe5oDwe3&grant_type=authorization_code'.format(nest.code))

        data = response.json()
        nest.access_token = data['access_token']
        nest.save()

        return redirect('/')
    else:
        return redirect('https://home.nest.com/login/oauth2?client_id=6ccafabb-4945-4590-9fa9-b8f7e2b5d613&state=STATE')


@login_required
def search(request):
    data = {
        'requested': request.GET.get('requested'),
    }

    friend_uids = cache.get('friend_uids_{0}'.format(request.user.id))
    if not friend_uids:
        social = request.user.social_auth.filter(provider='facebook').first()
        response = requests.get(
            'https://graph.facebook.com/{0}/friends'.format(social.uid),
            params={'access_token': social.extra_data['access_token'], 'fields': 'id,name,picture', 'limit': '5000'}
            )

        friends = response.json()
        friend_uids = map(lambda x: int(x['id']), friends['data'])
        cache.set('friend_uids_{0}'.format(request.user.id), friend_uids, 60*60)


    data['friend_social'] = UserSocialAuth.objects.filter(uid__in=friend_uids).select_related('user')
    data['friends'] = map(lambda x: x.user, data['friend_social'])

    data['items'] = Item.objects.filter(owner__in=data['friends'], owner=F('possessor'))

    return render(request, 'search.html', data)


@login_required
def request_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    data = {
        'item': item
    }

    quote = delivery.api.post_delivery_quote(item.owner.profile.get().address, request.user.profile.get().address)
    print quote
    data['delivery_quote'] = quote['fee'] / 100
    data['quote'] = quote

    return render(request, 'request.html', data)


@login_required
def request_item_confirm(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    data = {
        'item': item
    }

    req = Request(requestor=request.user, item=item)
    req.save()

    message = '''
Hello!

You have a new request for "{0}"! Please approve it at http://reciproxity.me/requests

Thanks!
Reciproxity
'''.format(item.name)


    send_mail("New Reciproxity Request", message,
    "{0} {1} <hello@reciproxity.me>".format(request.user.first_name, request.user.last_name), [item.owner.email])

    return redirect('/search?requested=' + item_id)

@login_required
def address(request):
    data = {}
    if 'address' in request.POST and 'phone_number' in request.POST:
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.address = request.POST.get('address')
        profile.phone_number = request.POST.get('phone_number')
        profile.save()
        return redirect('/me')

    return render(request, 'address.html', data)

@login_required
def borrowed(request):
    data = {}

    data['borrowed'] = Item.objects.filter(~Q(owner=F('possessor')), possessor=request.user)
    data['requests'] = Request.objects.filter(requestor=request.user, completed=False)

    data['owed'] = sum(map(lambda x: x.requests.order_by('-id').first().cost_delivery, data['borrowed'])) / 100.

    data['owed_full'] = data['owed'] * 100

    return render(request, 'borrowed.html', data)

@login_required
def return_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    req = Request(requestor=item.owner, accepted=True, item=item)
    req.save()

    return redirect("/requests")

@login_required
def list_requests(request):
    data = {'accepted': 'accepted' in request.GET}

    data['requests'] = Request.objects.filter(item__possessor=request.user, completed=False).order_by('accepted')
    data['outstanding'] = Item.objects.filter(~Q(owner=F('possessor')), owner=request.user) #Request.objects.filter(item__owner=request.user, completed=True)



    return render(request, 'requests.html', data)


@login_required
def accept_request(request, req_id):
    req = get_object_or_404(Request, id=req_id, item__owner=request.user)
    req.accepted = True
    req.save()
    return redirect('/requests?accepted')


def backlog(request):
    pending_requests = Request.objects.filter(accepted=True, in_progress=False, completed=False)

    data = {
        'pending_requests': str(pending_requests)
    }

    all_users = set()
    for req in pending_requests:
        all_users.add(req.requestor)
        if req.item:
            all_users.add(req.item.possessor)
    data['users'] = map(str, all_users)
    all_user_presence = dict()

    for user in all_users:
        connected_account, status = update_nest_status(user)
        all_user_presence[user] = status
    data['all_user_presence'] = str(all_user_presence)

    for req in pending_requests:
        if (not req.item and all_user_presence[req.requestor] == 'home') or all_user_presence[req.requestor] == all_user_presence[req.item.possessor] == 'home':
            pickup = None
            if req.item:
                pickup = delivery.Location('{0} {1}'.format(req.item.possessor.first_name, req.item.possessor.last_name),
                                     req.item.possessor.profile.get().address,
                                     req.item.possessor.profile.get().phone_number)
            else:
                pickup = delivery.Location('Craigslist User',
                                     req.address,
                                     '1 212 555 5555')
            dropoff = delivery.Location('{0} {1}'.format(req.requestor.first_name, req.requestor.last_name),
                                 req.requestor.profile.get().address,
                                 req.requestor.profile.get().phone_number)

            if req.item:
                manifest = '{0}'.format(req.item.name)
            else:
                manifest = 'verify item - ' + req.craig.title
            de = delivery.Delivery(delivery.api, manifest, pickup, dropoff)
            de.create()
            print de
            req.pickup_estimate = de.pickup_eta
            req.delivery_estimate = de.dropoff_eta
            req.delivery_id = de.delivery_id
            req.in_progress = True
            req.cost_delivery = de.fee
            req.save()

    in_progress = Request.objects.filter(accepted=True, in_progress=True, completed=False)
    data['in_progress'] = map(str, in_progress)
    for req in in_progress:
        print req
        del_data = delivery.api.get_delivery_data(req.delivery_id)
        req.pickup_estimate = del_data.get('pickup_eta')
        req.delivery_estimate = del_data.get('dropoff_eta')
        if del_data.get('status') == 'delivered':
            req.completed = True
            from decimal import Decimal
            paid = False
            if req.item:
                before_p = req.item.possessor
                req.item.possessor = req.requestor
                if req.item.possessor == req.item.owner:
                    profile = Profile.objects.filter(user=before_p).first()
                    profile.balance -= Decimal(req.cost_delivery) / Decimal(100)
                    profile.save()
                    paid = True

            if not paid:
                profile = Profile.objects.filter(user=req.requestor).first()
                profile.balance -= Decimal(req.cost_delivery) / Decimal(100)
                profile.save()

        req.save()
        if req.item:
            req.item.save()

    return HttpResponse(json.dumps(data), content_type="application/json")

def craigslist(request):
    data = {
        'posts': CraigPost.objects.filter(user=request.user).order_by('-id')
    }

    return render(request, 'craigslist.html', data)

def cragslist_submit(request):
    print request.POST
    if 'url' not in request.POST or 'email_body' not in request.POST:
        return redirect('/craigslist')

    craig_url = request.POST.get('url')
    craig_email = request.POST.get('email_body')

    email_addr, craig_title = scrape_craigslist(craig_url)

    email_addr = 'rohun@rohunbansal.com'

    post = CraigPost(url=craig_url, title=craig_title, email=email_addr, user=request.user)
    post.save()
    msg = Message(post=post, text=craig_email, from_us=True)
    msg.save()

    send_mail("Replying to your Craigslist post", craig_email,
    "{0} <hello@reciproxity.me>".format(request.user.first_name), [email_addr])

    return redirect('/craigslist')


def craigslist_reply(request, req_id):
    post = get_object_or_404(CraigPost, id=req_id, user=request.user)
    if 'email_body' not in request.POST:
        return redirect('/craigslist')

    message = request.POST.get('email_body')
    if 'send_link' in request.POST and request.POST.get('send_link') == 'on' and 'price' in request.POST:
        hash_ver = hashlib.sha256("reciproxity{0}{1}".format(post.id, post.title)).hexdigest()
        url = 'http://reciproxity.me/accept/{0}/{1}'.format(post.id, hash_ver)

        message += '''

        To confirm this purchase for ${0}, please go to {1} and enter your address (this will not be availalbe to the reciproxity user to protect your privacy) and a messager will be sent to you to pick up the item. You can select the method of payment at the link.

        '''.format(request.POST.get('price'), url)
        post.price = int(request.POST.get('price'))
        profile = Profile.objects.filter(user=request.user).first()
        profile.balance -= post.price
        profile.save()
        post.save()

    msg = Message(post=post, text=message, from_us=True)
    msg.save()

    send_mail("Re: Replying to your Craigslist post", msg.text,
    "{0} <hello@reciproxity.me>".format(request.user.first_name), [post.email])

    return redirect("/craigslist")


def craigslist_accept(request, req_id, hash):
    post = get_object_or_404(CraigPost, id=req_id)
    data = {'post': post, 'hash': hash}

    hash_ver = hashlib.sha256("reciproxity{0}{1}".format(post.id, post.title)).hexdigest()

    if hash != hash_ver:
        return redirect('/')

    return render(request, 'accept.html', data)


def craigslist_accept_done(request, req_id, hash):
    post = get_object_or_404(CraigPost, id=req_id)
    data = {'post': post, 'hash': hash}

    hash_ver = hashlib.sha256("reciproxity{0}{1}".format(post.id, post.title)).hexdigest()

    if hash != hash_ver:
        return redirect('/')

    if not 'address' in request.POST:
        return redirect('/accept/{{0}}/{{1}}/done'.format(post.id, hash))

    address = request.POST.get('address')

    req = Request(requestor=request.user, craig=post, accepted=True, address=address)
    req.save()


    return render(request, 'accept_done.html', data)


def balance(request):
    data = {}
    return render(request, 'balance.html', data)
