import graphene
import graphql_jwt
from graphql_jwt import ObtainJSONWebToken

import achievements.schema
import api.schema
import audiences.schema
import block.schema
import block.mutations
import collectibles.schema
import collectibles.mutations
import emails.schema
import experiences.schema
import guardians.schema
import kb.schema
import organization.schema
import organization.mutations
import plans.schema
import students.schema
import students.mutations
import universals.schema
import users.schema
import wallets.schema
import avatars.schema
import avatars.mutations
import bank.mutations
import bank.schema
import plans.mutations
import payments.mutations
import payments.schema
import games.mutations
import games.schema
import users.mutations
import treasuretrack.schema
import treasuretrack.mutations
import badges.schema
from django.utils import timezone

class CustomTokenAuth(ObtainJSONWebToken):

    @classmethod
    def resolve(cls, root, info, **kwargs):
        user = info.context.user

        if hasattr(user, 'student'):
            student_plan = user.student.guardianstudentplan
            if student_plan.is_cancel:
                raise Exception("Please reactive your plan")
            if student_plan.expired_at and student_plan.expired_at < timezone.now():
                raise Exception("Expiration date has expired")

        return cls()


class Mutation(
    api.schema.Mutation,
    block.mutations.Mutation,
    bank.mutations.Mutation,
    students.mutations.Mutation,
    collectibles.mutations.Mutation,
    emails.schema.Mutation,
    avatars.mutations.Mutation,
    plans.mutations.Mutation,
    payments.mutations.Mutation,
    games.mutations.Mutation,
    users.mutations.Mutation,
    treasuretrack.mutations.Mutation,
    organization.mutations.Mutation,
    graphene.ObjectType
):
    token_auth = CustomTokenAuth.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()


class Query(
        avatars.schema.Query,
        achievements.schema.Query,
        api.schema.Query,
        audiences.schema.Query,
        block.schema.Query,
        bank.schema.Query,
        collectibles.schema.Query,
        experiences.schema.Query,
        games.schema.Query,
        guardians.schema.Query,
        kb.schema.Query,
        organization.schema.Query,
        payments.schema.Query,
        plans.schema.Query,
        students.schema.Query,
        treasuretrack.schema.Query,
        users.schema.Query,
        universals.schema.Query,
        wallets.schema.Query,
        badges.schema.Query,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)