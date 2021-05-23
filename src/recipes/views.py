from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag
from recipes import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """ Manage tags in the databse """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """ Return object for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')
