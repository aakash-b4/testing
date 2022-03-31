import datetime
purpose_list = ["SALARY_DISBURSEMENT","REIMBURSEMENT","BONUS","INCENTIVE","OTHERS"]
def generate_order_id(merchant_id):
    return "SAB"+str(datetime.datetime.now()).replace("-","").replace(" ","").replace(":","").replace(".","")+str(merchant_id)
