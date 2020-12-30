
###############################################################################
###############################################################################
# Email function for the app. Used in GraphicsPortion to email the user #######
# about the harmful ingredients in the product. Uses Selenium to log into #####
# the gmail account and send the user an email. Takes in three variables: the #
# receipient's email address, the subject of the email, and the body of the ###
# email. ######################################################################
###############################################################################
###############################################################################

import module_manager
module_manager.review()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter 


#Uses selenium to send an email to the user given an email address, a subject, 
#and a message(body)
def sendEmail(emailAddress, subject, body): 
    driver = webdriver.Chrome('/Users/lauracanseco/Desktop/chromedriver')

    #Email information for skinBot gmail#
    ######################################
    user = 'skinbot15112@gmail.com' 
    password = 'lauracanseco123'
    ######################################

    url = 'gmail.com'
    driver.get('https://' + url)
    driver.implicitly_wait(5)

    #Inputs username 
    driver.find_element_by_id('identifierId').send_keys(user + Keys.ENTER)

    #Inputs password 
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys(password + Keys.ENTER)

    #Clicks "Compose Message" button 
    driver.find_element_by_xpath('/html/body/div[7]/div[3]/div/div[2]/div[1]/div[1]/div[1]/div/div/div/div[1]/div/div').click()

    #Clicks "recepients" button and inputs the given email address 
    driver.find_element_by_id(':9b').click()
    driver.find_element_by_id(':9b').send_keys(emailAddress + Keys.ENTER)

    #Clicks the Subject line and inputs the given subject, then enters the 
    #tab key and inputs the body 
    driver.find_element_by_id(':8t').click()
    driver.find_element_by_id(':8t').send_keys(subject + Keys.TAB + body)

    #Clicks the send button 
    driver.find_element_by_id(':8j').click()


