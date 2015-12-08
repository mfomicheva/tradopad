import random
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from dynamic_preferences import global_preferences_registry
from .models import Rater, Segment, Rating

global_preferences = global_preferences_registry.manager()


def index(request):
    template = loader.get_template('rater/index.html')
    return HttpResponse(template.render(RequestContext(request)))


def finish(request):
    template = loader.get_template('rater/finish.html')
    return HttpResponse(template.render(RequestContext(request)))


def access(request):
    rater, created = Rater.objects.get_or_create(email=request.POST['email'])
    if created:
        rater.batch_id = random.randint(1, int(global_preferences['rater__number_of_batches']))
        rater.save()
    response = HttpResponseRedirect(reverse('rater:rate'))
    response.set_cookie('rater_pk', rater.pk)
    return response


def submit_rating(request, segment_id):
    rater = get_object_or_404(Rater, pk=request.COOKIES['rater_pk'])
    Rating.objects.create(rater_id=rater.pk, segment_id=segment_id, rating=request.POST['rating'])
    response = HttpResponseRedirect(reverse('rater:rate'))
    return response


def rate(request):
    rater = get_object_or_404(Rater, pk=request.COOKIES['rater_pk'])
    total_segments = Segment.objects.filter(batch_id=rater.batch_id).count()
    segment_number = Segment.objects.filter(batch_id=rater.batch_id).filter(
        pk__in=Rating.objects.filter(rater_id=rater.pk).values_list('segment_id', flat=True)
    ).count() + 1

    if total_segments > segment_number - 1:
        segment = Segment.objects.filter(batch_id=rater.batch_id).exclude(
            pk__in=Rating.objects.filter(rater_id=rater.pk).values_list('segment_id', flat=True)
        )[0]
    else:
        return HttpResponseRedirect(reverse('rater:finish'))

    template = loader.get_template('rater/rate.html')
    context = RequestContext(request, {
        'total_segments': total_segments,
        'segment_number': segment_number,
        'segment': segment,
        'choices': global_preferences['rater__single_choice_options'].split(';'),
    })
    return HttpResponse(template.render(context))