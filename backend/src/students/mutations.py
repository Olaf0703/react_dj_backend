import os
import random
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from graphene import ID

from api.models import profile
from graphql_jwt.shortcuts import create_refresh_token, get_token
from .models import Student, StudentGrade
from plans.models import StudentPlan
from organization.models import School, Group
from kb.models.grades import Grade
from kb.models import AreaOfKnowledge
from guardians.models import Guardian, GuardianStudent
from audiences.models import Audience
from users.schema import UserSchema, UserProfileSchema
from .schema import StudentGradeSchema
from plans.models import GuardianStudentPlan
from users.models import User
from avatars.models import Avatar, StudentAvatar
from experiences.models import Battery
from organization.models import Classroom

class CreateStudent(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        guardian_student_plan_id = graphene.ID(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        audience = graphene.ID(required=True)
        school = graphene.ID(required=False)
        grade = graphene.ID(required=False)
        group = graphene.ID(required=False)
        dob = graphene.Date(required=False)
        student_plan = graphene.ID(required=False)
        list_subject_id = graphene.List(ID)

    def mutate(
        self,
        info,
        first_name,
        last_name,
        guardian_student_plan_id,
        list_subject_id,
        username,
        password,
        audience,
        school=None,
        grade=None,
        group=None,
        dob=None,
        student_plan=None,
    ):

        try:
            with transaction.atomic():
                user_guardain = info.context.user
                if not user_guardain.is_authenticated:
                    raise Exception(
                        "Authentication credentials were not provided")

                guardian = user_guardain.guardian
                audience = Audience.objects.get(id=audience)

                user = User()
                student = Student(
                    first_name=first_name,
                    last_name=last_name,
                    full_name=first_name + ' ' + last_name,
                    audience=audience
                )

                if(grade):
                    grade = Grade.objects.get(pk=grade)

                if username:
                    user.username = username
                else:
                    count = 1
                    while True:
                        if get_user_model().objects.get(username=username).exists():
                            count += 1
                        else:
                            break
                    user.username = first_name + last_name + count
                if password:
                    user.set_password(password)
                else:
                    user.set_unusable_password()

                user.save()

                student.user = user

                if dob:
                    student.dob = dob

                student.save()

                battery, new = Battery.objects.get_or_create(
                    student=student,
                )
                battery.save()

                guardianStudent = GuardianStudent.objects.create(
                    student=student,
                    guardian=guardian
                )

                # Student Plan
                if student_plan:
                    pass
                elif school:
                    student_plan = School.objects.get(school).student_plan
                elif group:
                    audience = Group.objects.get(group).audience
                    student_plan = Audience.objects.get(audience).student_plan
                elif grade:
                    audience = Grade.objects.get(grade).audience
                    student_plan = Audience.objects.get(audience).student_plan
                else:
                    student_plan = StudentPlan.objects.get_or_create(
                        name='Default Plan')

                student_plan = StudentPlan.objects.get(pk=student_plan)
                student.student_plan.add(student_plan)

                student.save()

                if(grade):
                    student_grade = StudentGrade(
                        student=student,
                        grade=grade,
                    )
                    student_grade.save()

                guardian_student_plan = GuardianStudentPlan.objects.get(
                    pk=guardian_student_plan_id)

                guardian_student_plan.student_id = student.id
                for subject_id in list_subject_id:
                    subject = AreaOfKnowledge.objects.get(pk=subject_id)
                    guardian_student_plan.subject.add(subject)

                guardian_student_plan.save()

                # set default avatar
                accessories = Avatar.objects.filter(type_of="ACCESSORIES")
                heads = Avatar.objects.filter(type_of="HEAD")
                clothes = Avatar.objects.filter(type_of="CLOTHES")
                pants = Avatar.objects.filter(type_of="PANTS")

                list_avatar_items = [random.choice(accessories), random.choice(heads), random.choice(clothes), random.choice(pants)]

                for avatar in list_avatar_items:
                    student_avatar = StudentAvatar.objects.create(
                        student_id=student.id, avatar_id=avatar.id)
                    avatar_type = avatar.type_of
                    StudentAvatar.objects.filter(
                        student=student,
                        avatar__type_of=avatar_type,
                        in_use=True).update(
                        in_use=False)
                    student_avatar.in_use = True
                    student_avatar.save()

                profile_obj = profile.objects.get(user=user.id)
                token = get_token(user)
                refresh_token = create_refresh_token(user)

                student.init_student_topic_mastery()
                student.init_student_topic_status()

                return CreateStudent(
                    guardian=guardian,
                    student=student,
                    user=user,
                    profile=profile_obj,
                    token=token,
                    refresh_token=refresh_token
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


class ChangeStudentPassword(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    profile = graphene.Field(UserProfileSchema)

    class Arguments:
        student_id = graphene.ID(required=True)
        password = graphene.String(required=True)

    def mutate(
            self,
            info,
            student_id,
            password):
        try:
            with transaction.atomic():
                # user = info.context.user
                # if not user.is_authenticated:
                #     raise Exception("Authentication credentials were not provided")
                student = Student.objects.get(pk=student_id)
                student.user.set_password(password)
                student.user.save()

                guardian_student = student.guardianstudent_set.all().order_by(
                    'create_timestamp').first()

                profile_obj = profile.objects.get(user=student.user.id)

                return ChangeStudentPassword(
                    guardian=guardian_student.guardian if guardian_student else None,
                    student=student,
                    user=student.user,
                    profile=profile_obj,
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e


class CreateChangeStudentGrade(graphene.Mutation):
    guardian = graphene.Field('guardians.schema.GuardianSchema')
    student = graphene.Field('students.schema.StudentSchema')
    grade = graphene.Field('kb.schema.GradeSchema')
    student_grade = graphene.Field(StudentGradeSchema)

    class Arguments:
        grade_id = graphene.ID(required=True)
        student_id = graphene.ID(required=True)
        is_finished = graphene.Int(required=False)
        percentage = graphene.Float(required=False)
        complete_date = graphene.Date(required=False)
        is_active = graphene.Boolean(required=False)

    def mutate(
            self,
            info,
            grade_id,
            student_id,
            is_finished=None,
            percentage=None,
            complete_date=None,
            is_active=True):

        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.guardian:
            raise Exception("Not found student")
        guardian = user.guardian
        try:
            with transaction.atomic():
                # user = info.context.user
                # if not user.is_authenticated:
                #     raise Exception("Authentication credentials were not provided")

                student_grade, created = StudentGrade.objects.get_or_create(
                    grade_id=grade_id,
                    student_id=student_id
                )

                if is_finished:
                    student_grade.is_finished = is_finished

                if percentage:
                    student_grade.percentage = percentage

                if complete_date:
                    student_grade.complete_date = complete_date

                if not is_active:
                    student_grade.is_active = False

                student_grade.save()
                student = student_grade.student
                student = Student.objects.get(pk=student.id)
                guardian = Guardian.objects.get(pk=guardian.id)
                return CreateChangeStudentGrade(
                    guardian=guardian,
                    student_grade=student_grade,
                    grade=student_grade.grade,
                    student=student_grade.student
                )
        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

# Increase Student's level by one
# Student's info comes from logined user info
#   Input: None
#   Output: {
#               studentSchema,
#               userSchema
#   }


class LevelUp(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)
    # class Arguments:
    #     pass

    def mutate(self, info):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        level_amount = user.student.level.amount
        next_level = user.student.level.__class__.objects.get(
            amount=level_amount + 1)
        if next_level:
            user.student.level = next_level
            user.student.level.save()

        return LevelUp(user=user, student=user.student)

# Set Student's point
# Student's info comes from logined user info
#   Input: Point to set( int )
#   Output: {
#               studentSchema,
#               userSchema
#   }


class setPoint(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    user = graphene.Field(UserSchema)

    class Arguments:
        point_to_set = graphene.Int(required=False)

    def mutate(self, info, point_to_set):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student
        student.points = point_to_set
        student.save()

        return setPoint()


class UpdateIsNew(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')

    def mutate(self, info):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")
        if not user.student:
            raise Exception("Not found student")

        student = user.student
        student.is_new = False
        student.save()

        return UpdateIsNew(student=student)

class UpdateStudent(graphene.Mutation):
    student = graphene.Field('students.schema.StudentSchema')
    class Arguments:
        student_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        grade_id = graphene.ID(required=False)
        last_name = graphene.String(required=False)
        classroom_id = graphene.ID(required=False)
        username = graphene.String(required=False)
        group_id = graphene.ID(required=False)
        password = graphene.String(required=False)

    def mutate(
        self,
        info,
        student_id,
        name=None,
        grade_id=None,
        last_name=None,
        classroom_id=None,
        username=None,
        group_id=None,
        password=None):
        user = info.context.user

        if not user.is_authenticated:
            raise Exception("Authentication credentials were not provided")

        student = Student.objects.get(pk = student_id)
        student.first_name = name
        student.last_name = last_name
        studentGrade = StudentGrade(
            grade = Grade.objects.get(pk = grade_id),
            student = student
        )
        studentGrade.save()
        student.classroom = Classroom.objects.get(pk = classroom_id)
        student.user.username = username
        student.user.first_name = name
        student.user.last_name = last_name
        student.user.set_password(password)
        student.user.save()
        # group actions
        student.save()

        return UpdateIsNew(student=student)


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    change_student_password = ChangeStudentPassword.Field()
    create_change_student_grade = CreateChangeStudentGrade.Field()
    level_up = LevelUp.Field()
    set_point = setPoint.Field()
    update_is_new = UpdateIsNew.Field()
    update_student = UpdateStudent.Field()