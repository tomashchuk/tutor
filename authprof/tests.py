import pytest

from authprof.models import AuthUser


@pytest.mark.django_db
def test_user_create():
    AuthUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert AuthUser.objects.count() == 1


@pytest.mark.django_db
def test_user_type():
    user = AuthUser.objects.create_user(
        'test_student',
        'student@thebeatles.com',
        'johnpassword'
    )
    user.user_type = AuthUser.STUDENT
    user.save()
    assert user.is_student


@pytest.mark.django_db
def test_user_email_unique():
    AuthUser.objects.create_user('john', 'user@thebeatles.com', 'johnpassword')
    try:
        AuthUser.objects.create_user('john', 'user@thebeatles.com', 'johnpassword')
        assert False
    except:
        pass
