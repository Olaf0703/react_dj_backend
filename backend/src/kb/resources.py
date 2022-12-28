from app.resources import TranslatableModelResource
from app.widgets import TranslatableForeignKeyWidget
from import_export.fields import Field
from import_export.resources import ModelResource
from .models import Topic, Grade, TopicGrade, Prerequisite, GradePrerequisite
from .models.content import (
    Question,
    AnswerOption,
    QuestionImageAsset,
    QuestionAudioAsset,
    MultipleChoiceAnswerOption,
    MultipleSelectAnswerOption,
    TypeInAnswerOption,
    OrderAnswerOption,
    RelateAnswerOption,
)
from .models.areas_of_knowledge import AreaOfKnowledge


class AreaOfKnowledgeResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    class Meta:
        model = AreaOfKnowledge
        skip_unchanged = True
        report_skipped = False


class TopicResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    parent = Field(
        column_name='parent',
        attribute='parent',
        widget=TranslatableForeignKeyWidget(Topic, 'name')
    )

    class Meta:
        model = Topic
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'language_code',
            'name',
            'is_active',
            'parent',
            'video_assistor',
            'area_of_knowledge',
            'standard_topic',
        )


class GradeResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    name = Field(
        attribute='name'
    )

    class Meta:
        model = Grade
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'language_code',
            'name',
            'audience',
            'is_active',
        )


class TopicGradeResource(ModelResource):
    class Meta:
        model = TopicGrade
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'topic',
            'grade',
            'is_active',
        )
        export_order = (
            'id',
            'topic',
            'grade',
            'is_active'
        )


class QuestionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    question_text = Field(attribute='question_text')

    class Meta:
        model = Question
        skip_unchanged = True
        report_skipped = False
        field = (
            'id',
            'identifier',
            'language_code',
            'question_text',
            'topic',
            'grade',
        )
        export_order = (
            'id',
            'identifier',
            'language_code',
            'question_text',
            'topic',
            'grade',
        )
        exclude = (
            'is_active',
            'random_slug',
            'deleted_timestamp',
            'create_timestamp',
            'update_timestamp',
            'topic_grade',
        )


class QuestionImageAssetResource(ModelResource):
    class Meta:
        model = QuestionImageAsset
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'identifier',
            'question',
            'order',
            'image'
        )
        export_order = (
            'id',
            'identifier',
            'question',
            'order',
            'image'
        )


class MultipleChoiceAnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = MultipleChoiceAnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class MultipleSelectAnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = MultipleSelectAnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class TypeInAnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = TypeInAnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
            'case_sensitive',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
            'case_sensitive',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class OrderAnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = OrderAnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'order',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'order',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class RelateAnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    key = Field(
        attribute='key'
    )

    value = Field(
        attribute='value'
    )

    class Meta:
        model = RelateAnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'key',
            'value',
            'question',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'key',
            'value',
            'question',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class AnswerOptionResource(TranslatableModelResource):
    language_code = Field(
        attribute='_current_language'
    )

    answer_text = Field(
        attribute='answer_text'
    )

    class Meta:
        model = AnswerOption
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        export_order = (
            'id',
            # 'identifier',
            'language_code',
            'answer_text',
            'question',
            'is_correct',
        )
        exclude = (
            'create_timestamp',
            'update_timestamp',
            'random_slug',
        )


class QuestionAudioAssetResource(ModelResource):
    class Meta:
        model = QuestionAudioAsset
        skip_unchanged = True
        report_skipped = False
        fields = (
            'id',
            'identifier',
            'question',
            'order',
            'audio_file'
        )
        export_order = (
            'id',
            'identifier',
            'question',
            'order',
            'audio_file'
        )


class PrerequisiteResource(ModelResource):
    class Meta:
        model = Prerequisite
        skip_unchanged = True
        report_skipped = False
        fields = ['id', 'topic', 'prerequisites']


class GradePrerequisiteResource(ModelResource):
    class Meta:
        model = GradePrerequisite
        skip_unchanged = True
        report_skipped = False
        fields = [
            'id',
            'area_of_knowledge',
            'grade',
            'mastery',
            'competence',
        ]
