# Shop collection functions

test_item_for_reference = {
    "Item Name": {
        "price": 1,
        "currency": "gp",
        "margin": 1,
        "max": 3,
        "category": "Home Goods"
    }
}

# Constants
com = combat()
using(baglib="4119d62e-6a98-4153-bea9-0a99bb36da2c")
node = "shop"
channel_id = str(ctx.channel.id)
a_shop = dict
a_log = dict
an_item = dict

default_settings = {
    "shopkeeper_role": "Shopkeeper",
    "default_bag": "Shopping Bag"
}

settings = load_json(get_svar("shops", dump_json(default_settings)))
item_reference = load_json(get_svar("shop_items", "[]"))

# Helpers
def build_embed(embed_str: str) -> str:
    """
    Builds the output embed for all the shop aliases
    :embed_str: The embed string
    :return: The concatenated embed string
    :rtype: str
    """
    return f'''embed {embed_str} -footer "{ctx.prefix}{ctx.alias} v1.0 | Created by Corvux"'''

def new_shop(shop_name: str, 
             **kwargs) -> a_shop:
    """
    Creates a new shop object
    :shop_name: The shop's name
    :return: New shop
    :rtype: a_shop
    """
    return {
        "name": shop_name,
        "owner": ctx.author.id,
        "margin": int(kwargs.get('margin', 1)),
        "buy": kwargs.get('buy', True),
        "inventory": {},
        "logs": []
    }

def get_shop() -> a_shop:
    """
    Builds the output embed for all the shop aliases
    :embed_str: The embed string
    :return: The concatenated embed string
    :rtype: str
    """
    return load_json(com.get_metadata(node, "{}"))

def update_shop(shop: a_shop) -> None:
    com.set_metadata(node, dump_json(shop))

def close_shop() -> None:
    com.delete_metadata(node)

def is_owner() -> bool:
    shop = get_shop()
    return ctx.author.id == shop.get('owner')

def get_item(name: str, create_item: bool = False, **kwargs) -> an_item:
    shop = get_shop()

    if item := shop["inventory"].get(name):
        return item
    elif create_item == False:
        return
    else:
        item = {
            "name": name,
            "quantity": kwargs.get('quantity', 1),
            "price": kwargs.get('price', 1),
            "currency": kwargs.get('currency', 'gp'),
            "category": kwargs.get('category'),
            "image_url": kwargs.get('image_url')
        }

        if kwargs.get('margin'):
            item["margin"] = kwargs.get('margin')

        return item

def modify_inventory(item: an_item) -> (bool, an_item):
    shop = get_shop()
    # Remove empty items
    if shop["inventory"].get(item.get('name')) and item.get('quantity') == 0:
        shop["inventory"].pop(item.get('name'))
    # Trying to add an empty item
    elif item.get('quantity') == 0:
        return False, "Can't add an empty item"
    # Update/add an item
    else:
        shop["inventory"][item.get('name')] = item

    update_shop(shop)

    return True, item

def is_manager() -> bool:
    shop = get_shop()
    user_roles = [r.name for r in ctx.author.get_roles()]

    return is_owner() or settings.get('shopkeeper_role') in user_roles

def build_inventory_list():
    shop = get_shop()
    categories = {'General': []}
    desc = "```"
    divider = '---------------'

    for item_name, item_data in shop["inventory"].items():
        if category := item_data.get('category'):
            if not categories.get(category):
                categories[category] = []

            categories[category].append(item_data)
        else:
            categories['General'].append(item_data)
    
    for category, items in categories.items():
        if items:
            items.sort(key=lambda p: p.get('name'))
            item_string = "\n".join(f"{item.get('name'):<26}{item.get('price'):>8,}{item.get('currency'):<4}  {item.get('quantity'):>6,}" for item in items)
            desc += f'''\n{category}\n{divider}\n{item_string}\n{divider}\n'''
    
    desc += "```"

    return desc



def _create_log(type: str, 
                item: an_item, 
                quantity: int, 
                cost: int, 
                ) -> a_log:
    shop = get_shop()
    log = {
        "type": type,
        "item": item.get('name'),
        "cost": cost,
        "quantity": quantity,
        "currency": item.get('currency'),
        "timestamp": int(time()),
        "char": character().name,
        "user_id": ctx.author.id
    }

    shop["logs"].append(log)
    update_shop(shop)

    return log



def buy_item(item, quantity, **kwargs):
    bagsLoaded = baglib.load_bags()

    if item.get('quantity') < quantity:
        return False, "Not enough items in stock"

    cost = item.get('price') * quantity

    c, error = baglib.modify_coins(bagsLoaded, item.get('currency'), -cost)

    if error:
        return False, "You do not have enough coins."   
    
    bagname = kwargs.get('bagname')
    if not bagname or bagname == 'None':
        bagname = settings.get('default_bag')

    baglib.get_bag(bagsLoaded, bagname, True, True)

    baglib.modify_item(bagsLoaded, item.get('name'), quantity, bagname, True)

    item['quantity']-=quantity

    modify_inventory(item)

    baglib.save_bags(bagsLoaded)

    log = _create_log("buy", item, quantity, cost)

    # For output validation
    log['bag'] = bagname

    return True, log

def sell_item(item_name, quantity):
    shop = get_shop()
    bagsLoaded = baglib.load_bags()
    ref_item = None
    item = None

    for g in item_reference:
        items = load_json(get_gvar(g))

        if ref_item := items.get(item_name):
            break

    if not ref_item:
        return False, "Item not found", None
    elif ref_item.get('buy', True) == False or shop.get('buy', True) == False:
        return False, "The shopkeeper refuses to buy the item.", None
    
    cost = (ref_item.get('price') * float(ref_item.get('margin', shop.get('margin', 1)))) * quantity
    c, error = baglib.modify_coins(bagsLoaded, ref_item.get('currency'), cost) 

    if error:
        return False, "Why can't I give you my money?", None
    
    if item := get_item(item_name):
        item["quantity"] += quantity
    else:
        item = get_item(item_name, True,
                        quantity=quantity,
                        price=ref_item.get('price',1),
                        currency=ref_item.get('currency',"gp"),
                        category=ref_item.get('category'),
                        image_url=ref_item.get('image_url'))
        
        if ref_item.get('margin'):
            item["margin"] = ref_item.get('margin')

    bag, l, success = baglib.modify_item(bagsLoaded, item.get('name'), -quantity, None, False, True)
    modify_inventory(item) 
    baglib.save_bags(bagsLoaded)
    ref_item["name"] = item_name

    log = _create_log("sell", ref_item, quantity, cost)

    log["bag"] = bag[0] if bag else ""

    return True, log, ref_item


def randomize_inventory(num_items: int):
    items = {}

    for g in item_reference:
        ref_items = load_json(get_gvar(g))

        for item_name, item_data in ref_items.items():
            if item_data.get('in_shop', True) != False:
                items[item_name] = item_data

    item_list = list(items.items())
    if num_items:
        num_items = min(num_items, 100) # Ensure we have a cap
        loaded_items = 0
        output = {}

        while loaded_items < num_items and item_list:
            index = roll(f"1d{len(item_list)}-1")
            item_name, item_data = item_list[index]
            if not (item := get_item(item_name)):
                item = get_item(item_name, True,
                                quantity=0,
                                price=item_data.get('price',1),
                                currency=item_data.get('currency',"gp"),
                                category=item_data.get('category'),
                                image_url=item_data.get('image_url')
                                )

            if item_data.get('max') and item.get('quantity')+1 > item_data.get('max'):
                item_list.pop(index)
                continue

            item["quantity"] += 1
            loaded_items+=1
            if item_name in output:
                output[item_name] += 1
            else:
                output[item_name] = 1

            modify_inventory(item)

    return output