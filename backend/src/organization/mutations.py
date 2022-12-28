import os
import random
import sys
import graphene
from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from graphene import ID
from organization.models.schools import SchoolPersonnel
from users.schema import UserSchema, UserProfileSchema
from organization.schema import AdministrativePersonnelSchema, ClassroomSchema, SchoolPersonnelSchema, SchoolSchema, TeacherSchema, GroupSchema
from organization.models import School, Group, Teacher, Classroom, AdministrativePersonnel
from graphql_jwt.shortcuts import create_refresh_token, get_token
from payments.models import DiscountCode
from kb.models.grades import Grade
from audiences.models import Audience
from django.contrib.auth.models import User
from students.models import Student, StudentGrade
from students.schema import StudentSchema
class CreateTeacherInput(graphene.InputObjectType):
    email = graphene.String()
    name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    gender = graphene.String()
    user_type = graphene.String()
    username = graphene.String()

class CreateTeacher(graphene.Mutation):
    teacher = graphene.Field(TeacherSchema)
    user = graphene.Field(UserSchema)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        school_id = graphene.ID(required=True)
        zip = graphene.String(required=True)
        country = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        coupon_code = graphene.String(required=False)

    def mutate(
        self,
        info,
        first_name,
        last_name,
        school_id,
        zip,
        country,
        email,
        password,
        username,
        coupon_code=None,
    ):

        try:
            with transaction.atomic():
                school = School.objects.get(pk=school_id)
                user = get_user_model()(
                    first_name = first_name,
                    last_name = last_name,
                    username=username,
                )
                user.set_password(password)
                user.email = email
                user.save()

                teacher= Teacher.objects.create(
                    user=user,
                    name=first_name,
                    last_name=last_name,
                    school=school,
                    zip=zip,
                    country=country,
                )
                if coupon_code:
                    coupon_code = coupon_code.upper()
                    discount = DiscountCode.objects.get(code=coupon_code)
                    teacher.discountCode = discount

                teacher.save();
                
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                
                return CreateTeacher(
                    teacher = teacher,
                    user = user,
                    token = token,
                    refresh_token = refresh_token
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateClassroom(graphene.Mutation):
    user = graphene.Field(UserSchema)
    classroom = graphene.Field(ClassroomSchema)
    teacher = graphene.Field(TeacherSchema)
    class Arguments:
        name = graphene.String(required=True)
        grade_id = graphene.ID(required=True)
        teacher_id = graphene.ID(required=False)
        language = graphene.String(required=True)
        audience_id = graphene.ID(required=True)

    def mutate(
        self,
        info,
        name,
        grade_id,
        language,
        audience_id,
        teacher_id=None,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                grade = Grade.objects.get(pk=grade_id)
                audience = Audience.objects.get(pk=audience_id)
                if teacher_id:
                    teacher = Teacher.objects.get(pk=teacher_id)
                else:
                    teacher = user.schoolpersonnel.teacher;
                user.save()
                classroom = Classroom(
                    name=name,
                    grade=grade,
                    language=language,
                    audience=audience,
                )
                classroom.teacher = teacher
                classroom.save()
                return CreateClassroom(
                    user = user,
                    classroom = classroom,
                    teacher = teacher
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateSchool(graphene.Mutation):
    user = graphene.Field(UserSchema)
    school = graphene.Field(SchoolSchema)
    principle = graphene.Field(AdministrativePersonnelSchema)
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        name = graphene.String(required=True)
        district = graphene.String(required=True)
        type = graphene.String(required=True)
        zip = graphene.String(required=True)
        country = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        username = graphene.String(required=True)

    def mutate(
        self,
        info,
        name,
        district,
        type,
        zip,
        country,
        email,
        password,
        username,
    ):

        try:
            with transaction.atomic():

                school = School(
                    name=name,
                    type_of=type,
                )
                school.save()
                user = get_user_model()(
                    first_name = name,
                    last_name = 'Principle',
                    username = username,
                    email = email,
                )
                user.set_password(password)
                user.email = email
                user.save()
                principle = AdministrativePersonnel(
                    school = school,
                    user = user,
                    name = name,
                    last_name = 'Principle',
                    zip = zip,
                    country = country,
                    district = district
                )
                principle.save()
                token = get_token(user)
                refresh_token = create_refresh_token(user)
                return CreateSchool(
                    user = user,
                    school = school,
                    principle = principle,
                    token = token,
                    refresh_token = refresh_token,
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateTeachersInSchool(graphene.Mutation):
    school = graphene.Field(SchoolSchema)
    class Arguments:
        teachers = graphene.List(CreateTeacherInput)

    def mutate(
        self,
        info,
        teachers
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                school = user.schoolpersonnel.school
                for teacher in teachers:
                    user = get_user_model()(
                        username = teacher.username,
                        first_name = teacher.name,
                        last_name = teacher.last_name
                    )
                    user.set_password(teacher.password)
                    user.email = teacher.email
                    user.save()
                    if(teacher.user_type == "Admin"):
                        admin = AdministrativePersonnel.objects.create(
                            school = school,
                            user = user,
                            name = teacher.name,
                            last_name = teacher.last_name,
                            gender = teacher.gender,
                        )
                    else : 
                        teacher= Teacher.objects.create(
                            school=school,
                            user=user,
                            name=teacher.name,
                            last_name=teacher.last_name,
                            gender = teacher.gender,
                        )

                return CreateTeachersInSchool(
                    school = school
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class UpdateClassroomSettings(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    user = graphene.Field(UserSchema)
    class Arguments:
        classroom_id = graphene.ID()
        language = graphene.String()
        enable_game = graphene.Boolean()
        game_cost = graphene.Int()
        time_zone = graphene.String()
        monday_start = graphene.Time()
        monday_end = graphene.Time()
        tuesday_start = graphene.Time()
        tuesday_end = graphene.Time()
        wednesday_start = graphene.Time()
        wednesday_end = graphene.Time()
        thursday_start = graphene.Time()
        thursday_end = graphene.Time()
        friday_start = graphene.Time()
        friday_end = graphene.Time()
        saturday_start = graphene.Time()
        saturday_end = graphene.Time()
        sunday_start = graphene.Time()
        sunday_end = graphene.Time()
    def mutate(
        self,
        info,
        classroom_id,
        language,
        enable_game,
        game_cost,
        time_zone,
        monday_start,
        monday_end,
        tuesday_start,
        tuesday_end,
        wednesday_start,
        wednesday_end,
        thursday_start,
        thursday_end,
        friday_start,
        friday_end,
        saturday_start,
        saturday_end,
        sunday_start,
        sunday_end,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                classroom = Classroom.objects.get(pk=classroom_id)
                classroom.language = language
                classroom.enable_games = enable_game
                classroom.game_cost = game_cost
                classroom.time_zone = time_zone
                classroom.monday_start = monday_start
                classroom.monday_end = monday_end
                classroom.tuesday_start = tuesday_start
                classroom.tuesday_end = tuesday_end
                classroom.wednesday_start = wednesday_start
                classroom.wednesday_end = wednesday_end
                classroom.thursday_start = thursday_start
                classroom.thursday_end = thursday_end
                classroom.friday_start = friday_start
                classroom.friday_end = friday_end
                classroom.saturday_start = saturday_start
                classroom.saturday_end = saturday_end
                classroom.sunday_start = sunday_start
                classroom.sunday_end = sunday_end
                classroom.save()
                return UpdateClassroomSettings(
                    classroom = classroom,
                    user = user
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class ImportStudentToClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    
    class Arguments:
        username = graphene.String()
        password = graphene.String()
        classroom_id = graphene.ID()

    def mutate(
        self,
        info,
        username,
        password,
        classroom_id,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                student_user = User.objects.get(username = username)
                student = student_user.student
                pwdChkResult = student_user.check_password(password)
                if (pwdChkResult == False) :
                    raise Exception('Password of Student is wrong')
                classroom = Classroom.objects.get(pk=classroom_id)
                student.classroom = classroom;
                student.save()
                return ImportStudentToClassroom(
                    classroom = classroom
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateStudentToClassroom(graphene.Mutation):
    classroom = graphene.Field(ClassroomSchema)
    student = graphene.Field(StudentSchema)
    class Arguments:
        name = graphene.String()
        last_name = graphene.String()
        username = graphene.String()
        password = graphene.String()
        classroom_id = graphene.ID()

    def mutate(
        self,
        info,
        name,
        last_name,
        username,
        password,
        classroom_id,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                
                user = get_user_model()(
                    username = username,
                    first_name = name,
                    last_name = last_name,
                )
                user.set_password(password)
                user.save()
                classroom = Classroom.objects.get(pk=classroom_id)
                student = Student(
                    first_name=name,
                    last_name=last_name,
                    full_name=name + ' ' + last_name,
                    user = user,
                    classroom = classroom,
                    audience = classroom.audience,
                )
                student.save()
                studentGrade = StudentGrade(
                    student = student,
                    grade = classroom.grade 
                )
                studentGrade.save()
                return CreateStudentToClassroom(
                    classroom = classroom,
                    student = student
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class CreateGroup(graphene.Mutation):
    group = graphene.Field(GroupSchema)
    schoolPersonnel = graphene.Field(SchoolPersonnelSchema)
    class Arguments:
        name = graphene.String()
        studentIds = graphene.List(graphene.String)

    def mutate(
        self,
        info,
        name,
        studentIds,
    ):

        try:
            with transaction.atomic():
                user = info.context.user
                if user.is_anonymous:
                    raise Exception('Authentication Required')
                group = Group(
                    name = name,
                    school_personnel = user.schoolpersonnel,
                )
                group.save()
                for studentId in studentIds:
                    student = Student.objects.get(pk = studentId)
                    group.student_set.add(student)
                user.schoolpersonnel.group_set.add(group)
                return CreateGroup(
                    group = group,
                    schoolPersonnel = group.school_personnel
                )

        except (Exception, DatabaseError) as e:
            transaction.rollback()
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return e

class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()
    create_classroom = CreateClassroom.Field()
    create_school = CreateSchool.Field()
    create_teachers_in_school = CreateTeachersInSchool.Field()
    update_classroom_settings = UpdateClassroomSettings.Field()
    import_student_to_classroom = ImportStudentToClassroom.Field()
    create_student_to_classroom = CreateStudentToClassroom.Field()
    create_group = CreateGroup.Field()