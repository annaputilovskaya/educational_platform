from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import (CourseSerializer, LessonSerializer,
                             SubscriptionSerializer)
from lms.tasks import send_mail_about_course_updating
from users.models import User


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер списка курсов с постраничным выводом."
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(operation_description="Контроллер создания курса."),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(operation_description="Контроллер удаления курса."),
)
class CourseViewSet(ModelViewSet):
    """
    Контроллер курса.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        """
        Получает права доступа для разных действий.
        """
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner, IsAuthenticated)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner, IsAuthenticated)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Добавляет сведения о владельце при внесении информации о созданном курсе в БД.
        """
        serializer.save(owner=self.request.user)

    def update(self, request, pk, *args, **kwargs):
        """
        Проверяет, не прошло ли более чем четыре часа с момента последнего изменения курса.
        Если да, отправляет письма с уведомлением об этом на адреса подписчиков.
        """
        course = Course.objects.get(pk=pk)
        tmp_date = timezone.now() - timezone.timedelta(hours=4)
        if not course.updated_at or course.updated_at < tmp_date:
            subscriptions = Subscription.objects.filter(course=pk)
            users_list = [subscription.user.id for subscription in subscriptions]
            email_list = []
            for user in users_list:
                email_list.append(User.objects.get(id=user).email)
            send_mail_about_course_updating.delay(email_list, course.title)
            print("Отправлены письма об обновлении курса")
        else:
            print("Курс недавно обновлялся")
        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(CreateAPIView):
    """
    Контроллер создания урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Добавляет сведения о владельце при внесении информации о созданном уроке в БД.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """
    Контроллер списка уроков c постраничным выводом.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Контроллер детального просмотра урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Контроллер редактирования урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Контроллер удаления урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner, IsAuthenticated)


class SubscriptionApiView(RetrieveAPIView):
    """
    Контроллер подписки на курс.
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        """
        Проверяет, подписан ли пользователь на курс.
        При отсутствии подписики создает ее, а при наличии - удаляет.
        """
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)
        if Subscription.objects.filter(user=user, course=course).exists():
            Subscription.objects.filter(user=user, course=course).delete()
            message = f"Подписка для пользователя {user} на курс {course} удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = f"Подписка для пользователя {user} на курс {course} создана"
        return Response({"message": message})
