import pytest
from models import User, Image, Type, Wardrobe

@pytest.fixture
def sample_user():
    return User(
        id=1,
        name='Test User',
        email='test@example.com',
        password='test_password'
    )

@pytest.fixture
def sample_image():
    return Image(name='Test Image', image_url='https://example.com/test_image.jpg')

@pytest.fixture
def sample_type():
    return Type(name='Test Type')

@pytest.fixture
def sample_wardrobe(sample_user, sample_image, sample_type):
    return Wardrobe(name='Test Wardrobe', user=sample_user, image=sample_image, type=sample_type)


# ---------------------------- #
# * Tests are below * #

def test_to_json(sample_user):
    json_data = sample_user.to_json()
    assert json_data['id'] == 1
    assert json_data['name'] == 'Test User'

def test_user(sample_user):
    assert sample_user.name == 'Test User'
    assert sample_user.email == 'test@example.com'
    # assert sample_user.password == 'test_password'
    assert sample_user.password != 'test_password'

def test_image(sample_image):
    assert sample_image.name == 'Test Image'
    assert sample_image.image_url == 'https://example.com/test_image.jpg'

def test_type(sample_type):
    assert sample_type.name == 'Test Type'

def test_wardrobe(sample_wardrobe, sample_user, sample_image, sample_type):
    assert sample_wardrobe.name == 'Test Wardrobe'
    assert sample_wardrobe.user == sample_user
    assert sample_wardrobe.image == sample_image
    assert sample_wardrobe.type == sample_type
