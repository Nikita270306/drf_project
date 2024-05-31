from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from users.models import User, Payment, Subscription
from .models import Course, Lesson
from .validators import TitleValodator, YouTubeLinkValidator


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lessons.count', read_only=True)
    lessons = serializers.SerializerMethodField()
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all(), required=False)

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons(self, course):
        return LessonListSerializer(course.lessons.all(), many=True).data


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    validators = [
        TitleValodator(field='title'),
        serializers.UniqueTogetherValidator(fields=['title', 'description'], queryset=Lesson.objects.all()),
        YouTubeLinkValidator(field='video_link')
    ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link']


class PaymentSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())
    user = SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentsForOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'payment_method']



class CourseSerializers(serializers.ModelSerializer):
    all_lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    number_of_lesson = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, object):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=object).exists()

    def get_number_of_lesson(self, course):
        lesson = Lesson.objects.filter(course=course)
        if lesson:
            return lesson.count()
        return 0

    class Meta:
        model = Course
        fields = ('id', 'name', 'preview', 'description', 'all_lessons', 'number_of_lesson', 'sub_status', 'updated_at')


class PaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("course",)
