# TomeRater.py by Tara M.
# A class project for Codeacademy's Python Intensive, Summer 2018
#
# TomeRater is a simple suite of tools one could use to create and manage a 
# collection of users, books and graded book reviews.
#
# User base class takes a name, email and optional list of book objects 
def pad_to_20(text_in):
	return ("{:<20}".format(text_in))

class User(object):

	def __init__(self, name, email, book_list=[]):
		self.name = name
		self.email = email
		
		# Each item in the books dictionary has a 
		# key = Book object and 
		# value = this user's rating for that book
		self.books = {}			

		for item in book_list:
			self.read_book(item)
        
	def get_email(self):
		return(self.email)

	def change_email(self, address):
		self.email = address
		print(pad_to_20("Update:")+"The email address for {} has been changed to {}".format(self.name, 
                                                                              self.email))
	def __repr__(self):
		return(pad_to_20("User:")+"{}, email: {}, books read: {}".format(self.name, self.email, 
		                                                    len(self.books)))

	def __eq__(self, other_user):
		if (self.name == other_user.name and self.email == other_user.email):
			return(True)
		else:
			return(False)       

	# When a user reads a book, his or her rating is stored via this method
	def read_book(self, book, rating=None):
		self.books[book] = rating

	# Returns the average of all the ratings this user has given. 
	def get_average_rating(self):
		running_sum = 0
		running_count = 0
		for rating in self.books.values():
			if rating:
				running_sum += rating
				running_count +=1
		if running_count:
			return(running_sum/running_count)
		else:
			return(0)
			
# Base class for all books, requires only a title & isbn. Book ratings are stored
# in a list at this level
class Book(object):

	def __init__(self,title,isbn):
		self.title=title
		self.isbn = isbn
		self.ratings = [] # list of ratings. Valid values are integers 1-4
	
	# if two books' titles and isbn numbers match, they're equal
	def __eq__(self,other):
		if (self.title == other.title and self.isbn == other.isbn):
			return(True)
		else:
			return(False)
	
	# Because books are used as keys in the TomeRater.books dictionary, books
	# must be hashable.
	def __hash__(self):
		return hash((self.title, self.isbn))

	def __repr__(self):
		return(pad_to_20("Book:") + "A book titled {} with isbn {}".format(
		                                          self.title, 
		                                          self.isbn))
		
	def get_title(self):
		return(self.title)
		
	def get_isbn(self):
		return(self.isbn)

	def set_isbn(self, new_isbn):
		old_isbn = self.isbn
		self.isbn = new_isbn
		print(pad_to_20("Action:")+"The isbn for {} has changed from {} to {}".format(
												self.title,
												old_isbn,
												self.isbn))
												
	# used to add a rating to this book's rating list
	def add_rating(self,rating):
		try:
			if (rating and (rating >=0 and rating <=4)):
				self.ratings.append(rating)
		except:
			print(pad_to_20("ERROR!:")+"Invalid Rating")

	# Returns the average of all ratings given to this book
	def get_average_rating(self):
		running_total = 0
		running_count = 0
		for rating in self.ratings:
			running_total += rating
			running_count += 1
		return(running_total/running_count)

# The Fiction subclass has all the properties of Book plus an author property 
class Fiction(Book):

	def __init__(self, title, author, isbn):
		super().__init__(title, isbn)
		self.author = author

	def __repr__(self):
		return(pad_to_20("Fiction:")+"{} by {}".format(self.title, self.author))
	
	def get_author(self):
		return(self.author)
	
# The Non Fiction subclass has all the properties of Book plus subject and level properties
class Non_Fiction(Book):

	def __init__(self, title, subject, level, isbn):
		super().__init__(title, isbn)
		self.subject = subject
		self.level = level

	def __repr__(self):
		return(pad_to_20("NonFiction:")+"{}, a {} manual on {}".format(self.title, self.level, self.subject))
	
	def get_subject(self):
		return(self.subject)
			
	def get_level(self):
		return(self.level)

class TomeRater(object):

	def __init__(self):
		# the users dictionary has key=email and value=User object
		self.users = {}
		# the books dictionary has key=Book object and value=number of ratings for this book
		self.books = {}
		print("-------------------------------------------------------")
		print("The TomeRater lives!")
		print("-------------------------------------------------------")
		
	def create_book(self,title,isbn):
		return(Book(title,isbn))
				
	def create_novel(self,title,author,isbn):
		return(Fiction(title,author,isbn))
			
	def create_non_fiction(self,title,subject,level,isbn):
		return(Non_Fiction(title,subject,level,isbn))
	
	def add_user(self,name,email,user_books=None):
		if self.users.get(email):
			print(pad_to_20("ERROR!:")+"There is already a user with {} in the TomeRater system".format(
																	email))
		elif not self.email_looks_good(email):
			print(pad_to_20("ERROR!:")+"Trying to add user with invalid email, {}. User not created".format(
																email))		
		else:		
			self.users[email] = User(name, email)
			if user_books:
				for each_book in user_books:
					self.add_book_to_user(each_book, email)

	# When a user rates a book, we add the book and rating to the User.books dictionary,
	# we add the rating to the book.ratings list and we bump the associated counter by 1				
	def add_book_to_user(self,book,email,rating=None):
	
		# the book we're trying to add should either match something in self.books
		# in both isbn & title, 
		if self.bad_isbn(book):
			print(pad_to_20("ERROR!:")+"May not add {} with isbn {} to TomeRater. Duplicate isbn".format(
															book.title, 
															book.isbn)) 
		else:
			# add this book to the related user
			try:
				this_user = self.users[email]			
				this_user.read_book(book,rating)
				book.add_rating(rating)
				if self.books.get(book):
					self.books[book] +=1
				else:
					self.books[book] = 1;				
			except("KeyError"):
				print("No user with email {}".format(email))
			
	def print_catalog(self):
		print("---------------------------")
		print("Our catalog of books:")
		print("---------------------------")

		for book in self.books:
			print(book)

	def print_users(self):
		print("---------------------------")
		print("Our lucky users:")
		print("---------------------------")
		
		for user in self.users.values():
			print(user)

	# Returns the object in the passed group that has the highest get_average_rating()
	# Called by both most_positive_user, and highest_rated_book methods defined below
	def get_highest_average(self,passed_group):
		highest_average = 0
		highest_obj = ""
		for this_object in passed_group:
			this_average = this_object.get_average_rating()
			if this_average > highest_average:
				highest_average = this_average
				highest_obj = this_object
		return(highest_obj)
	
	# Returns a string describing the user who has given, on average, the most positive
	# reviews
	def most_positive_user(self):
		cheeriest_user = self.get_highest_average(self.users.values())
		her_avg_rating = cheeriest_user.get_average_rating()
		
		return_str = "Most Positive User: {} with an average rating of {}".format(
		                                     cheeriest_user.name, 
		                                     her_avg_rating
		                                     )        
		return(return_str)

	# Returns a string describing the book in our catalog with the highest average of 
	# reviews
	def highest_rated_book(self):
		beloved_book = self.get_highest_average(self.books.keys())
		its_avg_rating = beloved_book.get_average_rating()
		return_str = "Highest Rated Book: {} with an average rating of {}".format(
		                                     beloved_book.title, 
		                                     its_avg_rating)        
		return(return_str)
	
	# Returns a formatted string that displays the book read by the most users	
	def get_most_read_book(self):
		highest_count=0
		highest_desc = None
		for each_book_obj, num_times_read in self.books.items():
			if num_times_read > highest_count:
				highest_count = num_times_read
				highest_desc = "Most Read Book:     {} read {} times".format(
													each_book_obj.title,
													num_times_read)
		return(highest_desc) 

	# Compares two books. If their isbn numbers match, but the titles are different,
	# don't allow this item into TomeRater
	def bad_isbn(self, check_book):
		bad_isbn = False
		for each_book_obj, num_times in self.books.items():
			if (check_book.isbn == each_book_obj.isbn) and (check_book.title != each_book_obj.title):
				bad_isbn = True
		return(bad_isbn)
		
	# Checks if email contains an @ sign and a valid domain.
	def email_looks_good(self,email):
		allowed_top_level_domains = [".com", ".edu", ".org"]		
		if (email[-4: ] in allowed_top_level_domains) and ("@" in email):
			return(True)
		else:
			return(False)
