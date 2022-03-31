def calulate_tax_exclusive(number,percentage):
    tax=(number/100)*percentage
    return tax
def calulate_base(number,percentage):
    base=(100*number)/(100+percentage)
    return base