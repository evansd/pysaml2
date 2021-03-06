#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2011 Umeå University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Contains classes and functions that a SAML2.0 Service Provider (SP) may use
to do attribute aggregation.
"""
import logging
#from saml2 import client
from saml2 import BINDING_SOAP

logger = logging.getLogger(__name__)

DEFAULT_BINDING = BINDING_SOAP

class AttributeResolver(object):

    def __init__(self, saml2client, metadata=None, config=None):
        self.metadata = metadata

        self.saml2client = saml2client
        self.metadata = saml2client.config.metadata

    def extend(self, subject_id, issuer, vo_members, name_id_format=None,
                sp_name_qualifier=None, real_id=None):
        """ 
        :param subject_id: The identifier by which the subject is know
            among all the participents of the VO
        :param issuer: Who am I the poses the query
        :param vo_members: The entity IDs of the IdP who I'm going to ask
            for extra attributes
        :param name_id_format: Used to make the IdPs aware of what's going
            on here
        :return: A dictionary with all the collected information about the
            subject
        """
        result = []
        for member in vo_members:            
            for ass in self.metadata.attribute_services(member):
                for attr_serv in ass.attribute_service:
                    logger.info(
                            "Send attribute request to %s" % attr_serv.location)
                    if attr_serv.binding != BINDING_SOAP:
                        continue
                    # attribute query assumes SOAP binding
                    session_info = self.saml2client.attribute_query(
                                        subject_id, 
                                        attr_serv.location, 
                                        issuer_id=issuer, 
                                        sp_name_qualifier=sp_name_qualifier,
                                        nameid_format=name_id_format, 
                                        real_id=real_id)
                    if session_info:
                        result.append(session_info)
        return result
