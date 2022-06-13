    
def make_hist():   
    plt.hist(qualityroutes.keys(), color='g')
    plt.ylabel('Quality')
    plt.savefig('lijnvoeringkwaliteit.png')

    # the best route
    highest = max(qualityroutes)
    output(highest, qualityroutes[highest])