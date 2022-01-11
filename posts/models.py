from django.db import models
from django.db.models.deletion import CASCADE

from users.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=10000, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    created_by = models.ForeignKey('users.User', related_name="created_by", on_delete=CASCADE,)

    class Meta:
        ordering = ['created_at']


class PostLikedBy(models.Model):
    post = models.ForeignKey(Post, related_name="liked_post", on_delete=models.DO_NOTHING,)
    liked_by = models.ForeignKey('users.User', related_name="liked_by", on_delete=CASCADE,)
    liked = models.BooleanField(default=1,)

    class Meta:
        managed = True
        unique_together = ('post', 'liked_by')


class CommentOnPost(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.DO_NOTHING,)
    commented_by = models.ForeignKey('users.User', related_name="commented_by", on_delete=CASCADE,)
    comment = models.CharField(max_length=10000, null=False)

    def __str__(self):
        return self.comment