import pytest
from pydantic import ValidationError
from mt_metadata.common.person_basemodel import Person
from mt_metadata.common.comment_basemodel import Comment


def test_person_default_values():
    """
    Test the default values of the Person model.
    """
    person = Person()

    assert person.name == ""
    assert person.organization is None
    assert person.email is None
    assert person.url is None
    assert isinstance(person.comments, Comment)
    assert person.comments.value == None


def test_person_custom_values():
    """
    Test the Person model with custom values.
    """
    person = Person(
        name="John Doe",
        author="J. Doe",
        organization="MT Gurus",
        email="john.doe@mtgurus.org",
        url="https://mtgurus.org",
        comments="Lead researcher",
    )

    assert person.name == "John Doe"
    assert person.organization == "MT Gurus"
    assert person.email == "john.doe@mtgurus.org"
    assert person.url.unicode_string() == "https://mtgurus.org/"
    assert isinstance(person.comments, Comment)
    assert person.comments.value == "Lead researcher"


def test_person_partial_values():
    """
    Test the Person model with partial values.
    """
    person = Person(
        name="Jane Smith",
        email="jane.smith@mtgurus.org",
    )

    assert person.name == "Jane Smith"
    assert person.organization is None
    assert person.email == "jane.smith@mtgurus.org"
    assert person.url is None
    assert isinstance(person.comments, Comment)
    assert person.comments.value == None


def test_person_invalid_email():
    """
    Test the Person model with an invalid email.
    """
    with pytest.raises(ValidationError):
        Person(email="invalid-email")  # Invalid email format


def test_person_invalid_url():
    """
    Test the Person model with an invalid URL.
    """
    with pytest.raises(ValidationError):
        Person(url="invalid-url")  # Invalid URL format


def test_person_comments_as_string():
    """
    Test the Person model with comments provided as a string.
    """
    person = Person(comments="Expert in MT data processing")

    assert isinstance(person.comments, Comment)
    assert person.comments.value == "Expert in MT data processing"


def test_person_comments_as_comment_object():
    """
    Test the Person model with comments provided as a Comment object.
    """
    comment = Comment(value="Expert in MT data processing")
    person = Person(comments=comment)

    assert person.comments == comment


def test_author_alias():
    """
    Test the Person model with the author alias.
    """
    person = Person(author="J. Doe")

    assert person.name == "J. Doe"
