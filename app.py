# Importing essential libraries
from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load the regression model
model = joblib.load(open('model.pickle','rb'))
scaling = joblib.load(open('scaler.pickle','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    price = int(request.form['price'])
    seller_state = request.form['ss']
    payment = request.form['payment']
    payment_value = int(request.form['payvalue'])
    photos_count = int(request.form['photos'])
    customer_state = request.form['cs']
    product_category_name = request.form['pcn']
    delivery_days = int(request.form['dd'])
    estimated_days = int(request.form['ed'])
    arrival_time =  estimated_days - delivery_days
    arrival = ''
    delivery_impression = ''
    estimated_del_impression = ''
    existing = (request.form['y'])
    

    if (delivery_days >= 0 and delivery_days < 8 ):
        delivery_impression = 'Very_Fast'
    elif (delivery_days >= 8 and delivery_days < 16):
        delivery_impression = 'Fast'
    elif (delivery_days >= 16 and delivery_days < 25):
        delivery_impression = 'Neutral'
    elif (delivery_days >= 25 and delivery_days < 40):
        delivery_impression = 'Slow'
    elif (delivery_days >= 40 and delivery_days < 61):
        delivery_impression = 'Wrost'
    
    
    if (estimated_days >= 0 and estimated_days < 8 ):
        estimated_del_impression = 'Very_Fast'
    elif (estimated_days >= 8 and estimated_days < 16):
        estimated_del_impression = 'Fast'
    elif (estimated_days >= 16 and estimated_days < 25):
        estimated_del_impression = 'Neutral'
    elif (estimated_days >= 25 and estimated_days < 40):
        estimated_del_impression = 'Slow'
    elif (estimated_days >= 40 and estimated_days < 61):
        estimated_del_impression = 'Wrost'


    if (arrival_time > 0):
        arrival = 'Ontime'
    else:
        arrival = 'Late' 
  
    p = ['boleto', 'credit_card', 'debit_card', 'voucher']
    a = []
    for i in p:
        if i == payment:
            a.append(1)
        else:
            a.append(0)
    
    

    q =['AC', 'AL', 'AM','AP','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP','TO']
    b = []
    for i in q:
        if i == customer_state:
            b.append(1)
        else:
            b.append(0)
    

    r =['AM','BA','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RS','SC','SE','SP']
    c=[]
    for i in r:
        if i == seller_state:
            c.append(1)
        else:
            c.append(0)
    
    
    s = ['agro_industry_and_commerce','air_conditioning','art','arts_and_craftmanship','audio','auto','baby','bed_bath_table','books_general_interest','books_imported','books_technical','cds_dvds_musicals','christmas_supplies','cine_photo','computers','computers_accessories','consoles_games','construction_tools_construction','construction_tools_lights','construction_tools_safety','cool_stuff','costruction_tools_garden','costruction_tools_tools','diapers_and_hygiene','drinks','dvds_blu_ray','electronics','fashio_female_clothing','fashion_bags_accessories','fashion_childrens_clothes','fashion_male_clothing','fashion_shoes','fashion_sport','fashion_underwear_beach','fixed_telephony','flowers','food','food_drink','furniture_bedroom','furniture_decor','furniture_living_room','furniture_mattress_and_upholstery','garden_tools','health_beauty','home_appliances','home_appliances_2','home_comfort_2','home_confort','home_construction','housewares','industry_commerce_and_business','kitchen_dining_laundry_garden_furniture','la_cuisine','luggage_accessories','market_place','music','musical_instruments','office_furniture','other','party_supplies','perfumery','pet_shop','security_and_services','signaling_and_security','small_appliances','small_appliances_home_oven_and_coffee','sports_leisure','stationery','tablets_printing_image','telephony','toys','watches_gifts']
    d=[]
    for i in s:
        if i == product_category_name:
            d.append(1)
        else:
            d.append(0)
    

    t = ['Ontime','Late']
    e =[]
    for i in t:
        if i == arrival:
            e.append(1)
        else:
            e.append(0)
    

    u = ['Very_Fast','Fast','Neutral','Slow','Wrost']
    f = []
    for i in u:
        if i == delivery_impression:
            f.append(1)
        else:
            f.append(0)
    
    
    v = ['Very_Fast','Fast','Neutral','Slow','Wrost']
    g = []
    for i in v:
        if i == estimated_del_impression:
            g.append(1)
        else:
            g.append(0)
    

    w= ['yes','no']
    h = []
    for i in w:
        if i == existing:
            h.append(1)
        else:
            h.append(0)
    

    arr = [[price,payment_value,photos_count,delivery_days,estimated_days]]
    z = scaling.transform(arr)

    import functools
    import operator

    
    z = functools.reduce(operator.concat, z)
    price = [z[0]]  
    payment_value = [z[1]]
    photos_count = [z[2]]
    delivery_days = [z[3]] 
    estimated_days = [z[4]]
    


    data = [price + payment_value + photos_count + delivery_days + estimated_days + a + b + c + d + e + f + g + h]
  

    price = int(request.form['price'])
    seller_state = request.form['ss']
    payment = request.form['payment']
    payment_value = int(request.form['payvalue'])
    photos_count = int(request.form['photos'])
    customer_state = request.form['cs']
    product_category_name = request.form['pcn']
    delivery_days = int(request.form['dd'])
    estimated_days = int(request.form['ed'])
    arrival_time =  estimated_days - delivery_days
    arrival = ''
    delivery_impression = ''
    estimated_del_impression = ''
    existing = (request.form['y'])
    

    if (price == 0 or seller_state ==0 or payment == 0 or payment_value == 0 or photos_count ==0 or customer_state == 0 or product_category_name == 0 or delivery_days ==0 or estimated_days == 0):
        my_prediction = [0]
    else:
        my_prediction = model.predict(data)

    if (my_prediction == 1):
        prediction = 'Satisfied'
    else:
        prediction = 'Not Satisfied'

    return render_template('index.html', prediction_text='Customer {}'.format(prediction))

if __name__ == "__main__":
    app.run(debug=True)