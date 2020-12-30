###############################################################################
###############################################################################
# Given a user's skin type, skin concern, budget, and sunscreen preference, ###
# productSelenium_v3 finds three recommended products for the user based on ###
# that information. Uses selenium to go on ulta to find lists of potential  ###
# products. Then uses a recursive function pickProduct to select a product  ### 
# from that list that matches the user budget. ################################
###############################################################################
###############################################################################

import module_manager
module_manager.review()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import tkinter 
import random


#Uses selenium to recommend products for user based on products sold at ulta.com
def productRecommenderProgram(skinType, priceRange, skinConcern, sunscreenPreference): 

    #Driver 
    driver = webdriver.Chrome('/Users/lauracanseco/Desktop/chromedriver')
    
    #Finds lists of potential products and their prices 
    resultCleansers, resultCleanserPrices = findCleanser(driver, skinType)
    resultSpecializedProducts, resultSpecializedPrices = findSpecializedProduct(driver, skinConcern)
    resultSunscreens, resultSunscreenPrices = findSunscreen(driver, skinType, sunscreenPreference)
    
    #Sets price range to 30 if user's price range is low 
    if priceRange == 'low': 

        #Selects product from the lists of potential products and their prices 
        resultCleanser, resultCleanserPrice = pickProduct(resultCleansers,resultCleanserPrices, 30)
        resultSpecializedProduct, resultSpecializedProductPrice = pickProduct(resultSpecializedProducts, resultSpecializedPrices, 20)
        resultSunscreen, resultSunscreenPrice = pickProduct(resultSunscreens, resultSunscreenPrices, 40)

        #Finds the rating and number of reviews for the result product 
        resultCleanserRating, resultCleanserReviews = findProductRatingAndReviews(driver, resultCleanser)
        resultSpecializedRating, resultSpecializedReviews = findProductRatingAndReviews(driver, resultSpecializedProduct)
        resultSunscreenRating, resultSunscreenReviews = findProductRatingAndReviews(driver, resultSunscreen)
    
    #Sets a price range of 300 if user's price range is high 
    elif priceRange == 'high': 

        #Selects product from the lists of potential products and their prices 
        resultCleanser, resultCleanserPrice = pickProduct(resultCleansers, resultCleanserPrices, 300)
        resultSpecializedProduct, resultSpecializedProductPrice =pickProduct(resultSpecializedProducts, resultSpecializedPrices, 300)
        resultSunscreen, resultSunscreenPrice = pickProduct(resultSunscreens, resultSunscreenPrices, 300)

        #Finds the rating and number of reviews for the result product 
        resultCleanserRating, resultCleanserReviews = findProductRatingAndReviews(driver, resultCleanser)
        resultSpecializedRating, resultSpecializedReviews = findProductRatingAndReviews(driver, resultSpecializedProduct)
        resultSunscreenRating, resultSunscreenReviews = findProductRatingAndReviews(driver, resultSunscreen)
    
    print('finished!')
    #Returns result products, product ratings, and product number of reviews 
    return (resultCleanser, resultSpecializedProduct, resultSunscreen,
            resultCleanserPrice, resultSpecializedProductPrice, 
            resultSunscreenPrice, resultCleanserRating, resultCleanserReviews, 
            resultSpecializedRating, resultSpecializedReviews, 
            resultSunscreenRating, resultSunscreenReviews)

#Finds cleanser for user based on their skin type 
def findCleanser(driver, skinType): 
    #Opens cleanser page from ulta  
    url = 'www.ulta.com/skin-care-cleansers?N=2794'
    driver.get("https://" + url)
    driver.implicitly_wait(7)
    
    #Possible cleansers and their prices 
    resultCleansers = []
    resultCleanserPrices = []
    resultCleanser = ''
    
    #clicks filter products by 'dry' skin type button
    if (skinType == 'dry'):  
        driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[2]/div[3]/div[2]/ul[2]/ul/fieldset/li[4]/input').click()
    
    #Clicks filter products by 'normal' skin type button 
    elif (skinType == 'normal'): 
        driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[2]/div[3]/div[2]/ul[2]/ul/fieldset/li[2]/input').click()

    #Clicks filter products by 'oily' skin type button 
    elif (skinType == 'oily'):
        driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/div[2]/div[3]/div[2]/ul[2]/ul/fieldset/li[3]/input').click()
    
    driver.implicitly_wait(5)

    #Finds names of products 
    elements = driver.find_elements_by_class_name('prod-desc')
    for element in elements: 
        #Extracts product name 
        product = element.get_attribute('innerText') 
        resultCleansers.append(product)
    
    #Finds prices of product
    elements = driver.find_elements_by_class_name('regPrice')
    for element in elements: 

        text = element.get_attribute('innerText')
        #Cleans string up so the dollar sign is not included in price 
        newText = text[1:]
        resultCleanserPrices.append(newText)
    
    #Returns potential list of cleansers as well as their prices 
    return (resultCleansers, resultCleanserPrices)


#Given a list of potential products and their prices, recusively finds a product 
#for the user by generating a random number to determine the product and then 
#checking to see if it meets the users budget

def findIndex(resultProducts, resultPrices): 
    if len(resultProducts) < len(resultPrices):
        index = random.randint(0, len(resultProducts) - 1)
        return(index)
    else: 
        index = random.randint(0, len(resultPrices) - 1)
        return(index)

def pickProduct(resultProducts, resultPrices, priceRange):
    index = findIndex(resultProducts, resultPrices)
    #Eliminates prices with a dash because it's too difficult to parse through that info 

    if ('-' not in resultPrices[index]): 
        return(pickProductHelper(resultProducts, resultPrices, index, priceRange))

    else: 
        return(pickProduct(resultProducts, resultPrices, priceRange))

#Helper function for recursive pickProduct fn 
def pickProductHelper(resultProducts, resultPrices, index, priceRange): 
    #If product price is less than price range, return that product and its price! 
    if int(float(resultPrices[index])) <= priceRange: 
        resultProduct = resultProducts[index]
        resultProductPrice = resultPrices[index]
        return(resultProduct, resultProductPrice)
    
    #If product price does not meet budget, recurisvely call function
    else:
        index = findIndex(resultProducts, resultPrices)
        #Recursive call to helper fn 
        return(pickProductHelper(resultProducts, resultPrices, index, priceRange))

#Finds specialized product based on user's skin concern 
def findSpecializedProduct(driver, skinConcern): 

    resultSpecializedProducts = []
    resultSpecializedPrices = []

    #Filters products out by acne 
    if skinConcern == 'acne': 
        url = 'www.ulta.com/skin-care-treatment-serums?N=1z13p0kZ27cs'
        driver.get("https://" + url)
        driver.implicitly_wait(5)

        #Finds name of all the potential products 
        elements = driver.find_elements_by_class_name('prod-desc')
        for element in elements: 
            product = element.get_attribute('innerText')
            resultSpecializedProducts.append(product)

        #Finds price of potential prodcuts 
        elements = driver.find_elements_by_class_name('regPrice')
        for element in elements: 
            text = element.get_attribute('innerText')
            newText = text[1:]
            resultSpecializedPrices.append(newText)
        
        #Returns lists of potential specialized product names and prices
        return(resultSpecializedProducts, resultSpecializedPrices)

    #Filters out specialized product out by wrinkle concern 
    elif skinConcern == 'wrinkle': 
        url = 'www.ulta.com/skin-care-treatment-serums?N=1z13p1dZ27cs'
        driver.get("https://" + url)
        driver.implicitly_wait(5)
        
        #Finds name of potential products 
        elements = driver.find_elements_by_class_name('prod-desc')
        for element in elements: 
            product = element.get_attribute('innerText')
            resultSpecializedProducts.append(product)

        #Finds price of potential products 
        elements = driver.find_elements_by_class_name('regPrice')
        for element in elements: 
            text = element.get_attribute('innerText')
            newText = text[1:]
            resultSpecializedPrices.append(newText)
        
        #Returns list of potential specialized products and their prices 
        return(resultSpecializedProducts, resultSpecializedPrices)


#Finds sunscreen based on user's sunscreen preference and skin type 
def findSunscreen(driver, skinType, sunscreenPreference): 

    #Filters products for dry touch 
    if sunscreenPreference == 'dry-touch': 
        resultSunscreenPrices = []
        resultSunscreens = []
        url = 'www.ulta.com/skin-care-suncare-sunscreen?N=27ff'
        driver.get('https://' + url)
        driver.implicitly_wait(5)

    #Filters sunscreen based on skin type of user 

        #Filters out for dry skin type 
        if (skinType == 'dry'):  
            driver.implicitly_wait(5)
            driver.find_element_by_id('refinementsSkinType3').click()
        
        #Filters out for normal skin type 
        elif (skinType == 'normal'): 
            driver.implicitly_wait(5)
            driver.find_element_by_id('refinementsSkinType1').click()
        
        #Filters out for oily skin type 
        elif (skinType == 'oily'):
            driver.implicitly_wait(5)
            driver.find_element_by_id('refinementsSkinType2').click()
        
        driver.implicitly_wait(5)

        #Finds names of all the sunscreens 
        elements = driver.find_elements_by_class_name('prod-desc')
        for element in elements: 
            product = element.get_attribute('innerText')
            resultSunscreens.append(product)
        
        #finds the prices of all the sunscreens 
        elements = driver.find_elements_by_class_name('regPrice')
        for element in elements: 
            text = element.get_attribute('innerText')
            newText = text[1:]
            resultSunscreenPrices.append(newText)
        
        #Returns a lists of potential sunscreens and their prices 
        return(resultSunscreens, resultSunscreenPrices)

    #User prefers to have coverage in their sunscreen 
    elif sunscreenPreference == 'coverage': 
        resultSunscreenPrices = []
        resultSunscreens = []
        
        #Recommends a bb/cc cream for user 
        url = 'www.ulta.com/makeup-face-bb-cc-creams?N=277u'
        driver.get('https://' + url)
        driver.implicitly_wait(5)

        #Finds the names of all the potential products 
        elements = driver.find_elements_by_class_name('prod-desc')
        for element in elements: 
            product = element.get_attribute('innerText')
            resultSunscreens.append(product)
        elements = driver.find_elements_by_class_name('regPrice')

        #Finds the prices of all the potential prodcuts 
        for element in elements: 
            text = element.get_attribute('innerText')
            newText = text[1:]
            resultSunscreenPrices.append(newText)
        
        #Returns lists of potential sunscreens and their prices 
        return(resultSunscreens, resultSunscreenPrices)
        
#Finds product rating and their reviews given a name of a product
def findProductRatingAndReviews(driver, productName): 
    url = 'www.ulta.com'
    driver.get('https://' + url)
    driver.implicitly_wait(18) 

    #Clicks search button on ulta home page and inputs the name of product 
    driver.find_element_by_class_name('form-control').send_keys(productName + Keys.ENTER)
    driver.implicitly_wait(10)

    #Checks if the product is hyperlinked or the product needs to be clicked on 
    #If value is False then the product is immediately hyperlinked, if value is 
    #True then the product must be clicked on 
    value = len(driver.find_elements_by_class_name('prod-desc')) > 0

    #Product needs to be clicked on 
    if value == True: 
        
        #Clicks on product 
        driver.find_element_by_class_name('prod-desc').click()  
        driver.implicitly_wait(10)

        #Finds the product rating by finding innerText for element 
        element = driver.find_element_by_class_name('pr-snippet-rating-decimal')
        productRating = element.get_attribute('innerText')

        #Finds the product number of reviews 
        element = driver.find_element_by_class_name("pr-snippet-review-count")
        productReviews = element.get_attribute('innerText')
        
        #Cleans data 
        productNumberOfReviews = productReviews[:-8]

    #Product was directly hyperlinked 
    elif value == False: 
        driver.implicitly_wait(10)

        #Finds the product rating by finding innerText for element 
        element = driver.find_element_by_class_name('pr-snippet-rating-decimal')
        productRating = element.get_attribute('innerText')

        #Finds the product number of reviews 
        element = driver.find_element_by_class_name("pr-snippet-review-count")
        productReviews = element.get_attribute('innerText')
        
        #Cleans data 
        productNumberOfReviews = productReviews[:-8]
    
    return(productRating, productNumberOfReviews)
