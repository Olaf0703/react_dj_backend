import graphene
from django.conf import settings
from graphene_django import DjangoObjectType
from block.models import BlockConfigurationKeyword, BlockType, BlockTypeConfiguration, Block
from block.models import BlockConfiguration, BlockPresentation, BlockQuestionPresentation, \
    StudentBlockQuestionPresentationHistory
from block.models import BlockAssignment
from kb.schema import QuestionSchema


class BlockConfigurationKeywordSchema(DjangoObjectType):
    class Meta:
        model = BlockConfigurationKeyword
        fields = "__all__"


class BlockTypeSchema(DjangoObjectType):
    class Meta:
        model = BlockType
        fields = "__all__"

    name = graphene.String()

    def resolve_name(self, info, language_code=None):
        try:
            current_language = info.context.user.language
        except AttributeError:
            current_language = settings.LANGUAGE_CODE

        return self.safe_translation_getter("name", language_code=current_language)


class BlockTypeConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockTypeConfiguration
        fields = "__all__"


class BlockSchema(DjangoObjectType):
    class Meta:
        model = Block
        fields = "__all__"

    questions = graphene.List(QuestionSchema)

    def resolve_questions(self, info):
        return self.questions.all()


class BlockConfigurationSchema(DjangoObjectType):
    class Meta:
        model = BlockConfiguration
        fields = "__all__"


class BlockPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockPresentation
        fields = "__all__"


class StudentBlockQuestionPresentationHistorySchema(DjangoObjectType):
    class Meta:
        model = StudentBlockQuestionPresentationHistory
        fields = "__all__"


class BlockAssignmentSchema(DjangoObjectType):
    class Meta:
        model = BlockAssignment
        fields = "__all__"


# class BlockQuestionSchema(DjangoObjectType):
#     class Meta:
#         model = BlockQuestion
#         fields = "__all__"


class BlockQuestionPresentationSchema(DjangoObjectType):
    class Meta:
        model = BlockQuestionPresentation
        fields = "__all__"


class Query(graphene.ObjectType):
    # ----------------- Block Configuration Keyword ----------------- #

    blocks_configuration_keyword = graphene.List(
        BlockConfigurationKeywordSchema)
    block_configuration_keyword_by_id = graphene.Field(
        BlockConfigurationKeywordSchema, id=graphene.ID())

    def resolve_blocks_configuration_keyword(root, info, **kwargs):
        # Querying a list
        return BlockConfigurationKeyword.objects.all()

    def resolve_block_configuration_keyword_by_id(root, info, id):
        # Querying a single question
        return BlockConfigurationKeyword.objects.get(pk=id)

    # ----------------- Block Type ----------------- #

    blocks_type = graphene.List(BlockTypeSchema)
    block_type_by_id = graphene.Field(BlockTypeSchema, id=graphene.ID())

    def resolve_blocks_type(root, info, **kwargs):
        # Querying a list
        return BlockType.objects.all()

    def resolve_block_type_by_id(root, info, id):
        # Querying a single question
        return BlockType.objects.get(pk=id)

    # ----------------- BlockTypeConfiguration ----------------- #

    blocks_type_configuration = graphene.List(BlockTypeConfigurationSchema)
    block_type_configuration_by_id = graphene.Field(
        BlockTypeConfigurationSchema, id=graphene.ID())

    def resolve_blocks_type_configuration(root, info, **kwargs):
        # Querying a list
        return BlockTypeConfiguration.objects.all()

    def resolve_block_type_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockTypeConfiguration.objects.get(pk=id)

    # ----------------- Block ----------------- #

    blocks = graphene.List(BlockSchema)
    block_by_id = graphene.Field(BlockSchema, id=graphene.ID())
    blocks_by_topic = graphene.List(BlockSchema, id=graphene.ID())

    def resolve_blocks(root, info, **kwargs):
        # Querying a list
        return Block.objects.all()

    def resolve_block_by_id(root, info, id):
        # Querying a single question
        return Block.objects.get(pk=id)

    def resolve_blocks_by_topic(root, info, id):
        # Querying a list of blocks by topic id
        return Block.objects.filter(topic_grade__topic=id)

    # ----------------- BlockConfiguration ----------------- #

    blocks_configuration_type = graphene.List(BlockConfigurationSchema)
    block_configuration_type_by_id = graphene.Field(
        BlockConfigurationSchema, id=graphene.ID())

    def resolve_blocks_configuration(root, info, **kwargs):
        # Querying a list
        return BlockConfiguration.objects.all()

    def resolve_block_configuration_by_id(root, info, id):
        # Querying a single question
        return BlockConfiguration.objects.get(pk=id)

    # ----------------- BlockPresentation ----------------- #

    block_presentations = graphene.List(BlockPresentationSchema)
    block_presentation_by_id = graphene.Field(
        BlockPresentationSchema, id=graphene.ID())
    inactive_block_presentations = graphene.List(BlockPresentationSchema)
    inactive_block_presentation_by_id = graphene.Field(
        BlockPresentationSchema, id=graphene.ID())

    def resolve_block_presentations(root, info, **kwargs):
        # Querying a list
        return BlockPresentation.objects.all()

    def resolve_block_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockPresentation.objects.get(pk=id)

    def resolve_inactive_block_presentations(root, info, **kwargs):
        # Querying a list
        return BlockPresentation.objects.inactive_objects()

    def resolve_inactive_block_presentations_by_id(root, info, id):
        # Querying a single question
        return BlockPresentation.objects.inactive_objects.get(pk=id)

    # ----------------- BlockQuestionPresentation ----------------- #

    blocks_question_presentation = graphene.List(
        BlockQuestionPresentationSchema)
    block_question_presentation_by_id = graphene.Field(
        BlockQuestionPresentationSchema, id=graphene.ID())

    def resolve_blocks_question_presentation(root, info, **kwargs):
        # Querying a list
        return BlockQuestionPresentation.objects.all()

    def resolve_block_question_presentation_by_id(root, info, id):
        # Querying a single question
        return BlockQuestionPresentation.objects.get(pk=id)

    # ----------------- StudentBlockQuestionPresentationHistory ----------------- #
    block_question_presentation_history = graphene.List(
        StudentBlockQuestionPresentationHistorySchema
    )
    block_question_presentation_history_by_id = graphene.Field(
        StudentBlockQuestionPresentationHistorySchema, id=graphene.ID()
    )
    block_question_presentation_history_by_student_id = graphene.List(
        StudentBlockQuestionPresentationHistorySchema, id=graphene.ID()
    )

    def resolve_block_question_presentation_history(root, info, **kwargs):
        return StudentBlockQuestionPresentationHistory.objects.all();

    def resolve_block_question_presentation_history_by_id(root, info, id):
        return StudentBlockQuestionPresentationHistory.objects.get(pk=id);

    def resolve_block_question_presentation_history_by_student_id(root, info, id):
        return StudentBlockQuestionPresentationHistory.objects.filter(student=id)

    # ----------------- BlockAssignment ----------------- #

    block_assignments = graphene.List(
        BlockAssignmentSchema)
    block_assignment_by_student = graphene.Field(
        BlockAssignmentSchema, id=graphene.ID())

    def resolve_block_assignment(root, info, **kwargs):
        # Querying a list
        return BlockAssignment.objects.all()

    def resolve_block_assignment_by_student(root, info, id):
        # Querying a single question
        return BlockAssignment.objects.filter(student=id)
