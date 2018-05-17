# -*- coding: utf-8 -*-
from datetime import datetime
import uuid

from django.core.exceptions import ValidationError
from django.test import TestCase
import pytz

from ..models import Document


class DocumentTest(TestCase):
    def setUp(self):
        pass

    def assertRaisesWithMessage(self, exc, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except exc as inst:
            self.assertIn(msg, inst.messages)

    def assertRaisesWithMessageDict(self, exc, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except exc as inst:
            self.assertEqual(msg, inst.message_dict)

    def test_document_save_required_fields(self):
        file_name = "Test File 1.jpg"

        document = Document.objects.create(
            file_name=file_name,
            workflowlevel1_uuids= [str(uuid.uuid4())]
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)

    def test_document_save_all_fields(self):
        file_name = "Test File 1.jpg"

        document = Document.objects.create(
            file_name=file_name,
            file_type='jpg',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
            s3_file_key='TESTKEY',
            s3_bucket='TESTBUCKET',
        )

        document_db = Document.objects.get(pk=document.pk)
        self.assertEqual(document_db.file_name, file_name)
        self.assertEqual(document_db.organization_uuid, 'TestUUID')
        self.assertEqual(document_db.workflowlevel1_uuids, ['TestWF1UUID'])
        self.assertEqual(document_db.workflowlevel2_uuids, ['TestWF2UUID'])
        self.assertEqual(document_db.s3_file_key, 'TESTKEY')
        self.assertEqual(document_db.s3_bucket, 'TESTBUCKET')

    def test_document_save_fails_missing_filename(self):
        document = Document(
            file_type='jpg',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_file_type(self):
        document = Document(
            file_name='file1.x',
            file_type='x',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_file_type2(self):
        document = Document(
            file_name='file1.x',
            file_type='png',
            upload_date=datetime(2018, 1, 1, 12, 30, tzinfo=pytz.UTC),
            organization_uuid="TestUUID",
            workflowlevel1_uuids=['TestWF1UUID'],
            workflowlevel2_uuids=['TestWF2UUID'],
        )

        self.assertRaises(ValidationError, document.save)

    def test_document_save_fails_wrong_date_format(self):
        document = Document(
            file_name='file2.jpg',
            file_type='jpg',
            upload_date='2018.5.5',
        )

        self.assertRaises(ValidationError, document.save)
