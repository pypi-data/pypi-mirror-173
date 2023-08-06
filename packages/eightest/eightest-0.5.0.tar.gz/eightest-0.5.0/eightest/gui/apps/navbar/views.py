import os
import logging
import threading

from runner import Runner
from utilities import ROOT_DIR
from django.shortcuts import render
from django.http.response import JsonResponse

log = logging.getLogger('main')


def function(request):
    os.chdir(ROOT_DIR)
    runner = Runner()
    runner.dispatch_tasks()
    context = {}
    context['tasks'] = runner.tasks.remaining
    # runner.run_tests()

    try:
        thread = threading.Thread(target=runner.run_tests, args=())
        thread.start()

    except Exception:
        raise Exception

    return render(request, 'home.html', context)


def chris(request):
    data = {'name': 'chris'}
    return JsonResponse(data)
