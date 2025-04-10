from import_export import resources
from .models import User, UserBusinessProfile, BusinessAudience, UserIndustryAnswer, Industry, \
    IndustryQuestion


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserBusinessProfileResource(resources.ModelResource):
    class Meta:
        model = UserBusinessProfile


class BusinessAudienceResource(resources.ModelResource):
    class Meta:
        model = BusinessAudience


class UserIndustryAnswerResource(resources.ModelResource):
    class Meta:
        model = UserIndustryAnswer


class IndustryQuestionResource(resources.ModelResource):
    class Meta:
        model = IndustryQuestion


class IndustryResource(resources.ModelResource):
    class Meta:
        model = Industry
