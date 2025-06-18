from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from datetime import datetime
from .models import Issue, IssueType
from .forms import IssueForm, UpdateIssueStatusForm
from authe.models import UserProfile

def home(request):
    return render(request, 'main/home.html')

@login_required
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.user = request.user
            issue.save()
            messages.success(request, 'Issue reported successfully!')
            return redirect('issue_detail', pk=issue.pk)
    else:
        form = IssueForm()
    
    return render(request, 'main/create_issue.html', {'form': form})

def issue_detail(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    return render(request, 'main/issue_detail.html', {'issue': issue})

@login_required
def my_issues(request):
    issues = Issue.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/my_issues.html', {'issues': issues})

@login_required
def field_staff_dashboard(request):
    # Check if user is field staff
    try:
        profile = request.user.profile
        if profile.role != 'field_staff':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
    except:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    issues = Issue.objects.all().order_by('-created_at')
    issue_types = IssueType.objects.all()
    
    # Filter by issue type
    issue_type = request.GET.get('issue_type')
    if issue_type:
        issues = issues.filter(issue_type_id=issue_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        issues = issues.filter(status=status)
    
    # Filter by date and time range
    date_from = request.GET.get('date_from')
    time_from = request.GET.get('time_from', '00:00')
    date_to = request.GET.get('date_to')
    time_to = request.GET.get('time_to', '23:59')
    
    if date_from:
        try:
            datetime_from = datetime.strptime(f"{date_from} {time_from}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__gte=datetime_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            datetime_to = datetime.strptime(f"{date_to} {time_to}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__lte=datetime_to)
        except ValueError:
            pass
    
    context = {
        'issues': issues,
        'issue_types': issue_types,
        'status_choices': Issue.STATUS_CHOICES,
        'selected_type': issue_type,
        'selected_status': status,
        'date_from': date_from,
        'time_from': time_from,
        'date_to': date_to,
        'time_to': time_to
    }
    
    return render(request, 'main/field_staff_dashboard.html', context)

@login_required
def officer_dashboard(request):
    # Check if user is officer
    try:
        profile = request.user.profile
        if profile.role != 'officer':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
    except:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    issues = Issue.objects.all().order_by('-created_at')
    issue_types = IssueType.objects.all()
    
    # Filter by issue type
    issue_type = request.GET.get('issue_type')
    if issue_type:
        issues = issues.filter(issue_type_id=issue_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        issues = issues.filter(status=status)
    
    # Filter by date and time range
    date_from = request.GET.get('date_from')
    time_from = request.GET.get('time_from', '00:00')
    date_to = request.GET.get('date_to')
    time_to = request.GET.get('time_to', '23:59')
    
    if date_from:
        try:
            datetime_from = datetime.strptime(f"{date_from} {time_from}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__gte=datetime_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            datetime_to = datetime.strptime(f"{date_to} {time_to}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__lte=datetime_to)
        except ValueError:
            pass
    
    context = {
        'issues': issues,
        'issue_types': issue_types,
        'status_choices': Issue.STATUS_CHOICES,
        'selected_type': issue_type,
        'selected_status': status,
        'date_from': date_from,
        'time_from': time_from,
        'date_to': date_to,
        'time_to': time_to
    }
    
    return render(request, 'main/officer_dashboard.html', context)

@login_required
def analytics(request):
    # Check if user is officer
    try:
        profile = request.user.profile
        if profile.role != 'officer':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
    except:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    # Get issue types with counts
    issue_types_data = Issue.objects.values('issue_type__name').annotate(count=Count('id')).order_by('-count')
    
    # Get all issue types for the dropdown
    issue_types = IssueType.objects.all()
    
    # Get status distribution for a specific issue type if selected
    selected_issue_type = request.GET.get('issue_type')
    status_data = None
    
    if selected_issue_type:
        status_data = Issue.objects.filter(issue_type_id=selected_issue_type).values('status').annotate(count=Count('id')).order_by('-count')
    
    context = {
        'issue_types': issue_types,
        'issue_types_data': list(issue_types_data),
        'status_data': list(status_data) if status_data else None,
        'selected_issue_type': selected_issue_type
    }
    
    return render(request, 'main/analytics.html', context)

@login_required
def update_issue_status(request, pk):
    # Check if user is field staff or officer
    try:
        profile = request.user.profile
        if profile.role not in ['field_staff', 'officer']:
            return JsonResponse({'success': False, 'message': 'Permission denied'})
    except:
        return JsonResponse({'success': False, 'message': 'Permission denied'})
    
    issue = get_object_or_404(Issue, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status and new_status in dict(Issue.STATUS_CHOICES):
            issue.status = new_status
            issue.save()
            return JsonResponse({
                'success': True, 
                'message': 'Status updated successfully',
                'new_status': new_status,
                'display_status': dict(Issue.STATUS_CHOICES)[new_status]
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def issues_map(request):
    issues = Issue.objects.all()
    issue_types = IssueType.objects.all()
    
    # Filter by issue type
    issue_type = request.GET.get('issue_type')
    if issue_type:
        issues = issues.filter(issue_type_id=issue_type)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        issues = issues.filter(status=status)
    
    # Filter by date and time range
    date_from = request.GET.get('date_from')
    time_from = request.GET.get('time_from', '00:00')
    date_to = request.GET.get('date_to')
    time_to = request.GET.get('time_to', '23:59')
    
    if date_from:
        try:
            datetime_from = datetime.strptime(f"{date_from} {time_from}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__gte=datetime_from)
        except ValueError:
            pass
    
    if date_to:
        try:
            datetime_to = datetime.strptime(f"{date_to} {time_to}", '%Y-%m-%d %H:%M')
            issues = issues.filter(created_at__lte=datetime_to)
        except ValueError:
            pass
    
    context = {
        'issues': issues,
        'issue_types': issue_types,
        'status_choices': Issue.STATUS_CHOICES,
        'selected_type': issue_type,
        'selected_status': status,
        'date_from': date_from,
        'time_from': time_from,
        'date_to': date_to,
        'time_to': time_to
    }
    
    return render(request, 'main/issues_map.html', context)