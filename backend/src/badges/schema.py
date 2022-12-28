import graphene
from graphene_django import DjangoObjectType
from .models import Badge


class BadgeSchema(DjangoObjectType):
    class Meta:
        model = Badge
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- Badge ----------------- #

    badges = graphene.List(BadgeSchema)
    badges_by_id = graphene.Field(BadgeSchema, id=graphene.ID())

    def resolve_badges(root, info, **kwargs):
        # Querying a list
        return Badge.objects.all()

    def resolve_badges_by_id(root, info, id):
        # Querying a single question
        return Badge.objects.get(pk=id)
