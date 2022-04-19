from datetime import datetime
from .models import Order
import datetime

class OrderServices():
    def __init__(self):
        pass

    @staticmethod
    def stock_by_date(p_date,quantity_items):
        total_quantity=0
        queryset = Order.objects.filter(date_delivery=p_date)        
        # total = sum([item.orderitem_set.all() for item in queryset])
        queryset_total_order = [order.orderitem_set.all() for order in queryset]
        # print(queryset_total_order)
        # total_items = sum([item.id for item in queryset_total_orderitem])
        
        for order_items in queryset_total_order:
            
            # print(order_items )
            for items in order_items:
                total_quantity+=items.quantity
        #validando si la fecha esta superando el stock o es un dia domingo 
        if (total_quantity+quantity_items)>6 or p_date.strftime('%A')=='Sunday':
            return p_date


    @staticmethod
    def disabled_dates(quantity_items):
        invalid_dates=[]
        disabled_sundays=[]
        today = datetime.date.today()
        #calculando 3 dias despues de hoy hasta pasando 14 dias despues del 3er dia
        to_date=(today + datetime.timedelta(days=3)).strftime("%x")
        from_date=(today + datetime.timedelta(days=17)).strftime("%x")
        #calculando los dias desabilitados
        full_stock_dates = [OrderServices.stock_by_date((today + datetime.timedelta(days=i)),quantity_items) for i in range(3, 17)]
        for val in full_stock_dates:
            if val != None:
                if val.strftime('%A')=='Sunday':
                    val_string = val.strftime("%x")
                    disabled_sundays.append(val_string)
                else:
                    string_date = val.strftime("%x")
                    invalid_dates.append(string_date)
        return invalid_dates,disabled_sundays,to_date,from_date
    
