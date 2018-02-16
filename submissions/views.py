from django.shortcuts import render, redirect
from submissions.models import Contest, Category, Submission, Vote
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def list_contests(request):
    context = {
        'contests': Contest.objects.all()
    }
    return render(request, 'submissions/list_contests.html', context)
 
@login_required
def show_contest(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    submission_count = contest.submission_set.count()
    submitter = set()
    for submission in contest.submission_set.all():
        submitter.add(submission.author)
    voter = {}
    results = {}
    for vote in Vote.objects.filter(submission__contest=contest):
        if vote.user.username not in voter:
            voter[vote.user.username] = {'count': 0, 'average': 0, 'name': vote.user.username}
            
        voter[vote.user.username]['average'] = ((voter[vote.user.username]['average']*voter[vote.user.username]['count'])+vote.score)/(voter[vote.user.username]['count']+1)
        voter[vote.user.username]['count'] += 1
        voter[vote.user.username]['percent'] = 100*voter[vote.user.username]['count']/submission_count
        
        if vote.submission.id not in results:
            results[vote.submission.id] = {'score': 0, 'photo': vote.submission}
        results[vote.submission.id]['score'] += vote.score
        
    context = {
        'contest': contest,
        'submission_count': submission_count,
        'submitter_count': len(submitter),
        'vote_count': len(voter),
        'voters': voter,
        'results': results
    }
    return render(request, 'submissions/show_contest.html', context)

@login_required
def vote(request, contest_id):
    contest = Contest.objects.get(id=contest_id)
    if request.method == 'GET':
        submissions = Submission.objects.filter(contest=contest)
        needvotes = []
        for photo in submissions:
            if photo.vote_set.filter(user=request.user).count() < 1:
                needvotes.append(photo)
                photo.index = len(needvotes)
        context = {
            'contest': contest,
            'submissions': needvotes,
        }
        return render(request, 'submissions/vote.html', context)
    elif request.method == 'POST':
        for entry in request.POST.keys():
            if entry.startswith('vote_'):
                submission_id = entry.split('_')[1]
                score = request.POST.get(entry, 0)
                score = int(score)
                if score < 1:
                    continue
                try:
                    submission = Submission.objects.get(id=submission_id)
                    Vote.objects.create(user=request.user, submission=submission, score=score)
                except:
                    continue
        return redirect('show-contest', contest_id)
