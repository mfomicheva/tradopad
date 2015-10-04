from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .models import Rater, Segment, Rating


def index(request):
    template = loader.get_template('rater/index.html')
    return HttpResponse(template.render(RequestContext(request)))


def finish(request):
    template = loader.get_template('rater/finish.html')
    return HttpResponse(template.render(RequestContext(request)))


def access(request):
    rater, created = Rater.objects.get_or_create(email=request.POST['email'], batch_id=0)
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
    })
    return HttpResponse(template.render(context))
