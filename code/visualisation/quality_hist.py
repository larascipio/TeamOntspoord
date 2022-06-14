import matplotlib.pyplot as plt
from code.visualisation.output import output

def quality_hist(qualityroutes):
    """
        Create a hist for the best quality routes 
    """
    plt.hist(qualityroutes.keys(), color='g')
    plt.ylabel('Quality')
    plt.savefig('lijnvoeringkwaliteit.png')

    best_qual = max(qualityroutes.keys())
    best_route = qualityroutes[best_qual]
   
    # the best route
    highest = max(qualityroutes)
    highest_route = qualityroutes[highest]
    #output(highest, highest_route)

    # for train in best_route:
    #     print(train._route)
    
    outputfile = 'output.csv'
    output(best_qual, best_route, outputfile)
