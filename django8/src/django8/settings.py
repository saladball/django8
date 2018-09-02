
import os
from django.urls.base import reverse_lazy
from telnetlib import AUTHENTICATION
from django.conf.global_settings import AUTHENTICATION_BACKENDS,\
    LOGIN_REDIRECT_URL, MEDIA_URL, MEDIA_ROOT
from social_core.pipeline import social_auth

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#LOGIN_URL : login_required 함수를 통해 비로그인 상태의 유저를 
#해당하는 URL주소로 이동시키기 위한 변수
#reverse : 해당 함수를 호출했을 때 즉시 urls파일을 탐색해서 url주소를 찾음
#reverse_lazy : 해당 함수를 호출했을때 웹서버의 실행이 준비되면 urls파일을
#               탐색해서 url주소를 찾음
LOGIN_URL = reverse_lazy('customlogin:signin')
#로그인을 완료 한 뒤 돌아올 주소
LOGIN_REDIRECT_URL = reverse_lazy('index')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

#인증 처리에 관한 모듈등록
AUTHENTICATION_BACKENDS = (
    #구글 인증
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    #소셜로그인과 User모델클래스 매칭
    'django.contrib.auth.backends.ModelBackend',
    )

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o(4txy&jf5u+mmqj5*^kiv&u_u)d2%pnwzu8dewa160e*$5v&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#127.0.0.1 : 내컴퓨터

ALLOWED_HOSTS = ['localhost','127.0.0.1', '.pythonanywhere.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vote',
    'customlogin',
    'social_django', #소셜로그인에 대한 어플리케이션
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django8.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect'
            ],
        },
    },
]

#구글 개발자 사이트에서 발급받은 키/비밀번호 저장하는 공간
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='286413542165-8momed4dhpujf0mijcdfs1uq20e2fib4.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='PNl1oLB2CzAGpkNBxheszih6'




WSGI_APPLICATION = 'django8.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
#django프로젝트 내에서 파일을 꺼낼 때 사용하는 URL경로
MEDIA_URL = '/files/'
#실제 파일이 저장되는 경로
#os.path.join(경로, 경로) : 두 폴더경로를 붙인 경로 값을 반환
#project 경로 : d:\django
#'files'경로를 추가
#=> d:\django\files\
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')

#http://127.0.0.1:8000/files/1.jpg
#-> 프로젝트경로/files/1.jpg

