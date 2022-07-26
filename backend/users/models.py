from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'first_name', 'last_name']
    ADMIN = 'admin'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (USER, 'User'),
    ]
    role = models.CharField('Роль', choices=ROLES, max_length=200, default=USER)
    email = models.EmailField('Почта', max_length=254, unique=True)
    username = models.CharField('Логин', max_length=150, unique=True)
    first_name = models.TextField('Имя', max_length=150)
    last_name = models.TextField('Фамилия', max_length=150)
    password = models.TextField('Пароль', max_length=150)

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('author', 'user'),
            name='unique_object',
        )]
