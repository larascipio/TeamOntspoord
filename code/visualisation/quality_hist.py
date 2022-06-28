import matplotlib.pyplot as plt
from statistics import mean

def quality_hist(qualityroutes):
    """
    Create a histogram for the routes.
    """
    plt.figure(figsize=(80, 15))
    font = {'weight' : 'bold',
            'size'   : 50}
    plt.rc('font', **font)
    plt.hist(qualityroutes, range=[0, 10000], color='g', bins=100)
    plt.xlim([0, 10000])
    plt.xlabel('Quality')
    plt.ylabel('Number of runs')
    plt.title(f'Quality for {len(qualityroutes)} runs - Mean quality: {mean(qualityroutes)}')
    plt.savefig('./code/railnet_quality_histogram.png')


