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

    # for train in best_route:
    #     print(train._route)
    
    outputfile = 'output.csv'
    output(best_qual, best_route.get_trains(), outputfile)
