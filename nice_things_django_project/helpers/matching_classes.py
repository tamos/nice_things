# Created on Fri March 9
# 
# authors: Tyler Amos, Kevin Sun, Sashok "I take Crimea" Tyan

from abc import abstractmethod, ABC



class ResultFamily(object):
        
        self.kids = None


	def spawn_offspring(self):
                # this populates kids by instantiating the child classes
                self.kids.append(Food(blablabba))
                DivvY()
                
		pass
        
	def child_leave_nest(self):
                # children are appended and returned as df
                # for i in self.kids:
                # i.make_matches([filters, amtch, query,....])
                #      i.cat to df
                # return df # final df as in final_results
                print('y')




class Results:
	"""
	This is a class, like obviously. 
	"""
	def __init__(self, yelp_results):
		self.yelp_results = yelp_results
                
	
	def make_matches(self, filter_func, match_func, query_func):
                # x = filter_func(self.yelp_results)
                # x2 = match_func(x, self.yelp_results)
                # return query_func(x2, self.table)
                

class Food(Results):
        def __init__(self, query_func, match_func, collect_results_func):
            self.name = None
            self.filter_func = filter_func
##                self.name = name
##                self.addr = addr
##                self.zip_code = zip_code
##                self.latitude = latitude
##                self.longitude = longitude
##                self.inspection_id = inpsection_id
            
####
##	class Labour(self):
##		def __init__(self, filter_func, match_func, query_func):
##			self.name = name
##			self.addr = addr
##			self.zip_code = zip_code
##			self.latitude = latitude
##			self.longitude = longitude	
##			self.case_id = case_id
##
##	class Divvy(self):
##		def __init__(self, filter_func, match_func, query_func):
##			self.name = name
##			self.latitude = latitude
##			self.longitude = longitude
##			self.capacity = capacity
##
##	class Enviro(self):
##		def __init__(self, filter_func, match_func, query_func):
##			self.addr = addr
##			self.latitude = latitude
##			self.longitude = longitude	
##			self.complaints = complaints
##			self.complaints_url = complaints_url
##			self.enforcement = enforcement
##			self.enforcemment_url = enforcemment_url
##			
