from django.db.models import QuerySet

from learning.models import Topic, Material, Question


def perform_swift(items: QuerySet, order: int, old_order: int) -> None:
    for item in items:
        if order > old_order:
            if old_order < item.order <= order:
                item.order = item.order - 1
        else:
            if old_order > item.order >= order:
                item.order = item.order + 1
        item.save()


def swift_order_topics(order: int, ctopic: Topic) -> None:
    topics_to_swift = Topic.objects.filter(course_id=ctopic.course_id).exclude(
        id=ctopic.id
    )
    old_order = ctopic.order
    perform_swift(topics_to_swift, order, old_order)


def swift_order_materials(order: int, cmaterial: Material) -> None:
    materials_to_swift = Material.objects.filter(topic_id=cmaterial.topic_id).exclude(
        id=cmaterial.id
    )
    old_order = cmaterial.order
    perform_swift(materials_to_swift, order, old_order)


def swift_order_questions(order: int, cquestion: Question) -> None:
    questions_to_swift = Question.objects.filter(
        material_id=cquestion.material_id
    ).exclude(id=cquestion.id)
    old_order = cquestion.order
    perform_swift(questions_to_swift, order, old_order)
