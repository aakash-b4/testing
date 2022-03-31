from typing_extensions import final


def get_number(type,number,charge_number=0):
        final_number=0
        if(type=="percentage"):
            final_number=(float(charge_number)/100)*float(number)
            return final_number
        elif (type=="fix"):
            print(number)
            return charge_number
        else:
            return 0