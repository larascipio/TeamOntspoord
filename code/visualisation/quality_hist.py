import matplotlib.pyplot as plt
from code.visualisation.output import output

# def quality_hist(qualityroutes, best_quality, best_route):
def quality_hist(qualityroutes):
    """
        Create a hist for the best quality routes 
    """
    plt.hist(qualityroutes, color='g', bins=100)
    plt.xlabel('Quality')
    plt.ylabel('Number of runs')
    plt.title(f'Quality for {len(qualityroutes)} runs')
    plt.savefig('./code/lijnvoeringkwaliteit.png')

    # best_qual = max(qualityroutes.keys())
    # best_route = qualityroutes[best_qual]

    # for train in best_route:
    #     print(train._route)
    
    # outputfile = 'output.csv'
    # output(best_quality, best_route.get_trains(), outputfile)
