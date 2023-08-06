
import random
import string
from functools import reduce

class PasswordManager:
    
    '''Class which manages to create and change/reset the password'''
    
    def __init__(self, length:int = 8, digits:bool = True, letters:bool = True, mayus:bool = True, punctuation:bool = True):
        
        self.length = length              # the length of the password (by default: 8)
        self.digits = digits              # if password contains digits (by default: True)
        self.letters = letters            # if password contains letters (by default: True)
        self.mayus = mayus                # if password contains capital letters (if letters=False this also, by default: True)
        self.punctuation = punctuation    # if password contains special characters (by default: True)

        # Print recommendations
        if self.length < 4: print('Please, it is recommendable to have at least 4 characters in the password')
        if sum([self.digits, self.letters, self.mayus, self.punctuation]) < 3: 
            print('Please it is recommendable to have a more complex password')

            
    
    def CreatePassword(self):
        
        '''
        Method to create the password meeting class requirements and store it in used passowrds (__password_list)
        
        Input: No input
        Output: Created password (str)
        '''
        
        # Percentage of the password for each requirement
        part = int(self.length / sum([self.digits, self.letters, self.mayus, self.punctuation]))

        password = []

        # Add characters to the password
        for i in range(part):
            if self.digits: password += [random.sample(string.digits, 1)]
            if self.punctuation: password += [random.sample(string.punctuation, 1)]
            if self.letters:
                if self.mayus: password += [random.sample(string.ascii_letters[:26], 1)] + [random.sample(string.ascii_letters[26:], 1)]
                else: password += [random.sample(string.ascii_letters[:26], 1)]              
        if len(password) < self.length: password += [random.sample(string.ascii_letters[:26], self.length - len(password))]

        # Mix the chose characters
        password = ''.join(reduce(lambda a, b: a + b, password))
        self.__current_password = ''.join(random.sample(password, len(password)))
        
        # If list is already created append the new password
        try:
            self.__password_list.append(self.__current_password)
        
        # If there is no list, create ir
        except: 
            self.__password_list = [self.__current_password]
            
        return self.__current_password
    
    
    
    def IsExistingPassword(self, input_password:str):
        
        '''
        Method to ensure if a password has already been used
        
        Input: Password to check if has been used (str)
        Output: Message (has been used / never has been used)
        
        '''
        
        if input_password in self.__password_list: return 'This password has been used'
        else: return 'This password has never been used'        
        
        
    
    def CreateSimilarPasswordABit(self):
        
        '''
        Method to become the current method into a similar one (shuffling)
        
        Input: No input
        Output: Message (changed successfully)
        
        '''
        

        # Shuffle current password
        self.__currrent_password = ''.join(random.sample(self.__currrent_password, len(self.__currrent_password)))
        
        
        # If list is already created append the new password
        try:
            self.__password_list.append(self.__current_password)
        
        # If there is no list, create ir
        except: 
            self.__password_list = [self.__current_password]
        
        return 'Your password has been changed successfully'
    
    
    
    def ResetPassword(self):
        
        '''
        Method to reset the current password to empty (no password)
        
        Input: No input
        Output: Message (deleted successfully)
        
        '''
        
        # Remove current password
        self.__currrent_password = ''
        
        # If list is already created append the new password
        try:
            self.__password_list.append(self.__current_password)
        
        # If there is no list, create ir
        except: 
            self.__password_list = [self.__current_password]
        
        return 'Your password has been deleted successfully'
    
    
    
    def ChangeCurrentPassword(self, new_password:str):
        
        '''
        Method to change the current password with the input one
        
        Input: The new password (str)
        Output: Message (changed successfully)
        
        '''
        
        # Check if new password fits the requirements
        if len(new_password) != self.length: return f'Please check length requirements (should be: {self.length})'
        if self.digits != any(c.isdigit() for c in new_password): return f'Please check digit requirements (should be: {self.digits})'
        if self.punctuation != any(c in string.punctuation for c in new_password): return f'Please check punctuation requirements (should be: {self.punctuation})'
        if self.mayus != any(c == c.upper() if c.isalpha() else False for c in new_password): return f'Please check upper letter requirements (should be: {self.mayus})'
        
        # Change current password
        self.__currrent_password = new_password
        
        # If list is already created append the new password
        try:
            self.__password_list.append(self.__current_password)
        
        # If there is no list, create ir
        except: 
            self.__password_list = [self.__current_password]
        
        return 'Your password has been changed successfully'
    
    
    
        
class CustomisingPassword(PasswordManager):
    
    '''Child class of Password Manager which customises the password and check if a password is secure'''
    
    def __init__(self):
        super().__init__()
        
        
    def CreateCustomisedPassword(self, customised_word:str):
        
        '''
        Method to customise a password with a given word (givenword + random characters from current password)
        [It does not change the current password, to do so use method ChangeCurrentPassword]
        
        Input: Word to add in the password (str)
        Output: Customised password (str)
        
        '''
        
        resta = self.length - len(str(customised_word))
        if resta >= 0:
            return str(customised_word) + ''.join(random.sample(self.CreatePassword(), resta))
        else: return "Your word's length is bigger than the password's length"
        
        
        
    def IsMyPasswordSecure(self, input_password:str):
        
        '''
        Method to check if a password is secure or not taking into account the characteristics
        
        Input: Password to be checked (str)
        Output: A message commenting if the input password is secure
        
        '''
        
        puntos = 0
        minus, mayus, digit, punct = False, False, False, False
        
        if len(input_password) > 6: puntos += 1
        for i in input_password:
            if i.isdigit(): digit = True
            if i in string.punctuation: punct = True
            if i.isalpha() and i == i.upper(): mayus = True
            if i.isalpha() and i == i.lower(): minus = True
                
        puntos += sum([minus, mayus, digit, punct])
        if puntos > 3: return 'Your password is secure'
        else: return 'Your password is not secure, be careful (use our function if you need it)'
