import pytest
from pydantic import ValidationError
from mt_metadata.common import Person, Comment


def test_person_default_values(subtests):
    """
    Test the default values of the Person model.
    """
    person = Person()

    with subtests.test("default name is empty string"):
        assert person.name == ""

    with subtests.test("default organization is None"):
        assert person.organization is None

    with subtests.test("default email is None"):
        assert person.email is None

    with subtests.test("default url is None"):
        assert person.url is None

    with subtests.test("comments is Comment instance"):
        assert isinstance(person.comments, Comment)

    with subtests.test("comments value is None"):
        assert person.comments.value is None


def test_person_custom_values(subtests):
    """
    Test the Person model with custom values.
    """
    person = Person(
        name="John Doe",
        organization="MT Gurus",
        email="john.doe@mtgurus.org",
        url="https://mtgurus.org",
        comments="Lead researcher",
    )

    with subtests.test("name is set correctly"):
        assert person.name == "John Doe"

    with subtests.test("organization is set correctly"):
        assert person.organization == "MT Gurus"

    with subtests.test("email is set correctly"):
        assert person.email == "john.doe@mtgurus.org"

    with subtests.test("url is set correctly"):
        assert person.url.unicode_string() == "https://mtgurus.org/"

    with subtests.test("comments is Comment instance"):
        assert isinstance(person.comments, Comment)

    with subtests.test("comments value is set correctly"):
        assert person.comments.value == "Lead researcher"


def test_person_partial_values(subtests):
    """
    Test the Person model with partial values.
    """
    person = Person(
        name="Jane Smith",
        email="jane.smith@mtgurus.org",
    )

    with subtests.test("name is set correctly"):
        assert person.name == "Jane Smith"

    with subtests.test("organization is None"):
        assert person.organization is None

    with subtests.test("email is set correctly"):
        assert person.email == "jane.smith@mtgurus.org"

    with subtests.test("url is None"):
        assert person.url is None

    with subtests.test("comments is Comment instance"):
        assert isinstance(person.comments, Comment)

    with subtests.test("comments value is None"):
        assert person.comments.value is None


def test_person_invalid_email(subtests):
    """
    Test the Person model with an invalid email.
    """
    with subtests.test("invalid email raises ValidationError"):
        with pytest.raises(ValidationError):
            Person(email="invalid-email")  # Invalid email format


def test_person_invalid_url(subtests):
    """
    Test the Person model with an invalid URL.
    """
    with subtests.test("invalid URL raises ValidationError"):
        with pytest.raises(ValidationError):
            Person(url="invalid-url")  # Invalid URL format


def test_person_comments_as_string(subtests):
    """
    Test the Person model with comments provided as a string.
    """
    person = Person(comments="Expert in MT data processing")

    with subtests.test("comments is Comment instance"):
        assert isinstance(person.comments, Comment)

    with subtests.test("comments value is set correctly"):
        assert person.comments.value == "Expert in MT data processing"


def test_person_comments_as_comment_object(subtests):
    """
    Test the Person model with comments provided as a Comment object.
    """
    comment = Comment(value="Expert in MT data processing")
    person = Person(comments=comment)

    with subtests.test("comments object is preserved"):
        assert person.comments == comment


def test_author_alias(subtests):
    """
    Test the Person model with the author alias.
    """
    person = Person(author="J. Doe")

    with subtests.test("author sets name"):
        assert person.name == "J. Doe"


def test_person_with_kwargs(subtests):
    """
    Test the Person model initialization with kwargs.
    """
    # Create a dictionary of kwargs
    kwargs = {
        "name": "Robert Johnson",
        "organization": "Research University",
        "email": "robert@research-univ.edu",
        "url": "https://research-univ.edu/team/robert",
        "comments": "Data acquisition specialist",
    }

    # Initialize using kwargs unpacking
    person = Person(**kwargs)

    with subtests.test("name from kwargs is set correctly"):
        assert person.name == kwargs["name"]

    with subtests.test("organization from kwargs is set correctly"):
        assert person.organization == kwargs["organization"]

    with subtests.test("email from kwargs is set correctly"):
        assert person.email == kwargs["email"]

    with subtests.test("url from kwargs is set correctly"):
        assert person.url.unicode_string() == "https://research-univ.edu/team/robert"

    with subtests.test("comments from kwargs is set correctly"):
        assert person.comments.value == kwargs["comments"]


def test_person_with_partial_kwargs(subtests):
    """
    Test the Person model initialization with partial kwargs.
    """
    # Create a dictionary with only some fields
    kwargs = {"name": "Sarah Jones", "url": "https://mtsurvey.org/staff/sarah"}

    # Initialize using kwargs unpacking
    person = Person(**kwargs)

    with subtests.test("specified fields are set correctly"):
        assert person.name == "Sarah Jones"
        assert person.url.unicode_string() == "https://mtsurvey.org/staff/sarah"

    with subtests.test("unspecified fields have default values"):
        assert person.organization is None
        assert person.email is None
        assert person.comments.value is None


def test_person_with_nested_kwargs(subtests):
    """
    Test the Person model with nested object initialization through kwargs.
    """
    # Create kwargs with nested Comment value
    kwargs = {
        "name": "David Miller",
        "comments": {"value": "Field technician", "author": "Admin"},
    }

    person = Person(**kwargs)

    with subtests.test("name is set correctly"):
        assert person.name == "David Miller"

    with subtests.test("comments is Comment instance"):
        assert isinstance(person.comments, Comment)

    with subtests.test("comments value is set correctly"):
        assert person.comments.value == "Field technician"

    with subtests.test("comments author is set correctly"):
        assert person.comments.author == "Admin"
