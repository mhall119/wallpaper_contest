from django.contrib import admin
from django.utils.safestring import mark_safe

from submissions.models import Contest, Category, Submission, Vote
# Register your models here.

admin.site.register(Contest)
admin.site.register(Category)

class SubmissionAdmin(admin.ModelAdmin):
    def view(self, photo):
        return mark_safe('<a href="%s" target="_blank">[view]</a>' % photo.image_url)
    list_display = ('title', 'view', 'author', 'contest', 'category')
    list_filter = ('contest', 'category', 'author')
admin.site.register(Submission, SubmissionAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('submission', 'user', 'score', 'contest')
    list_filter = ('user',)
    def contest(self, vote):
        return vote.submission.contest.name
admin.site.register(Vote, VoteAdmin)

