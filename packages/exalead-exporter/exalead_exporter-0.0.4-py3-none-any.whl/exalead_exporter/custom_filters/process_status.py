# -*- coding:utf-8 -*-
#************************************************************************
from exalead_exporter.filters import Filter

#************************************************************************
class JobStatusFilter(Filter):

   #********************************
   def filter(self, value):
      if value is None or not isinstance(value, str):
         return value

      if value == "stopped":
         value = 0

      elif value == "started":
         value = 1

      else:
         value = -1

      return value

#************************************************************************
# over