from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ivangram.settings import AUTH_USER_MODEL


def cache_key(type, user_pk):
    return CACHE_TYPES[type] % user_pk


class FriendshipManager(models.Manager):
    def friends(self, user):
        key = cache_key("friends", user.pk)
        friends = cache.get(key)

        if friends is None:
            qs = Friend.objects.select_related("from_user").filter(to_user=user)
            friends = [u.from_user for u in qs]
            cache.set(key, friends)

        return friends

    def requests(self, user):
        key = cache_key("requests", user.pk)
        requests = cache.get(key)

        if requests is None:
            qs = FriendshipRequest.objects.filter(to_user=user)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            requests = list(qs)
            cache.set(key, requests)

        return requests

    def sent_requests(self, user):
        key = cache_key("sent_requests", user.pk)
        requests = cache.get(key)

        if requests is None:
            qs = FriendshipRequest.objects.filter(from_user=user)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            requests = list(qs)
            cache.set(key, requests)

        return requests

    def unread_requests(self, user):
        key = cache_key("unread_requests", user.pk)
        unread_requests = cache.get(key)

        if unread_requests is None:
            qs = FriendshipRequest.objects.filter(to_user=user, viewed__isnull=True)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            unread_requests = list(qs)
            cache.set(key, unread_requests)

        return unread_requests

    def unread_request_count(self, user):
        key = cache_key("unread_request_count", user.pk)
        count = cache.get(key)

        if count is None:
            count = FriendshipRequest.objects.filter(
                to_user=user, viewed__isnull=True
            ).count()
            cache.set(key, count)

        return count

    def read_requests(self, user):
        key = cache_key("read_requests", user.pk)
        read_requests = cache.get(key)

        if read_requests is None:
            qs = FriendshipRequest.objects.filter(to_user=user, viewed__isnull=False)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            read_requests = list(qs)
            cache.set(key, read_requests)

        return read_requests

    def rejected_requests(self, user):
        key = cache_key("rejected_requests", user.pk)
        rejected_requests = cache.get(key)

        if rejected_requests is None:
            qs = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=False)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            rejected_requests = list(qs)
            cache.set(key, rejected_requests)

        return rejected_requests

    def unrejected_requests(self, user):
        key = cache_key("unrejected_requests", user.pk)
        unrejected_requests = cache.get(key)

        if unrejected_requests is None:
            qs = FriendshipRequest.objects.filter(to_user=user, rejected__isnull=True)
            qs = self._friendship_request_select_related(qs, "from_user", "to_user")
            unrejected_requests = list(qs)
            cache.set(key, unrejected_requests)

        return unrejected_requests

    def unrejected_request_count(self, user):
        key = cache_key("unrejected_request_count", user.pk)
        count = cache.get(key)

        if count is None:
            count = FriendshipRequest.objects.filter(
                to_user=user, rejected__isnull=True
            ).count()
            cache.set(key, count)

        return count

    def add_friend(self, from_user, to_user, message=None):
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise NameError("Users are already friends")

        if FriendshipRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise NameError("You already requested friendship from this user.")

        if FriendshipRequest.objects.filter(from_user=to_user, to_user=from_user).exists():
            raise NameError("This user already requested friendship from you.")

        if message is None:
            message = ""

        request, created = FriendshipRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

        if created is False:
            raise NameError("Friendship already requested")

        if message:
            request.message = message
            request.save()

        return request

    def remove_friend(self, from_user, to_user):
        try:
            qs = Friend.objects.filter(to_user__in=[to_user, from_user], from_user__in=[from_user, to_user])
            
            if qs:
                qs.delete()
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        friends1 = cache.get(cache_key("friends", user1.pk))
        friends2 = cache.get(cache_key("friends", user2.pk))
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(to_user=user1, from_user=user2)
                return True
            except Friend.DoesNotExist:
                return False


class Friend(models.Model):
    to_user = models.ForeignKey(
        _("To who this users friend"),
        AUTH_USER_MODEL,
        models.CASCADE,
        related_name="friends"
    )
    from_user = models.ForeignKey(
        _("Who you are friend to"),
        AUTH_USER_MODEL,
        models.CASCADE,
        related_name="_unused_friend_relation"
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _("Friend")
        verbose_name_plural = _("Friends")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.to_user_id} is friends with #{self.from_user_id}"

    def save(self, *args, **kwargs):
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        _("This request from this user"),
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_sent",
    )
    to_user = models.ForeignKey(
        _("This request to this user"),
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="friendship_requests_received",
    )
    message = models.TextField(
        _("Message"),
        blank=True,
        max_length=4000,
    )
    created = models.DateTimeField(
        _("This when request was created"),
        default=timezone.now,
    )
    rejected = models.DateTimeField(
        _("This when request was rejected")
        blank=True,
        null=True
    )
    viewed = models.DateTimeField(
        _("This when request was viewed"),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Friendship Request")
        verbose_name_plural = _("Friendship Requests")
        unique_together = ("from_user", "to_user")
        ordering = ['id']

    def __str__(self):
        return f"User #{self.from_user_id} friendship requested #{self.to_user_id}"
