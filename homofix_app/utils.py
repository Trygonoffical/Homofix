import uuid
orider_id = 000
expert_num = 23001
support_num = 23001
def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:4]
    return code

def generate_order_code():
    global orider_id
    code = "HF-" + str(orider_id)
    orider_id += 1
    
    return code
def generate_expert_code():
    global expert_num
    code = "HE-" + str(expert_num)
    expert_num += 1
    
    return code

def generate_support_code():
    global support_num
    code = "HS-" + str(support_num)
    support_num += 1
    
    return code

 
