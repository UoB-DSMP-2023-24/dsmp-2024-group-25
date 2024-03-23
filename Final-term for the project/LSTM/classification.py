import pandas as pd

bank = ['Halifax', 'LBG']
ie = ['Blizzard', 'Xbox', 'Mojang Studios', 'SquareOnix', 'Disney', 'Netflix', 'Gamestation', 'CeX', 'HMV', "Blackwell's", 'Foyles', 'Collector Cave']
fc = ['Fat Face', 'Topshop', 'Matalan', 'North Face', 'Reebok', 'JD Sports', 'Barbiee Boutique', 'Revella', 'Loosely Fitted', 'Sports Direct', 'Mountain Warehouse', 'Millets']
kids = ['Gap Kids', 'Mamas & Papas', 'Mothercare', 'Lavender Primary', 'Happy Days Home', 'Kew House']
art_craft = ['Stitch By Stitch', 'Hobbycraft', 'A Yarn Story', 'Craftastic', 'Cass Art', 'Brilliant Brushes','Wool', 'Fitted Stitch', 'Five Senses Art']
grocery = ['Coop Local', 'Sainsbury', 'Tesco', 'Sainsbury Local']
daily_life = ['A Cut Above', 'PureGym', 'Grand Union BJJ', 'RugbyFields', 'Pets Corner', 'Town High', 'Head']
retailer_for_all = ['Selfridges', 'The Works', 'Hobby Lobby', 'Etsy', 'Amazon', 'AMAZON']
med = ['Boots', 'Lloyds Pharmacy', 'Remedy plus care', 'Specsavers', 'Vision Express', 'University College Hospital']
fd = ['Coffee #1', 'Starbucks', 'Costa Coffee', 'The Crown', 'Kings Arms', 'Rose & Crown', 'Frankie & Bennies', 'Deliveroo', 'JustEat', 'Victoria Park']

def replace_account_names(name, a, b, c, d, e, f, g, h, i, j):
    
    if name in a:
        return 'Bank'
    
    elif name in b:
        return 'Indoor Entertainment'
    
    elif name in c:
        return 'Fashion & Clothing'
    
    elif name in d:
        return 'Kids'
    
    elif name in e:
        return 'Arts & Craft'
    
    elif name in f:
        return 'Grocery'
    
    elif name in g:
        return 'Daily'
    
    elif name in h:
        return 'Large Retailers'
    
    elif name in i:
        return 'Medical'
    
    elif name in j:
        return 'Food & Drink'

    else:
        return name
    
def classify_third_party(data):
    bank = ['Halifax', 'LBG']
    ie = ['Blizzard', 'Xbox', 'Mojang Studios', 'SquareOnix', 'Disney', 'Netflix', 'Gamestation', 'CeX', 'HMV', "Blackwell's", 'Foyles', 'Collector Cave']
    fc = ['Fat Face', 'Topshop', 'Matalan', 'North Face', 'Reebok', 'JD Sports', 'Barbiee Boutique', 'Revella', 'Loosely Fitted', 'Sports Direct', 'Mountain Warehouse', 'Millets']
    kids = ['Gap Kids', 'Mamas & Papas', 'Mothercare', 'Lavender Primary', 'Happy Days Home', 'Kew House']
    art_craft = ['Stitch By Stitch', 'Hobbycraft', 'A Yarn Story', 'Craftastic', 'Cass Art', 'Brilliant Brushes','Wool', 'Fitted Stitch', 'Five Senses Art']
    grocery = ['Coop Local', 'Sainsbury', 'Tesco', 'Sainsbury Local']
    daily_life = ['A Cut Above', 'PureGym', 'Grand Union BJJ', 'RugbyFields', 'Pets Corner', 'Town High', 'Head']
    retailer_for_all = ['Selfridges', 'The Works', 'Hobby Lobby', 'Etsy', 'Amazon', 'AMAZON']
    med = ['Boots', 'Lloyds Pharmacy', 'Remedy plus care', 'Specsavers', 'Vision Express', 'University College Hospital']
    fd = ['Coffee #1', 'Starbucks', 'Costa Coffee', 'The Crown', 'Kings Arms', 'Rose & Crown', 'Frankie & Bennies', 'Deliveroo', 'JustEat', 'Victoria Park']
    
    data['Third Party Name'] = data['Third Party Name'].apply(lambda x: replace_account_names(x, bank, ie, fc, kids, art_craft, grocery, daily_life, retailer_for_all, med, fd))
    return data



