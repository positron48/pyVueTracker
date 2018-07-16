# - coding: utf-8 -

# Copyright (C) 2007 Patryk Zawadzki <patrys at pld-linux.org>
# Copyright (C) 2007-2012 Toms Baugis <toms.baugis@gmail.com>

# This file is part of Project Hamster.

# Project Hamster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Project Hamster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Project Hamster.  If not, see <http://www.gnu.org/licenses/>.

import datetime as dt
import re
from collections import defaultdict
from backend.lib.hamster import Fact

class Storage(object):

    # signals that are called upon changes
    def tags_changed(self): pass
    def facts_changed(self): pass
    def activities_changed(self): pass

    def dispatch_overwrite(self):
        self.tags_changed()
        self.facts_changed()
        self.activities_changed()

    # facts
    def add_fact(self, fact, start_time=None, end_time=None, temporary=False):
        fact = Fact(fact, start_time=start_time, end_time=end_time)
        start_time = fact.start_time or dt.datetime.now().replace(second=0, microsecond=0)

        self.start_transaction()
        result = self.__add_fact(fact.serialized_name(), start_time, end_time, temporary)
        self.end_transaction()

        if result:
            self.facts_changed()
        return result

    def get_fact(self, fact_id):
        """Get fact by id. For output format see GetFacts"""
        return self.__get_fact(fact_id)

    def update_fact(self, fact_id, fact, start_time, end_time, temporary = False):
        self.start_transaction()
        self.__remove_fact(fact_id)
        result = self.__add_fact(fact, start_time, end_time, temporary)
        self.end_transaction()
        if result:
            self.facts_changed()
        return result

    def stop_tracking(self, end_time):
        """Stops tracking the current activity"""
        facts = self.__get_todays_facts()
        if facts and not facts[-1]['end_time']:
            self.__touch_fact(facts[-1], end_time)
            self.facts_changed()

    def remove_fact(self, fact_id):
        """Remove fact from storage by it's ID"""
        self.start_transaction()
        fact = self.__get_fact(fact_id)
        if fact:
            self.__remove_fact(fact_id)
            self.facts_changed()
        self.end_transaction()

    def get_facts(self, start_date, end_date, search_terms=""):
        return self.__get_facts(start_date, end_date, search_terms)

    def get_formated_facts(self, start_date, end_date=None, search_terms=""):

        last_entries = self.get_facts(start_date, end_date, search_terms)

        for k, item in enumerate(last_entries):
            last_entries[k]['delta'] = round(item['delta'].seconds / 3600, 2)
            last_entries[k]['date'] = item['date'].strftime('%d.%m.%Y')
            last_entries[k]['start_time'] = item['start_time'].strftime('%H:%M')
            if item['end_time'] is not None:
                last_entries[k]['end_time'] = item['end_time'].strftime('%H:%M')
            else:
                last_entries[k]['end_time'] = ''

        return last_entries

    def get_todays_facts(self):
        """Gets facts of today, respecting hamster midnight. See GetFacts for
        return info"""
        return self.__get_todays_facts()

    # categories
    def add_category(self, name):
        res = self.__add_category(name)
        self.activities_changed()
        return res

    def get_category_id(self, category):
        return self.__get_category_id(category)

    def update_category(self, id, name):
        self.__update_category(id, name)
        self.activities_changed()

    def remove_category(self, id):
        self.__remove_category(id)
        self.activities_changed()

    def get_categories(self):
        return self.__get_categories()

    # activities
    def add_activity(self, name, category_id = -1):
        new_id = self.__add_activity(name, category_id)
        self.activities_changed()
        return new_id

    def update_activity(self, id, name, category_id):
        self.__update_activity(id, name, category_id)
        self.activities_changed()

    def remove_activity(self, id):
        result = self.__remove_activity(id)
        self.activities_changed()
        return result

    def get_category_activities(self, category_id = -1):
        return self.__get_category_activities(category_id = category_id)

    def get_activities(self, search = ""):
        return self.__get_activities(search)

    def change_category(self, id, category_id):
        changed = self.__change_category(id, category_id)
        if changed:
            self.activities_changed()
        return changed

    def get_activity_by_name(self, activity, category_id, resurrect = True):
        category_id = category_id or None
        if activity:
            return dict(self.__get_activity_by_name(activity, category_id, resurrect) or {})
        else:
            return {}

    # tags
    def get_tags(self, only_autocomplete):
        return self.__get_tags(only_autocomplete)

    def get_tag_ids(self, tags):
        tags, new_added = self.__get_tag_ids(tags)
        if new_added:
            self.tags_changed()
        return tags

    def update_autocomplete_tags(self, tags):
        changes = self.__update_autocomplete_tags(tags)
        if changes:
            self.tags_changed()

    def get_suggestions(self):
        # list of facts of last month
        now = dt.datetime.now()
        last_month = self.get_facts(now - dt.timedelta(days=60), now)
        #return last_month

        # naive recency and frequency rank
        # score is as simple as you get 30-days_ago points for each occurence
        suggestions = defaultdict(int)
        pattern = re.compile(r'\s+')

        for fact in last_month:
            days = 30 - (now - dt.datetime.combine(fact['date'], dt.time())).total_seconds() / 60 / 60 / 24

            label = fact['name']
            if fact['category']:
                label += "@%s" % fact['category']

            label = re.sub(pattern, ' ', label).strip()

            suggestions[label] += days

            if fact['tags']:
                label += " #%s" % (" #".join(fact['tags']))
                suggestions[label] += days

        for rec in self.get_activities():
            label = rec["name"]
            if rec["category"]:
                label += "@%s" % rec["category"]
            label = re.sub(pattern, ' ', label).strip()
            suggestions[label] += 0

        sortedSuggestions = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)

        suggestions = list()
        for rec in sortedSuggestions:
            suggestions.append(rec[0])

        return suggestions