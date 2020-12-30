# skinBot
Individual Final Term Project for 15-112. Uses Selenium and a simple Python AI to find harmful ingredients in a project and return product recommendations for a user.
skinBot by Laura Canseco (lcanseco)

Description: 

skinBot is a program in which the user is able to find harmful chemicals
in their skin care products, as well as receive skincare product 
recommendations. It returnsdetails about the recommended products' price, 
rating, and brand. Lastly, users can see graphs related to their recommended 
products. 

How to Run: 

In order to run skinBot, the user must run the file GraphicsPortion_v8. However, 
the folder that contains GraphicsPortion_v8 must also have 
harmfulIngredientFinderPortion_v3.py, productRecommenderPortion_v11, 
emailFeature, moduleManager, cmu112graphics, as well as the related image files 
that productRecommenderPortion_v11 uses. In order to run the program, the user
should run GraphicsPortion_v8. The user does not need to open the other files 
-- those files only need to be in the same folder as GraphicsPortion_v8. 

Libraries: 
pip install selenium 

In each file, this is what is imported: 

harmfulIngredientFinderPortion_v3 imports: 
import module_manager
module_manager.review()
from selenium import webdriver
import tkinter 
 
productRecomenderPortion_v11 imports: 
from cmu_112_graphics import *
from productSelenium_v2 import*

graphicsPortion_v8 imports: 
import module_manager
module_manager.review()
from harmfulIngredientFinderPortion_v3 import*
from productRecommenderPortion_v11 import *
from cmu_112_graphics import *
from emailFeature import *
import textwrap

productSelenium_v2 imports: 
import module_manager
module_manager.review()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter 
import random

There are no "shortcut commands" to skip features. 


