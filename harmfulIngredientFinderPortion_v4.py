###############################################################################
###############################################################################
# harmfulIngredientFinderPortion_v3 uses selenium to find the ingredients in  #
# a given product. Then, within that product, it uses dictionaries to return  #
# find the harmful ingredients within that list. It returns the harmful       #
# ingredients, as well as their definitions. ##################################
###############################################################################
###############################################################################

import module_manager
module_manager.review()
from selenium import webdriver
import tkinter 
 
#Runs program 
def harmfulIngredientProgram(productName):
    driver = webdriver.Chrome('/Users/lauracanseco/Desktop/chromedriver') 
    productIngredients = findProductIngredients(driver, productName)
    findHarmfulIngredients(productIngredients)
    productHarmfulIngredients, productHarmfulIngredientTypes = findHarmfulIngredients(productIngredients)
    harmfulIngredientDefinitions = harmfulIngredientExplanations(productHarmfulIngredientTypes) 
    return(harmfulIngredientDefinitions)
    
#For a given product, finds ingredients in that product 
def findProductIngredients(driver, productName): 
    url = 'www.cosdna.com'
    driver.get("https://" + url) 
    productIngredients = []
    
    #Types in product name
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/form/input').send_keys(productName)
    
    #Clicks search button
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div[1]/form/button').click()
    driver.implicitly_wait(10)  
    
    #Clicks on first result for product
    driver.find_element_by_xpath('/html/body/div[1]/main/div/div[2]/div[1]/table/tbody/tr[1]/td[2]/a').click()
    driver.implicitly_wait(10)
    
    #Checks if harmful ingredient indicator is on the page for a product
    elements = driver.find_elements_by_class_name('colors')
    for element in elements: 
        html = element.get_attribute('innerHTML') #Finds name of ingredient 
        productIngredients.append(html)
    return(productIngredients)


#Harmful ingredients compiled from several resources: 
#https://www.beautycounter.com/the-never-list, http://www.safecosmetics.org
# Will cite in display  
#Finds harmful ingredients in a list of ingredients
def findHarmfulIngredients(productIngredients): 
    productHarmfulIngredients = set()
    productHarmfulIngredientTypes = set()
    harmfulIngredients = {'benzalkonium chloride': {'benzalkonium chloride'},
    'butylated': {'butylatedhydroxy anisole', 'butylated hydroxytoluene'}, 
    'ethylenediaminetetraacetic acid': {'ethylenediaminetetraacetic acid'}, 
    'formaldehyde': {'formaldehyde'}, 'hydroquinone': {'hydroquinone'}, 
    'methylisothiazolinone': {'methylisothiazolinone', 
    'methylchloroisothiazolinone'}, 'oxybenzone': {'oxybenzone'}, 
    'retinyl palmitate': {'retinyl palmitate'}, 'SL': {'sodium lauryl sulfate', 
    'sodium laureth sulfate'}, 'toluene': {'toluene'}, 'triclosan': 
    {'triclosan', 'triclocarban'}, 'ethanolamines': {'triethanolamine', 
    'diethanolamine','dea-cetyl phosphate','dea oleth-3 phosphate', 
    'lauramide dea','linoleamide mea', 'myristamide dea', 'oleamide dea', 
    'stearamide mea', 'tea-lauryl sulfate'}, 'parabens': {'ethylparaben', 
    'butylparaben','isobutylparaben', 'isopropylparaben', 'methylparaben', 
    'propylparaben'}, 'phthalates': {'phthalate', 'diethyl phthalate', 
    'dibutyl phthalate', 'dehp','dep', 'dbp'}, 'PEG': {'polyethylene glycol', 
    'peg-4', 'peg-100', 'propylene glycol', 'butylene glycol'}}
    for product in productIngredients: 
        product = product.lower()
        for typeOfIngredient in harmfulIngredients: 
            if product in harmfulIngredients[typeOfIngredient]: 
                productHarmfulIngredients.add(product)
                productHarmfulIngredientTypes.add(typeOfIngredient)
    return(productHarmfulIngredients, productHarmfulIngredientTypes) 
 
#Explanations from https://www.beautycounter.com/the-never-list, will formally 
#Will cite in display to inform users of where this informaton comes from 
#Returns the explanations of given harmful ingredients
def harmfulIngredientExplanations(productHarmfulIngredientTypes): 
    harmfulIngredientDefinitions = dict()
    harmfulIngredientToDefinition = {'benzalkonium chloride': "A disinfectant" + 
    " used as a preservative and surfactant.", 'butylated': "Synthetic" + 
    " antioxidants used to extend shelf life. Most likely carnicogens" + 
    " carcinogens and hormone disruptors and may cause liver damage.", 
    ' ethylenediaminetetraacetic acid': "A chelating (binding) agent added to" + 
    " cosmetics to improve stability. May be toxic to organs",  'formaldehyde': 
    " Used as a preservative in cosmetics. A known carcinogen that is also" + 
    " linked to asthma, neurotoxicity, and developmental toxicity.", 
    ' hydroquinone': "A skin-lightening chemical that inhibits the production" +
    " of melanin and is linked to cancer, organ toxicity, and skin irritation.",
    ' methylisothiazolinone': "Chemical preservatives that are among the most" +
    " common irritants, sensitizers, and causes of contact skin allergies.", 
    ' oxybenzone': "Sunscreen agent and ultraviolet light absorber linked to" +
    " irritation, sensitization and allergies, and possible hormone disruption.", 
    'parabens': "A class of preservatives commonly used to prevent the growth" +
    " of bacteria and mold. Parabens are endocrine (or hormone) disruptors" +
    ", which may alter important hormone mechanisms in our bodies.", 
    'phthalates': "A class of plasticizing chemicals used to make products" +
    " more pliable or to make fragrances stick to skin. Phthalates disrupt the" + 
    " endocrine system and may cause birth defects.", 'PEG': "PEGs are widely" +
    " used in cosmetics as thickeners, solvents, softeners, and" + 
    " moisture-carriers. Depending on manufacturing processes, PEGs may be" + 
    " contaminated with measurable amounts of ethylene oxide and 1,4-dioxane," +
    "which are both carcinogens.", 'retinyl palmitate': "Retinyl palmitate is" + 
    " an ingredient composed of palmitic acid and retinol (Vitamin A). Data" + 
    " from an FDA study indicate that retinyl palmitate, when applied to the" + 
    " skin in the presence of sunlight, may result in adverse health" + 
    " consequences like lesions and photosensitization.", 'SL': "SLS and SLES" + 
    " are surfactants that can cause skin irritation or trigger allergies.", 
    'toluene': "A volatile petrochemical solvent that is toxic to the immune" + 
    " system and can cause birth defects.", 'triclosan': "Antimicrobial" + 
    " pesticides toxic to the aquatic environment; may also impact human" + 
    " reproductive systems.", 'ethanolamines': "Surfactants and pH adjuster" + 
    " linked to allergies, skin toxicity, hormone disruption, and inhibited"
    + " fetal brain development."}
    for product in productHarmfulIngredientTypes: 
        for typeOfIngredient in harmfulIngredientToDefinition: 
            if product == typeOfIngredient: 
                harmfulIngredientDefinitions[product] = harmfulIngredientToDefinition[typeOfIngredient]
    return(harmfulIngredientDefinitions)
