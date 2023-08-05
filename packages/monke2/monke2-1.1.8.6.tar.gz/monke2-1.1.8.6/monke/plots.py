import matplotlib.pyplot as plt

errbar=[7,5,1,1,'x']

def plots(figsize=(6,4)):
    fig, ax = plt.subplots(figsize=figsize,dpi=120)
    return ax

def errorbar(ax, x_val,y_val,y_err,x_err=[0],errbar=[7,5,1,1,'x'],color='tab:red',line='',label='Daten',size=(6,4)):
    if x_err == [0]:
        x_err = [0]*len(x_val)
    
    ax.errorbar(x_val, y_val,color=color,marker=errbar[4],markersize=errbar[0],linestyle=line,
    yerr=y_err, xerr=x_err,label=label,capsize=errbar[1], elinewidth=errbar[2])

    return 

def style():
    plt.rcParams['lines.linestyle'] = ''