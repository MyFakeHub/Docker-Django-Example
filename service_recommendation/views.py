from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import AnalyticsForm
import pickle

from .backend import inspect_random_user
from .backend import inspect_user


def display_non_vas(request):
    with open('tensorflow/result_vas.pkl', 'rb') as f:
        vas_users = pickle.load(f)
    with open('tensorflow/result_non_vas.pkl', 'rb') as f:
        non_vas_users = pickle.load(f)
    with open('tensorflow/result_taken_vas.pkl', 'rb') as f:
        taken_vas = pickle.load(f)
    with open('tensorflow/result_recommendations.pkl', 'rb') as f:
        recommendations = pickle.load(f)

    return render(request, 'service_recommendation/results.html', {'is_vas': False,
                                                                    'vas': vas_users,
                                                                    'non_vas': non_vas_users,
                                                                    'taken_vas': taken_vas,
                                                                    'recommendations': recommendations})

def display_vas(request):
    with open('tensorflow/result_vas.pkl', 'rb') as f:
        vas_profile = pickle.load(f)
    with open('tensorflow/result_taken_vas.pkl', 'rb') as f:
        taken_vas = pickle.load(f)
    
    return render(request, 'service_recommendation/results.html', {'is_vas': True,
                                                                    'vas': vas_profile,
                                                                    'taken_vas': taken_vas})

def index(request):
    if request.method == 'POST':
        form = AnalyticsForm(request.POST)
        if form.is_valid():
            res = inspect_user(form.cleaned_data['msisdn'])
            if res == 0:
                with open('tensorflow/result_type.pkl', 'rb') as f:
                    result_type = pickle.load(f)
                if result_type == 'Non-VAS':
                    return display_non_vas(request)
                else:
                    return display_vas(request)
                    
            else:
                return render(request, 'service_recommendation/debug.html', {'value': 'well something is obviously wrong. debug code: ' + str(res)})

    else:
        form = AnalyticsForm()
    return render(request, 'service_recommendation/index.html', {'form': form})
    
def random(request):
    if request.method == 'POST':
        res = inspect_random_user()
        if res == 0:
            with open('tensorflow/result_vas.pkl', 'rb') as f:
                vas_users = pickle.load(f)
            with open('tensorflow/result_non_vas.pkl', 'rb') as f:
                non_vas_users = pickle.load(f)
            with open('tensorflow/result_taken_vas.pkl', 'rb') as f:
                taken_vas = pickle.load(f)
            with open('tensorflow/result_recommendations.pkl', 'rb') as f:
                recommendations = pickle.load(f)

            return render(request, 'service_recommendation/results.html', {'vas': vas_users,
                                                                            'non_vas': non_vas_users,
                                                                            'taken_vas': taken_vas,
                                                                            'recommendations': recommendations})
        else:
            return render(request, 'service_recommendation/debug.html', {'value': 'well something is obviously wrong. debug code: ' + str(res)})
    else:
        return render(request, 'service_recommendation/debug.html', {'value': 'well something is obviously wrong. debug request method: ' + str(request.method)})

