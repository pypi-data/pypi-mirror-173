#!/usr/bin/env python

# Copyright 2017-2020 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

from autosubmit.job.job import Job
from bscearth.utils.date import date2str
from autosubmit.job.job_common import Status, Type
from log.log import Log, AutosubmitError, AutosubmitCritical

class DicJobs:
    """
    Class to create jobs from conf file and to find jobs by start date, member and chunk

    :param jobs_list: jobs list to use
    :type job_list: JobList
    :param parser: jobs conf file parser
    :type parser: SafeConfigParser
    :param date_list: start dates
    :type date_list: list
    :param member_list: member
    :type member_list: list
    :param chunk_list: chunks
    :type chunk_list: list
    :param date_format: option to format dates
    :type date_format: str
    :param default_retrials: default retrials for ech job
    :type default_retrials: int

    """

    def __init__(self, jobs_list, parser, date_list, member_list, chunk_list, date_format, default_retrials):
        self._date_list = date_list
        self._jobs_list = jobs_list
        self._member_list = member_list
        self._chunk_list = chunk_list
        self._parser = parser
        self._date_format = date_format
        self.default_retrials = default_retrials
        self._dic = dict()

    def parse_relation(self, section,member=True, unparsed_option=[],called_from=""):
        """
        function to parse a list of chunks or members to be compressible for autosubmit member_list or chunk_list.

        :param section: Which section is being parsed.
        :type section: str
        :param member: Is a member or chunk list?
        :type member: bool
        :param unparsed_option: List obtained from configuration files.
        :type unparsed_option: list
        :param called_from: Parameter used to show a more complete error message if something is not working correctly..
        :type unparsed_option: str
        """
        parsed_list = []
        offset = 1
        if len(unparsed_option) > 0:
            if '-' in unparsed_option or ':' in unparsed_option:
                start_end = [-1, -1]
                count = 0
                if '-' in unparsed_option:
                    for location in unparsed_option.split('-'):
                        location = location.strip('[').strip(']').strip(':')
                        if location == "":
                            location = "-1"
                        start_end[count] = int(location)
                        count = count + 1
                elif ':' in unparsed_option:
                    for location in unparsed_option.split(':'):
                        location = location.strip('[').strip(']').strip(':')
                        if location == "":
                            location = "-1"
                        start_end[count] = int(location)
                        count = count + 1
                if start_end[0] == -1 and start_end[1] == -1:
                    raise AutosubmitCritical(
                        "Wrong format for excluded_member parameter in section {0}\nindex was not found".format(
                            section), 7000)
                elif start_end[0] > -1 and start_end[1] == -1:
                    if member:
                        for member_number in xrange(int(start_end[0]), len(self._member_list)):
                            parsed_list.append(member_number)
                    else:
                        for chunk in xrange(int(start_end[0]), len(self._chunk_list) + 1):  # chunk starts in 1
                            parsed_list.append(chunk)
                elif start_end[0] > -1 and start_end[1] > -1:
                    for item in xrange(int(start_end[0]), int(start_end[1]) + offset):
                        parsed_list.append(item)

                elif start_end[0] == -1 and start_end[1] > -1:
                    if member:
                        for item in xrange(0, int(start_end[1]) + offset):  # include last element
                            parsed_list.append(item)
                    else:
                        for item in xrange(1, int(start_end[1]) + offset):  # include last element
                            parsed_list.append(item)
                elif start_end[0] > start_end[1]:
                    raise AutosubmitCritical(
                        "Wrong format for {1} parameter in section {0}\nStart index is greater than ending index".format(
                            section,called_from), 7011)
                else:
                    raise AutosubmitCritical(
                        "Wrong format for {1} parameter in section {0}\nindex weren't found".format(
                            section), 7011)
            elif ',' in unparsed_option:
                for item in unparsed_option.split(','):
                    parsed_list.append(int(item.strip(": -[]")))
            else:
                try:
                    for item in unparsed_option.split(" "):
                        parsed_list.append(int(item.strip(": -[]")))
                except BaseException as e:
                    raise AutosubmitCritical(
                        "Wrong format for {1} parameter in section {0}".format(section,called_from), 7011,
                        str(e))
            pass
        return parsed_list
    def read_section(self, section, priority, default_job_type, jobs_data=dict()):
        """
        Read a section from jobs conf and creates all jobs for it

        :param default_job_type: default type for jobs
        :type default_job_type: str
        :param jobs_data: dictionary containing the plain data from jobs
        :type jobs_data: dict
        :param section: section to read
        :type section: str
        :param priority: priority for the jobs
        :type priority: int
        """
        running = 'once'
        splits = int(self.get_option(section, "SPLITS", -1))
        if self._parser.has_option(section, 'RUNNING'):
            running = self._parser.get(section, 'RUNNING').lower()
        frequency = int(self.get_option(section, "FREQUENCY", 1))
        if running == 'once':
            self._create_jobs_once(section, priority, default_job_type, jobs_data,splits)
        elif running == 'date':
            self._create_jobs_startdate(section, priority, frequency, default_job_type, jobs_data,splits)
        elif running == 'member':
            self._create_jobs_member(section, priority, frequency, default_job_type, jobs_data,splits, \
                                     self.parse_relation(section,True,self.get_option(section, "EXCLUDED_MEMBERS", []),"EXCLUDED_MEMBERS"), \
                                     self.parse_relation(section,True,self.get_option(section, "INCLUDED_MEMBERS", []),"INCLUDED_MEMBERS"))

        elif running == 'chunk':
            synchronize = self.get_option(section, "SYNCHRONIZE", None)
            delay = int(self.get_option(section, "DELAY", -1))
            self._create_jobs_chunk(section, priority, frequency, default_job_type, synchronize, delay, splits, jobs_data, \
                                    excluded_chunks=self.parse_relation(section,False,self.get_option(section, "EXCLUDED_CHUNKS", []),"EXCLUDED_CHUNKS"), \
                                    excluded_members=self.parse_relation(section,True,self.get_option(section, "EXCLUDED_MEMBERS", []),"EXCLUDED_MEMBERS"), \
                                    included_chunks=self.parse_relation(section,False,self.get_option(section, "INCLUDED_CHUNKS", []),"INCLUDED_CHUNKS"), \
                                    included_members=self.parse_relation(section,True,self.get_option(section, "INCLUDED_MEMBERS", []),"INCLUDED_MEMBERS"))

        pass

    def _create_jobs_once(self, section, priority, default_job_type, jobs_data=dict(),splits=0):
        """
        Create jobs to be run once

        :param section: section to read
        :type section: str
        :param priority: priority for the jobs
        :type priority: int
        """


        if splits <= 0:
            job = self.build_job(section, priority, None, None, None, default_job_type, jobs_data, -1)
            self._dic[section] = job
            self._jobs_list.graph.add_node(job.name)
        else:
            self._dic[section] = []
        total_jobs = 1
        while total_jobs <= splits:
            job = self.build_job(section, priority, None, None, None, default_job_type, jobs_data, total_jobs)
            self._dic[section].append(job)
            self._jobs_list.graph.add_node(job.name)
            total_jobs += 1
        pass

        #self._dic[section] = self.build_job(section, priority, None, None, None, default_job_type, jobs_data)
        #self._jobs_list.graph.add_node(self._dic[section].name)

    def _create_jobs_startdate(self, section, priority, frequency, default_job_type, jobs_data=dict(), splits=-1):
        """
        Create jobs to be run once per start date

        :param section: section to read
        :type section: str
        :param priority: priority for the jobs
        :type priority: int
        :param frequency: if greater than 1, only creates one job each frequency startdates. Always creates one job
                          for the last
        :type frequency: int
        """
        self._dic[section] = dict()
        tmp_dic = dict()
        tmp_dic[section] = dict()
        count = 0
        for date in self._date_list:
            count += 1
            if count % frequency == 0 or count == len(self._date_list):
                if splits <= 0:
                    self._dic[section][date] = self.build_job(section, priority, date, None, None, default_job_type,
                                                              jobs_data)
                    self._jobs_list.graph.add_node(self._dic[section][date].name)
                else:
                    tmp_dic[section][date] = []
                    self._create_jobs_split(splits, section, date, None, None, priority,
                                            default_job_type, jobs_data, tmp_dic[section][date])
                    self._dic[section][date] = tmp_dic[section][date]



    def _create_jobs_member(self, section, priority, frequency, default_job_type, jobs_data=dict(),splits=-1,excluded_members=[],included_members=[]):
        """
        Create jobs to be run once per member

        :param section: section to read
        :type section: str
        :param priority: priority for the jobs
        :type priority: int
        :param frequency: if greater than 1, only creates one job each frequency members. Always creates one job
                          for the last
        :type frequency: int
        :type excluded_members: list
        :param excluded_members: if member index is listed there, the job won't run for this member.

        """
        self._dic[section] = dict()
        tmp_dic = dict()
        tmp_dic[section] = dict()
        for date in self._date_list:
            tmp_dic[section][date] = dict()
            self._dic[section][date] = dict()
            count = 0
            if splits > 0:
                for member in self._member_list:
                    if len(included_members) == 0:
                        if self._member_list.index(member) not in excluded_members:
                            tmp_dic[section][date][member] = []
                    else:
                        if self._member_list.index(member) in included_members:
                            tmp_dic[section][date][member] = []
            for member in self._member_list:
                if self._member_list.index(member)  in excluded_members:
                    continue
                if len(included_members) > 0:
                    if self._member_list.index(member) not in included_members:
                        continue
                count += 1
                if count % frequency == 0 or count == len(self._member_list):
                    if splits <= 0:
                        self._dic[section][date][member] = self.build_job(section, priority, date, member, None,default_job_type, jobs_data,splits)
                        self._jobs_list.graph.add_node(self._dic[section][date][member].name)
                    else:
                        self._create_jobs_split(splits, section, date, member, None, priority,
                                                default_job_type, jobs_data, tmp_dic[section][date][member])
                        self._dic[section][date][member] = tmp_dic[section][date][member]



    def _create_jobs_chunk(self, section, priority, frequency, default_job_type, synchronize=None, delay=0, splits=0, jobs_data=dict(),excluded_chunks=[],excluded_members=[],included_chunks=[],included_members=[]):
        """
        Create jobs to be run once per chunk

        :param synchronize:
        :param section: section to read
        :type section: str
        :param priority: priority for the jobs
        :type priority: int
        :param frequency: if greater than 1, only creates one job each frequency chunks. Always creates one job
                          for the last
        :type frequency: int
        :param delay: if this parameter is set, the job is only created for the chunks greater than the delay
        :type delay: int
        """
        # Temporally creation for unified jobs in case of synchronize

        if synchronize is not None:
            tmp_dic = dict()
            count = 0
            for chunk in self._chunk_list:
                if chunk in excluded_chunks:
                    continue
                if len(included_chunks) > 0:
                    if chunk not in included_chunks:
                        continue
                count += 1
                if delay == -1 or delay < chunk:
                    if count % frequency == 0 or count == len(self._chunk_list):
                        if splits > 1:
                            if synchronize == 'date':
                                tmp_dic[chunk] = []
                                self._create_jobs_split(splits, section, None, None, chunk, priority,
                                                   default_job_type, jobs_data, tmp_dic[chunk])
                            elif synchronize == 'member':
                                tmp_dic[chunk] = dict()
                                for date in self._date_list:
                                    tmp_dic[chunk][date] = []
                                    self._create_jobs_split(splits, section, date, None, chunk, priority,
                                                            default_job_type, jobs_data, tmp_dic[chunk][date])

                        else:
                            if synchronize == 'date':
                                tmp_dic[chunk] = self.build_job(section, priority, None, None,
                                                                chunk, default_job_type, jobs_data)
                            elif synchronize == 'member':
                                tmp_dic[chunk] = dict()
                                for date in self._date_list:
                                    tmp_dic[chunk][date] = self.build_job(section, priority, date, None,
                                                                      chunk, default_job_type, jobs_data)
        # Real dic jobs assignment/creation
        self._dic[section] = dict()
        for date in self._date_list:
            self._dic[section][date] = dict()
            for member in self._member_list:
                if len(included_members) > 0:
                    if self._member_list.index(member) not in included_members:
                        continue
                if self._member_list.index(member) in excluded_members:
                    continue
                self._dic[section][date][member] = dict()
                count = 0
                for chunk in self._chunk_list:
                    if chunk in excluded_chunks:
                        continue
                    if len(included_chunks) > 0:
                        if chunk not in included_chunks:
                            continue
                    count += 1
                    if delay == -1 or delay < chunk:
                        if count % frequency == 0 or count == len(self._chunk_list):
                            if synchronize == 'date':
                                self._dic[section][date][member][chunk] = tmp_dic[chunk]
                            elif synchronize == 'member':
                                self._dic[section][date][member][chunk] = tmp_dic[chunk][date]

                            if splits > 1 and synchronize is None:
                                self._dic[section][date][member][chunk] = []
                                self._create_jobs_split(splits, section, date, member, chunk, priority, default_job_type, jobs_data, self._dic[section][date][member][chunk])
                                pass
                            elif synchronize is None:
                                self._dic[section][date][member][chunk] = self.build_job(section, priority, date, member,
                                                                                             chunk, default_job_type, jobs_data)
                                self._jobs_list.graph.add_node(self._dic[section][date][member][chunk].name)

    def _create_jobs_split(self, splits, section, date, member, chunk, priority, default_job_type, jobs_data, dict):
        total_jobs = 1
        while total_jobs <= splits:
            job = self.build_job(section, priority, date, member, chunk, default_job_type, jobs_data, total_jobs)
            dict.append(job)
            self._jobs_list.graph.add_node(job.name)
            total_jobs += 1

    def get_jobs(self, section, date=None, member=None, chunk=None):
        """
        Return all the jobs matching section, date, member and chunk provided. If any parameter is none, returns all
        the jobs without checking that parameter value. If a job has one parameter to None, is returned if all the
        others match parameters passed

        :param section: section to return
        :type section: str
        :param date: stardate to return
        :type date: str
        :param member: member to return
        :type member: str
        :param chunk: chunk to return
        :type chunk: int
        :return: jobs matching parameters passed
        :rtype: list
        """
        jobs = list()

        if section not in self._dic:
            return jobs

        dic = self._dic[section]
        #once jobs
        if type(dic) is list:
            jobs = dic
        elif type(dic) is not dict:
            jobs.append(dic)
        else:
            if date is not None:
                self._get_date(jobs, dic, date, member, chunk)
            else:
                for d in self._date_list:
                    self._get_date(jobs, dic, d, member, chunk)
        try:
            if len(jobs) > 0:
                if type(jobs[0]) is list:
                    jobs_flattened = [job for jobs_to_flatten in jobs for job in jobs_to_flatten]
                    jobs = jobs_flattened
        except BaseException as e:
            pass
        return jobs

    def _get_date(self, jobs, dic, date, member, chunk):
        if date not in dic:
            return jobs
        dic = dic[date]
        if type(dic) is list:
            for job in dic:
                jobs.append(job)
        elif type(dic) is not dict:
            jobs.append(dic)
        else:
            if member is not None:
                self._get_member(jobs, dic, member, chunk)
            else:
                for m in self._member_list:
                    self._get_member(jobs, dic, m, chunk)

        return jobs

    def _get_member(self, jobs, dic, member, chunk):
        if member not in dic:
            return jobs
        dic = dic[member]
        if type(dic) is not dict:
            jobs.append(dic)
        else:
            if chunk is not None:
                if chunk in dic:
                    jobs.append(dic[chunk])
            else:
                for c in self._chunk_list:
                    if c not in dic:
                        continue
                    jobs.append(dic[c])
        return jobs

    def build_job(self, section, priority, date, member, chunk, default_job_type, jobs_data=dict(), split=-1):
        name = self._jobs_list.expid
        if date is not None:
            name += "_" + date2str(date, self._date_format)
        if member is not None:
            name += "_" + member
        if chunk is not None:
            name += "_{0}".format(chunk)
        if split > -1:
            name += "_{0}".format(split)
        name += "_" + section
        if name in jobs_data:
            job = Job(name, jobs_data[name][1], jobs_data[name][2], priority)
            job.local_logs = (jobs_data[name][8], jobs_data[name][9])
            job.remote_logs = (jobs_data[name][10], jobs_data[name][11])

        else:
            job = Job(name, 0, Status.WAITING, priority)


        job.section = section
        job.date = date
        job.member = member
        job.chunk = chunk
        job.date_format = self._date_format

        if split > -1:
            job.split = split

        job.frequency = int(self.get_option(section, "FREQUENCY", 1))
        job.delay = int(self.get_option(section, "DELAY", -1))
        job.wait = self.get_option(section, "WAIT", 'true').lower() == 'true'
        job.rerun_only = self.get_option(section, "RERUN_ONLY", 'false').lower() == 'true'
        job_type = self.get_option(section, "TYPE", default_job_type).lower()
        job.dependencies = self.get_option(section, "DEPENDENCIES", "").split()
        if job_type == 'bash':
            job.type = Type.BASH
        elif job_type == 'python' or job_type == 'python2':
            job.type = Type.PYTHON2
        elif job_type == 'python3':
            job.type = Type.PYTHON3
        elif job_type == 'r':
            job.type = Type.R
        job.executable = self.get_option(section, "EXECUTABLE", None)

        job.platform_name = self.get_option(section, "PLATFORM", None)
        if job.platform_name is not None:
            job.platform_name = job.platform_name
        job.file = self.get_option(section, "FILE", None)
        job.queue = self.get_option(section, "QUEUE", None)
        job.check = str(self.get_option(section, "CHECK", 'True')).lower()
        job.export = str(self.get_option(section, "EXPORT", None))
        job.processors = str(self.get_option(section, "PROCESSORS", 1))
        job.threads = str(self.get_option(section, "THREADS", 1))
        job.tasks = str(self.get_option(section, "TASKS", '0'))
        job.memory = self.get_option(section, "MEMORY", '')
        job.memory_per_task = self.get_option(section, "MEMORY_PER_TASK", '')
        if job.wallclock is None:
            job.wallclock = self.get_option(section, "WALLCLOCK", None)
        #if job.wallclock is None and job.platform_name.lower() != "local":
        #    job.wallclock = "01:59"
        #elif job.wallclock is None and job.platform_name.lower() == "local":
        #    job.wallclock = "00:00"
        job.retrials = int(self.get_option(section, 'RETRIALS', -1))
        job.delay_retrials = str(self.get_option(section, 'DELAY_RETRY_TIME', "-1"))
        if job.retrials == -1:
            job.retrials = None
        job.notify_on = [x.upper() for x in self.get_option(section, "NOTIFY_ON", '').split(' ')]
        job.synchronize = self.get_option(section, "SYNCHRONIZE", None)
        job.check_warnings = str(self.get_option(section, "SHOW_CHECK_WARNINGS", 'false')).lower()
        job.running = self.get_option(section, 'RUNNING', 'once').lower()
        job.x11 = bool(self.get_option(section, 'X11', False ))

        if self.get_option(section, "SKIPPABLE", "False").lower() == "true":
            job.skippable = True
        else:
            job.skippable = False
        if job.check_warnings == 'true':
            job.check_warnings = True
        else:
            job.check_warnings = False

        self._jobs_list.get_job_list().append(job)

        return job

    def get_option(self, section, option, default):
        """
        Returns value for a given option

        :param section: section name
        :type section: str
        :param option: option to return
        :type option: str
        :param default: value to return if not defined in configuration file
        :type default: object
        """
        if self._parser.has_option(section, option):
            return self._parser.get(section, option)
        else:
            return default

