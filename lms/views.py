from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config.settings import TIME_ZONE
from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.permissions import IsModerator, IsOwner
from lms.serializers import (CourseSerializer, LessonSerializer,
                             SubscriptionSerializer)
from lms.tasks import send_mail_about_course_updating
from users.models import User


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator, IsAuthenticated)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner, IsAuthenticated)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner, IsAuthenticated)
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, pk, *args, **kwargs):
        course = Course.objects.get(pk=pk)
        subscriptions = Subscription.objects.filter(course=pk)
        users_list = [subscription.user.id for subscription in subscriptions]
        email_list = []
        for user in users_list:
            email_list.append(User.objects.get(id=user).email)
        send_mail_about_course_updating.delay(email_list, course.title)
        # print(datetime.now(TIME_ZONE))
        # print(course.updated_at)
        # if (datetime.now(TIME_ZONE) - course.updated_at).hours > 4:
        #     send_mail_about_course_updating.delay(email_list, course.title)
        #     print("Отправлено письмо об обновлении курса")
        # else:
        #     print("Курс недавно обновлялся")
        return super().update(request, *args, **kwargs)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsModerator | IsOwner, IsAuthenticated)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsOwner, IsAuthenticated)


class SubscriptionApiView(RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
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
