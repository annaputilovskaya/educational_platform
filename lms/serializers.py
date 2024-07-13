from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson, Subscription
from lms.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    """
    Сериализатор урока.
    """

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            VideoLinkValidator(field="video_link"),
        ]


class CourseSerializer(ModelSerializer):
    """
    Сериализатор курса.
    """

    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    subscription = SerializerMethodField(read_only=True)

    def get_subscription(self, course):
        """
        Проверяет наличие подписки пользователя на курс.
        """
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    def get_count_lessons(self, course):
        """
        Возвращает количество уроков в курсе.
        """
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):
    """
    Сериализатор подписки.
    """

    class Meta:
        model = Subscription
        fields = "__all__"
