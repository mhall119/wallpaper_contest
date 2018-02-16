from django.contrib import admin
from submissions.models import Contest, Category, Submission, Vote
# Register your models here.

admin.site.register(Contest)
admin.site.register(Category)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'contest')
    list_filter = ('contest', 'author')
admin.site.register(Submission, SubmissionAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('submission', 'user', 'score', 'contest')
    list_filter = ('user',)
    def contest(self, vote):
        return vote.submission.contest.name
admin.site.register(Vote, VoteAdmin)

