import numpy as np

def roundup(x,r=2):
        a = x*10**r
        a = np.ceil(a)
        a = a*10**(-r)

        if type(x) == float or type(x) == int or type(x) == np.float64:
            if a == 0 :
                a=10**(-r)
        else:
            try:                                           # rundet mehrdimensionale arrays
                for i,j in enumerate(a):
                    for k,l in enumerate(j):
                        if i == 0:  
                            i=10**(-r)
            except:                                        # rundet eindimensionale arrays
                for i,j in enumerate(a):
                    if i == 0:  
                        i=10**(-r)
                    
        return np.around(a,r)

def varianz_xy(x,x_mean,y,y_mean):
        return (1/len(x))*((x-x_mean)*(y-y_mean)).sum()

def varianz_x(x,x_mean):
    return (1/len(x))*((x-x_mean)**2).sum()
    
def mittel_varianzgewichtet(val,val_err):
    return (val/(val_err**2)).sum()/(1/(val_err**2)).sum()


# Passt die Rundung von Werten an die Fehler an, erzeugt strings fertig für tabellen
def errorRound(x, xerr):
    new_x = [0]*len(x)
    new_x_err = [0]*len(x)
    if len(x) == len(xerr):
        for i in range(len(x)):

            # #--rundet die Fehler auf erste/zweite signifikante Nachkommastellen--
            # errstring = np.format_float_positional(xerr[i])  
            # k = 0
            # decimalplaces = 0
            # while (errstring[k] == '0' or errstring[k] == '1' or errstring[k]=='.'):
            #     decimalplaces +=1
            #     k +=1
            # print(decimalplaces)


            #--passt nachkommastelle der werte an fehler
            errstring = np.format_float_positional(xerr[i])                 # Fehler als String
            decimalplaces = 0                        # Anzahl der Nachkommastellen
            j = len(errstring) - 1
           
            if xerr[i] != int(xerr[i]):
                while errstring[j] != '.':             # zählt nachkommastellen
                    decimalplaces += 1
                    j -= 1
            else:
                decimalplaces = 0
            numformat = '{:.'+str(decimalplaces)+'f}'
            new_x[i] = round(x[i],decimalplaces)
            new_x[i] = numformat.format(new_x[i])
        
    else:
        print('errorRound: arrays must have same length')

    return new_x