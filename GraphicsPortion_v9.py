###############################################################################
###############################################################################
# Main file for the entire project. The user needs to run this file in order ##
# to run the app. Uses 112 graphics and calls the other required files. #######
# Selenium is not compatible with 112 graphics, so everything that uses #######
# Selenium is separate. MyModalApp is the main function. There are three ######
# modes: HarmfulIngredientCheckerMode, productRecommenderMode, as well as #####
# splashScreenMode. ###########################################################
###############################################################################
###############################################################################

import module_manager
module_manager.review()
from harmfulIngredientFinderPortion_v4 import*
from productRecommenderPortion_v11 import *
from cmu_112_graphics import *
from emailFeature import *
import textwrap


#Harmful Ingredient Mode
class HarmfulIngredientCheckerMode(Mode):
    #Welcoming message 
    def appStarted(mode):
        mode.productName = ''
        mode.message = 'Welcome to Harmful Ingredient Finder. Click any key to begin.'
        mode.resultDictionary = None
        mode.returnResult = False 
        mode.cancel = False
        mode.returnString = ''
    
    
    def mousePressed(mode, event): 
        if mode.returnResult == True: 
            #User clicks 'return to home screen button'
            if (400 <= event.x <= 550) and (525 <= event.y <= 575): 
                mode.app.setActiveMode(mode.app.splashScreenMode)
                HarmfulIngredientCheckerMode.appStarted(mode)

            #User clicks 'email results' button 
            elif (100 <= event.x <= 250) and (525 <= event.y <= 575): 
                userEmail = mode.getUserInput('What is your email address?')
                subject = f'Harmful ingredients in {mode.productName}'
                body = mode.returnString 
                #Calls sendEmail function from emailFeature file 
                sendEmail(userEmail, subject, body)

        elif mode.cancel == True: 
            #User pressed cancel in input, so returns user back to home page
            if (400 <= event.x <= 650) and (500 <= event.y <= 600): 
                mode.app.setActiveMode(mode.app.splashScreenMode)
                HarmfulIngredientCheckerMode.appStarted(mode)

    def keyPressed(mode, event):
        productName = mode.getUserInput('What is the exact name and brand of the skincare product you want to find the harmful ingredients for?')
        if productName == None: 
            mode.message = 'You canceled'
            mode.cancel = True
        else: 
            mode.message = f'Finding harmful ingredients in {productName}' 
            mode.productName = productName
            if mode.resultDictionary == None: 
                mode.resultDictionary = harmfulIngredientProgram(productName)
                mode.returnResult = True
    
    def drawResult(mode, canvas): 
        
        #Sets up formatting of string into paragraphs 
        returnString = ''
        for item in mode.resultDictionary: 
            returnString += f'{item}: '
            returnString += f'{mode.resultDictionary[item]}'
        
        #Uses text wrapper to format string into a paragraph 
        wrapper = textwrap.TextWrapper(width = 95)
        string = wrapper.fill(text = returnString)
        mode.returnString = returnString

        #Draws result 
        canvas.create_text(mode.width/2, 450, text = "** Data compiled from CosDNA, The Never List, and safecosmetics.org **", 
                            fill = 'red', font = 'Helvetica 11 italic')
        canvas.create_text(mode.width/2, 100, text = 'Your product contains the following harmful ingredients:', 
                                                    font = 'Helvetica 20 bold')
        #There were no harmful ingredients in product
        if returnString == '': 
            canvas.create_text(mode.width/2, 250 , text = 'No harmful ingredients found!', 
                                                    font = 'Helvetica 16')
        #There are harmful ingredients in product                                            
        else: 
            canvas.create_text(mode.width/2, mode.height/2, text = f'{string}', 
                                                        font = 'Helvetica 14')
    #Draws return home button 
    def drawReturnHomeButton(mode, canvas):
        canvas.create_rectangle(400, 525, 550, 575, fill = 'black')
        canvas.create_text(475, 550, text = 'Return to home screen', fill = 'white')

    #Draws email button 
    def drawEmailButton(mode, canvas): 
        canvas.create_rectangle(100, 525, 250, 575, fill = 'black')
        canvas.create_text(175, 550, text = 'Email results', fill = 'white')
    
    #Redraw all 
    def redrawAll(mode, canvas):
        #Draws mode.message
        if mode.returnResult == False and mode.cancel == False: 
            font = 'Helvetica 14'
            canvas.create_text(mode.width/2, mode.height/2, text = mode.message, 
        
                                                            font = font)
        #Draws result
        elif mode.returnResult == True: 
            mode.drawResult(canvas)
            mode.drawReturnHomeButton(canvas)
            mode.drawEmailButton(canvas)

#Home Screen for app   
class SplashScreenMode(Mode):
    def drawHarmfulIngredientButton(mode, canvas): 
        canvas.create_rectangle(100, 300, 300, 450, fill = 'black')
        canvas.create_text(200, 375, text = 'Harmful Ingredient Finder', fill = 'white')

    def drawProductRecommenderButton(mode, canvas): 
        canvas.create_rectangle(400, 300, 600, 450, fill = 'black')
        canvas.create_text(500, 375, text = 'Product Recommender', fill = 'white')

    def mousePressed(mode, event): 
        if 100 <= event.x <= 300 and 300 <= event.y <= 450: 
            mode.app.setActiveMode(mode.app.harmfulIngredientCheckerMode)
        
        elif 400 <= event.x <= 600 and 300 <= event.y <= 450: 
            mode.app.setActiveMode(mode.app.productRecommenderMode)

    def redrawAll(mode, canvas):
        font = 'Helvetica 20'
        canvas.create_text(mode.width/2, 150, text = 'Welcome to skinBot! Click which mode you would like to interact with.', 
                                                    fill = 'black', font = font)
        mode.drawHarmfulIngredientButton(canvas)
        mode.drawProductRecommenderButton(canvas) 

#Overall App 
class MyModalApp(ModalApp): 
    def appStarted(app): 
        app.splashScreenMode = SplashScreenMode() 
        app.setActiveMode(app.splashScreenMode)
        app.harmfulIngredientCheckerMode = HarmfulIngredientCheckerMode()
        #Creates an instance of MyApp from productRecommenderPortion
        app.productRecommenderMode = MyApp() 

app = MyModalApp(width = 700, height = 600)