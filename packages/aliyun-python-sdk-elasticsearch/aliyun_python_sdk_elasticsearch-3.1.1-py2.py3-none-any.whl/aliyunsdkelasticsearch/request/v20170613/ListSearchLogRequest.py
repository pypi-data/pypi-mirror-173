# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RoaRequest
from aliyunsdkelasticsearch.endpoint import endpoint_data

class ListSearchLogRequest(RoaRequest):

	def __init__(self):
		RoaRequest.__init__(self, 'elasticsearch', '2017-06-13', 'ListSearchLog','elasticsearch')
		self.set_uri_pattern('/openapi/instances/[InstanceId]/search-log')
		self.set_method('GET')

		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

	def get_InstanceId(self): # string
		return self.get_path_params().get('InstanceId')

	def set_InstanceId(self, InstanceId):  # string
		self.add_path_param('InstanceId', InstanceId)
	def get_size(self): # integer
		return self.get_query_params().get('size')

	def set_size(self, size):  # integer
		self.add_query_param('size', size)
	def get_query(self): # string
		return self.get_query_params().get('query')

	def set_query(self, query):  # string
		self.add_query_param('query', query)
	def get_endTime(self): # integer
		return self.get_query_params().get('endTime')

	def set_endTime(self, endTime):  # integer
		self.add_query_param('endTime', endTime)
	def get_beginTime(self): # integer
		return self.get_query_params().get('beginTime')

	def set_beginTime(self, beginTime):  # integer
		self.add_query_param('beginTime', beginTime)
	def get_page(self): # integer
		return self.get_query_params().get('page')

	def set_page(self, page):  # integer
		self.add_query_param('page', page)
	def get_type(self): # string
		return self.get_query_params().get('type')

	def set_type(self, type):  # string
		self.add_query_param('type', type)
