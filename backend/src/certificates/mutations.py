import graphene
from graphql import GraphQLError
from .models import Certificates, StudentCertificates


# Create Certificate
class CreateCertificate(graphene.Mutation):
    id = graphene.ID()
    image = graphene.String()
    pos_title = graphene.Float()
    pos_editable_text = graphene.Float()
    pos_student_name = graphene.Float()
    pos_text = graphene.Float()
    pos_name = graphene.Float()
    pos_from_who = graphene.Float()

    class Argument:
        image = graphene.String(required=True)
        pos_title = graphene.Float(required=True)
        pos_editable_text = graphene.Float(required=True)
        pos_student_name = graphene.Float(required=True)
        pos_text = graphene.Float(required=True)
        pos_name = graphene.Float(required=True)
        pos_from_who = graphene.Float(required=True)

    @classmethod
    def mutate(root, info, image, pos_title, pos_editable_text, pos_student_name, pos_text, pos_name, pos_from_who):
        if not info.context.user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        certificate = Certificates(
            image=image,
            pos_title=pos_title,
            pos_editable_text=pos_editable_text,
            pos_student_name=pos_student_name,
            pos_text=pos_text,
            pos_name=pos_name,
            pos_from_who=pos_from_who
        )
        certificate.save()
        return CreateCertificate(certificate=certificate)


# Update Certificate
class UpdateCertificate(graphene.Mutation):
    certificate_id = graphene.ID()
    image = graphene.String()
    pos_title = graphene.Float()
    pos_editable_text = graphene.Float()
    pos_student_name = graphene.Float()
    pos_text = graphene.Float()
    pos_name = graphene.Float()
    pos_from_who = graphene.Float()

    class Argument:
        certificate_id = graphene.ID(required=True)
        image = graphene.String(required=False)
        pos_title = graphene.Float(required=False)
        pos_editable_text = graphene.Float(required=False)
        pos_student_name = graphene.Float(required=False)
        pos_text = graphene.Float(required=False)
        pos_name = graphene.Float(required=False)
        pos_from_who = graphene.Float(required=False)

    def mutate(root, info, certificate_id, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")

        certificate = Certificates.objects.get(pk=certificate_id)
        if not certificate:
            raise GraphQLError("Certificate does not exist")

        # For each key and value in keyword arguments
        # if each key is exists and the value each key is not null,
        # update the current object with the new value
        for k, v in kwargs.items():
            if certificate.k and v is not None:
                setattr(certificate, k, v)

        certificate.save()
        return UpdateCertificate(certificate=certificate)


# Create Student Certificate
class CreateStudentCertificate(graphene.Mutation):
    id = graphene.ID()
    title = graphene.String()
    editableText = graphene.String()
    text = graphene.String()
    certificate = graphene.Int()
    fromWho = graphene.Int()
    toWho = graphene.Int()

    class Argument:
        title = graphene.String(required=True)
        editableText = graphene.String(required=True)
        text = graphene.String(required=True)
        certificate = graphene.Int(required=True)
        fromWho = graphene.Int(required=True)
        toWho = graphene.Int(required=True)

    def mutate(root, info, title, editable_text, text, certificate, from_who, to_who):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")

        student_certificate = StudentCertificates(title=title, editableText=editable_text,
                                                  text=text, certificate=certificate,
                                                  fromWho=from_who, toWho=to_who)
        student_certificate.save()
        return CreateStudentCertificate(student_certificate=student_certificate, certificate=certificate)


# Update Student Certificate
class UpdateStudentCertificate(graphene.Mutation):
    id = graphene.ID()
    title = graphene.String()
    editableText = graphene.String()
    text = graphene.String()
    certificate = graphene.Int()
    fromWho = graphene.Int()
    toWho = graphene.Int()

    class Argument:
        student_certificate_id = graphene.ID(required=True)
        title = graphene.String(required=False)
        editableText = graphene.String(required=False)
        text = graphene.String(required=False)
        certificate = graphene.Int(required=True)
        fromWho = graphene.Int(required=True)
        toWho = graphene.Int(required=True)

    def mutate(root, info, student_certificate_id, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError("Authentication credentials were not provided")

        student_certificate = StudentCertificates.objects.get(pk=student_certificate_id)
        if not student_certificate:
            raise GraphQLError("Student Certificate does not exist")

        for k, v in kwargs.items():
            if student_certificate.k and v is not None:
                setattr(student_certificate, k, v)

        student_certificate.save()
        return UpdateStudentCertificate(student_certificate=student_certificate)


class Mutation(graphene.ObjectType):
    create_certificate = CreateCertificate.Field()
    update_certificate = UpdateCertificate.Field()
    create_student_certificate = CreateStudentCertificate.Field()
    update_student_certificate = UpdateStudentCertificate.Field()
