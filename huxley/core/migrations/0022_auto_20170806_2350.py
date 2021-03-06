# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-06 20:20
from __future__ import unicode_literals

from datetime import datetime
from django.db import migrations


def migrate_school_data(apps, schema_editor):
    School = apps.get_model('core', 'School')
    Registration = apps.get_model('core', 'Registration')
    Conference = apps.get_model('core', 'Conference')
    conference, created = Conference.objects.get_or_create(
        session=65,
        defaults={
            'start_date': datetime(2017, 3, 5),
            'end_date': datetime(2017, 3, 7),
            'reg_open': datetime(2017, 1, 1),
            'early_reg_close': datetime(2017, 2, 2),
            'reg_close': datetime(2017, 3, 3)
        })
    for school in School.objects.all():
        registration = Registration.objects.create(
            school=school,
            conference=conference,
            registered_at=school.registered,
            num_beginner_delegates=school.beginner_delegates,
            num_intermediate_delegates=school.intermediate_delegates,
            num_advanced_delegates=school.advanced_delegates,
            num_spanish_speaking_delegates=school.spanish_speaking_delegates,
            num_chinese_speaking_delegates=school.chinese_speaking_delegates,
            registration_comments=school.registration_comments,
            is_waitlisted=school.waitlist,
            waivers_completed=school.waivers_completed,
            assignments_finalized=school.assignments_finalized,
            fees_owed=school.fees_owed,
            fees_paid=school.fees_paid,
            modified_at=school.modified_at)

        for committee_preference in list(school.committeepreferences.all()):
            registration.committee_preferences.add(committee_preference)

        for country_preference in school.countrypreferences.all():
            country_preference.registration = registration
            country_preference.save()


class Migration(migrations.Migration):

    dependencies = [('core', '0021_auto_20170801_2332'), ]

    operations = [migrations.RunPython(migrate_school_data)]
