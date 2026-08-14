import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from time import sleep

# Load environment variables
load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

# Define model and message
model_name = "llama-3.3-70b-versatile"

Iphone_Status="""
ChatGPT said:
Got it. You want plain detailed information, written naturally, so you can give that information to your AI—not a prompt, not instructions for the AI.

Apple iPhone 16 — Detailed Information
The Apple iPhone 16 is a premium smartphone launched by Apple in September 2024. In India, the iPhone 16 was launched with three storage options: 128GB, 256GB, and 512GB. The starting price of the 128GB model was ₹79,900.

The iPhone 16 has a 6.1-inch Super Retina XDR OLED display with a resolution of 2556 × 1179 pixels. It uses Apple's A18 chip, which is designed for high performance and supports Apple's newer AI features. The phone has a dual-camera system on the back consisting of a 48MP Fusion main camera and a 12MP Ultra Wide camera. It also has a 12MP TrueDepth front camera.

The iPhone 16 uses a USB-C port for charging and data transfer and supports MagSafe wireless charging. It has an IP68 water and dust resistance rating. The phone weighs approximately 170 grams and was released in Black, White, Pink, Teal, and Ultramarine colours.

iPhone 16 India launch prices
The original India prices were:

128GB — ₹79,900
256GB — ₹89,900
512GB — ₹1,09,900
The 128GB model is particularly important for price prediction because it has frequently been the model used for the largest promotional discounts and is one of the most commonly purchased configurations.

iPhone 16 Price History in India
After its September 2024 launch, the iPhone 16 initially remained close to its official ₹79,900 starting price. During the 2024 festive-sales period, including Flipkart's Big Billion Days, the price started falling and the 128GB model was seen around the ₹75,000–₹76,000 range, depending on the exact offer and payment method.

By early 2025, the iPhone 16 had received significantly larger discounts. During Republic Day and other early-2025 sales, the 128GB model was available around the ₹64,000 range in some promotions.

During the middle of 2025, the price generally moved into the ₹55,000–₹65,000 range during major retailer promotions. The exact price depended on the retailer, sale period, bank discount, exchange offer and stock availability.

During the Independence Day sales in August 2025, the iPhone 16 128GB was reported at approximately ₹69,999, with additional bank discounts capable of reducing the effective purchase price further.

The most important historical event for predicting Big Billion Days pricing was Flipkart Big Billion Days 2025. During this sale, the iPhone 16 128GB was offered at approximately ₹51,999. Additional eligible bank discounts could reduce the effective price to around ₹50,999, while some customers reported prices around the ₹49,000–₹52,000 range after combining eligible offers and cashback.

This makes approximately ₹52,000 a very important historical benchmark for iPhone 16 128GB during a major Big Billion Days sale.

Later in 2025, the iPhone 16 generally remained in the ₹50,000–₹60,000 range during different promotional periods. Some exceptional promotions were significantly lower. For example, a December 2025 Croma promotion was reported at approximately ₹40,990. This should be considered an exceptional promotional price rather than the standard market price because such prices can depend on limited stock, payment offers and other conditions.

By 2026, the iPhone 16 had become an older generation because newer iPhone models had entered the market. Its price therefore became increasingly dependent on retailer inventory, upcoming sales and competition between retailers.

As of August 12, 2026, the iPhone 16 128GB has been listed on Flipkart at approximately ₹66,900, with an effective price around ₹61,655 after displayed applicable offers. This is the current reference price and should not be confused with a confirmed Big Billion Days price.

Overall historical range
For the iPhone 16 128GB, the observed price movement can broadly be represented as:

Launch: ₹79,900
2024 festive sales: ~₹75,000–₹76,000
Early 2025 sales: ~₹64,000
Mid-2025 sales: ~₹55,000–₹65,000
Independence Day 2025: ~₹69,999 before additional offers
BBD 2025: ₹51,999
BBD 2025 after eligible offers: roughly ₹49,000–₹51,000
Exceptional late-2025 promotion: ~₹40,990
Current August 2026 Flipkart price: ~₹66,900
Current effective offer price: ~₹61,655

The ₹40,990 price should be treated as an exceptional low, while the ₹51,999 BBD 2025 price is a more useful benchmark for predicting another Big Billion Days sale.

For price prediction, the difference between the normal selling price and the effective price after bank offers/cashback/exchange is important. A phone advertised at ₹51,999 may have a lower final cost for a customer who has an eligible credit card, cashback or exchange offer. Therefore, historical prices should not all be treated as directly equivalent.

The iPhone 16's price has generally followed a downward trend as the product has aged, but individual sale prices can temporarily move higher or lower because of stock levels, retailer competition, bank promotions and major shopping events.

iPhone 16 128GB vs 256GB PRICE DATA

128GB:

India Launch Price:
₹79,900

Launch Date:
September 2024

2024 Festive/BBD:
Approximately ₹75,000–₹76,000 in reported promotional pricing.

Early 2025:
Approximately ₹64,000 during some major promotions.

June 2025:
₹69,999 on Flipkart without requiring a bank offer or exchange.

August 2025:
Approximately ₹69,999 during Independence Day promotions, with additional eligible offers potentially reducing the effective price.

Flipkart Big Billion Days 2025:
₹52,999 listed sale price.
₹51,999 effective sale price for the reported BBD offer.
Additional eligible ICICI/Axis credit-card discount could reduce the price by another ₹1,000.
Some customers reported effective prices around ₹49,000–₹52,000 depending on applicable offers and cashback.

Late 2025:
Approximately ₹54,999 during Flipkart Big Bang Diwali Sale.

Exceptional December 2025 promotion:
Approximately ₹40,990 was reported at Croma.
This should be classified as an exceptional promotional price rather than the normal market price.

Current August 2026 reference:
Approximately ₹66,900 listed price on Flipkart.
Approximately ₹61,655 after displayed applicable offers.

256GB:

India Launch Price:
₹89,900

Launch Date:
September 2024

Difference from 128GB at launch:
₹10,000

2024:
The 256GB version was generally priced above the 128GB version.
Exact promotional prices should be recorded only when the storage variant is explicitly confirmed.

2025:
The 256GB model continued to carry a higher price than the 128GB model.
The 128GB model received the strongest and most frequently reported BBD promotional pricing.

June 2025:
The 128GB model was confirmed at ₹69,999 on Flipkart.
Do NOT use ₹69,999 as the 256GB price because the source specifically identifies the 128GB variant.

BBD 2025:
The confirmed ₹51,999 BBD price applies to the 128GB model.
A reliable 256GB BBD 2025 price should NOT be assumed without a source explicitly identifying the 256GB variant.
Mark the 256GB BBD 2025 value as "not confirmed" rather than guessing.

Current 2026 Flipkart observations:
256GB listings have been observed around ₹77,900–₹79,900 before applicable offers.
One Flipkart listing showed ₹79,900 with an offer price around ₹75,905.
Another listing showed ₹77,900 after a direct reduction from ₹79,900, with additional bank offers.

July 2026:
A Gadgets Now comparison listed the iPhone 16 256GB at approximately ₹73,900.

IMPORTANT COMPARISON:

128GB launch price:
₹79,900

256GB launch price:
₹89,900

Launch price difference:
₹10,000

The 256GB version does not have better processor, camera, display, battery or performance than the 128GB version.
The primary hardware difference is storage capacity.

128GB is better for:
Users who use cloud storage.
Users who do not store large amounts of 4K video.
Users who want the lowest possible iPhone 16 price.
Users whose main goal is getting the best BBD deal.

256GB is better for:
Users who record large amounts of 4K video.
Users who store many photos and videos locally.
Users who play large games.
Users who plan to keep the phone for several years.
Users who do not want to depend heavily on iCloud or other cloud storage.

PRICE-PREDICTION RELATIONSHIP:

The 256GB model should not simply be predicted as:

128GB predicted price + ₹10,000

because discounts can be different for each storage variant.

The model should learn the historical discount percentage separately.

Example:

128GB:
Launch = ₹79,900
BBD price = ₹51,999
Discount = approximately 34.96%

256GB:
Launch = ₹89,900
BBD price = unknown/not reliably confirmed

Therefore, the model should not invent a historical BBD 2025 price for the 256GB model.

The model should use:
256GB launch price
256GB current price
256GB observed sale prices
256GB retailer discounts
256GB bank offers
256GB inventory
256GB historical discount percentage
and compare these with the 128GB price trend.

CURRENT VALUE COMPARISON:

128GB:
Lower purchase price.
Best choice for saving money.
More likely to receive aggressive promotional pricing.
Better choice when the primary objective is the lowest BBD price.

256GB:
Costs more.
Provides twice the storage.
Better for heavy storage users.
More attractive if the BBD discount reduces the price difference between 128GB and 256GB.

IMPORTANT:
The price difference between 128GB and 256GB should be monitored during BBD.

If:
256GB price - 128GB price <= ₹5,000

then 256GB becomes significantly more attractive because the buyer receives double the storage for a relatively small additional cost.

If:
256GB price - 128GB price >= ₹10,000

then 128GB generally provides better value for users who do not require additional storage.

If:
256GB price - 128GB price >= ₹15,000

then 128GB is generally the better value choice unless the buyer specifically needs 256GB storage.




"""

def llm(systemprompt,prompt):
   systemMessage={
       "role":"system",
       "content":systemprompt
   }
   userMessage={
       "role":"user",
       "content":prompt

   }
   messages=[systemMessage,userMessage]
   response = client.chat.completions.create(
    model=model_name,
    messages=messages,
  
)
   answer=response.choices[0].message.content
   return answer

def first(Iphone_Status):
    systemprompt=f"""
You are an profesnnal phone expert .Extract an tell me the detail of the iphone that is been given.
you have to only return the phone and it specs that is required to be known by an buyer and performance and camer detail
and also tell me why should i buy this in current year
Output:
The output should be first about Iphone 
Then it specs
Then compare why should i buy this
"""
    userprompt=f"""
 Extract the details of the phone from here {Iphone_Status}
"""
    return llm(systemprompt,userprompt)

def second(Iphone_Status):
    systemprompt=f"""
Your are an expert sales working in flipkart/Amazon now your task is to extract the price of the iphone from all the sales
that is been provided

Output:
the output should be which time and the price

"""
    userprompt=f"""
extract the price from here {Iphone_Status}
"""
    return llm(systemprompt,userprompt)

def third(IphoneStaus):
    systemprompt=f"""
You are an expert sales prediction that predict according to previous data Your task is to get the detail of iphone price{Iphone_Status}
and predict the price in 2026 bigbillion day price of iphone and also make comparison for both 128gb and 256gb also tell which to buy should be good

Output:
Just print the price of iphone in this bigbillion day
Also print the prediction precentage
Then print the comparison
Give one clear winner which to buy
"""
    userprompt=f"""
from the previous price{IphoneStaus} predict the price of iphone in this bigbillion day 2026
"""
    return llm(systemprompt,userprompt)

Iphone=first(Iphone_Status)
print(Iphone)
sleep(3)
pricehistory=second(Iphone_Status)
sleep(2)
prediction=third(Iphone_Status)
print(prediction)

