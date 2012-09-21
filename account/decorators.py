from django.http import HttpResponseRedirect
from account.models import Account
from django.core.urlresolvers import reverse

def referee_required(view_func):
    def new(request, *args, **kwargs):
        u = request.user
        try:
            a = u.account
        except:
            a = None
        if u and a and a.role == 's':
            return view_func(request, *args, **kwargs)
        #    if a:
        #        request.user = a[0]
        #        return view_func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))
    return new
