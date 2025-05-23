import django
from django.conf import settings
from django.db import connection
from django.test import TestCase
from django.apps import AppConfig
import os
import sys
import unittest

CURRENT_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_OF_SCRIPT_DIR = os.path.dirname(CURRENT_SCRIPT_DIR)
sys.path.insert(0, PARENT_OF_SCRIPT_DIR)

from drf_test_case.models_for_test import MyModel, PrefixModel
from drf_test_case.serializers_for_test import MyModelSerializer
from rest_framework.fields import HiddenField, SerializerMethodField

class DRFTestCaseAppConfig(AppConfig):
    name = 'drf_test_case'
    path = CURRENT_SCRIPT_DIR
    models_module = 'drf_test_case.models_for_test'

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'rest_framework',
            'drf_test_case.test_runner.DRFTestCaseAppConfig',
        ),
        DEFAULT_AUTO_FIELD='django.db.models.AutoField',
    )
    django.setup()

class TestSerializerMethodFieldUniqueTogether(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(PrefixModel)
            schema_editor.create_model(MyModel)

    def test_smf_becomes_hidden_field(self):
        serializer = MyModelSerializer()
        fields = serializer.fields
        field_in_question = fields['prefix_fk']
        field_type_name = type(field_in_question).__name__
        
        print(f"Type of fields['prefix_fk']: {field_type_name}")
        
        self.assertIsInstance(
            field_in_question,
            HiddenField,
            f"BUG: 'prefix_fk' should be HiddenField. Got {field_type_name}"
        )
        # For testing the fix later:
        # self.assertIsInstance(
        #     field_in_question,
        #     SerializerMethodField,
        #     f"FIXED: 'prefix_fk' should be SerializerMethodField. Got {field_type_name}"
        # )

if __name__ == '__main__':
    print(f"Running tests in {__file__} directly...")
    unittest.main(verbosity=2)
