from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
#from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.db import models

#from account.models import User
from .models import Task, Roadmap, Score
from .forms import TaskForm, TaskEditForm, RoadmapForm

from datetime import date, datetime, timedelta
from calendar import monthrange
from .utils import monday_of_week_one, stats


@login_required(login_url=reverse_lazy('account:login'))
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user == task.roadmap.user:
        return render(request, 'task.html', {'task': task})
    else:
        raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_new(request, pk):
    action = 'New'
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if request.user == roadmap.user:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.roadmap = roadmap
                task.save()
                return redirect('roadmap:task', pk=task.pk)
        else:
            form = TaskForm()
        return render(request, 'task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    action = 'Update'
    if request.user == task.roadmap.user:
        if request.method == 'POST':
            form = TaskEditForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                if task.state == 'ready':
                    task.set_score()
                else:
                    task.unset_score()
                task.save()
                return redirect('roadmap:task', pk=task.pk)
        else:
            form = TaskEditForm(instance=task)
        return render(request, 'task_edit.html', {'form': form, 'action': action})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    roadmap_pk = task.roadmap.pk
    if request.user == task.roadmap.user:
        task.delete()
        return redirect('roadmap:roadmap', pk=roadmap_pk)
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmaps_show(request):
    user = request.user
    roadmaps = user.roadmap_set.all()
    return render(request, 'roadmaps.html', {'roadmaps': roadmaps})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_detail(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.user == request.user:
        tasks = Task.objects.filter(roadmap=roadmap).order_by('state', 'estimate')
        return render(request, 'roadmap_detail.html', {'roadmap': roadmap, 'tasks': tasks})
    raise PermissionDenied


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_stats(request):
    user = request.user
    roadmaps = user.roadmap_set.all()
#
    stat_dict = stats(roadmaps)
#

    return render(request, 'roadmap_stat.html', stat_dict)
                  #{'weeks': weeks, 'months': months})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_new(request):
    if request.method == 'POST':
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.user = request.user
            roadmap.save()
            return redirect('roadmap:roadmaps')
    else:
        form = RoadmapForm()
    return render(request, 'roadmap_new.html', {'form': form})


@login_required(login_url=reverse_lazy('account:login'))
def roadmap_delete(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk)
    if roadmap.user == request.user:
        roadmap.delete()
    else:
        raise PermissionDenied
    return redirect('roadmap:roadmaps')