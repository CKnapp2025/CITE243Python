import time   

indent = 5             
indentIncreasing = True 

while True:             
    print(" " * indent + "=======Hello World!=======")  
    time.sleep(0.05)     

    if indentIncreasing:   
        indent += 1
        if indent == 20:   
            indentIncreasing = False
    else:                  
        indent -= 1
        if indent == 0:    
            indentIncreasing = True
