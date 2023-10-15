from datetime import datetime
from typing import Optional
from itertools import chain
from django.db import models
from django.db.models import Q, QuerySet
from django.contrib import admin


class BaseModelManager(models.Manager):
    use_for_related_fields: bool = True

    def __init__(self, *args, **kwargs):
        self.with_deleted: bool = kwargs.pop("deleted", False)
        super().__init__(*args, **kwargs)

    def _base_queryset(self) -> "QuerySet":
        return super().get_queryset().filter(Q(is_deleted=True) | Q(is_deleted=False))

    def get_queryset(self) -> "QuerySet":
        qs: "QuerySet" = self._base_queryset()
        if self.with_deleted:
            return qs

        return qs.filter(is_deleted=False)


class PrintableMixin:
    def __repr__(self: "models.Model"):
        return str(self.to_dict())

    def to_dict(self: "models.Model") -> dict:
        opts = self._meta
        data: dict = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(self)
            if isinstance(
                f,
                (
                    models.DateTimeField,
                    models.DateField,
                    models.ImageField,
                    models.FileField,
                ),
            ):
                if f.value_from_object(self) is not None:
                    data[f.name] = str(f.value_from_object(self))
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(self)]
        return data


class BaseModel(models.Model, PrintableMixin):
    class Meta:
        abstract: bool = True

    created_at: datetime = models.DateTimeField(
        verbose_name="created at model", auto_now_add=True, null=True
    )

    created_by: datetime = models.IntegerField(
        verbose_name="user creates model",
        help_text="user creates model",
        null=True,
        blank=True,
    )

    updated_at: datetime = models.DateTimeField(
        verbose_name="updated at model", auto_now=True
    )

    updated_by: int = models.IntegerField(
        verbose_name="user updates model",
        help_text="user updates model",
        null=True,
        blank=True,
    )

    is_deleted: bool = models.BooleanField(
        verbose_name="Whether model is deleted",
        default=False,
        help_text="just flag, not delete data actually",
    )

    objects: "BaseModelManager" = BaseModelManager()
    objects_with_deleted: "BaseModelManager" = BaseModelManager(deleted=True)
    objects_for_admin: "models.Manager" = models.Manager()

    def save(self, *args, **kwargs) -> None:  # pylint:disable=signature-differs
        user_id: Optional[str] = kwargs.pop("user_id", None)
        if user_id:
            if self.id:
                self.updated_by = user_id
            else:
                self.created_by = user_id

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs) -> None:  # pylint:disable=signature-differs
        self.is_deleted: bool = True
        self.save(*args, **kwargs)

    def restore(self, *args, **kwargs) -> None:
        self.is_deleted: bool = False
        self.save(*args, **kwargs)

    def hard_delete(self) -> None:
        super().delete()


class BaseModelAdmin(admin.ModelAdmin):
    list_filter: tuple[str] = ("is_deleted",)
    readonly_fields: tuple[str, str, str, str, str] = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "is_deleted",
    )

    def get_queryset(self, request) -> "QuerySet":
        return self.model.objects_for_admin.all()

    def save_model(self, request, obj, form, change) -> None:
        if change:
            obj.updated_by = request.user.id
        else:
            obj.created_by = request.user.id
            obj.updated_by = request.user.id

        super().save_model(request, obj, form, change)
