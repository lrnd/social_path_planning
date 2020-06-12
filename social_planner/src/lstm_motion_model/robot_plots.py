import numpy as np
from numpy import empty
import matplotlib.pyplot as plt

def plot_path_with_predictions(ground_truth, prediction, rbt_path):
    truths= ground_truth.cpu().numpy()
    predictions= prediction.cpu().numpy()
    steps = len(truths)
    num_agents = len(truths[0])

    ##need to flip from steps, num_agents, dims to
    #                   num_agents, steps, dims
    #add rbt is as last to plot, truth/pred the same
    truths_flip = empty([num_agents+1, steps, 2])
    pred_flip= empty([num_agents+1, steps, 2])
    #for p in range(len(truths_org)):
    for s in range(steps):
        for p in range(num_agents+1):
            if p == num_agents:
               truths_flip[p][s] = rbt_path[s] 
               pred_flip[p][s] = rbt_path[s] 
            else:
               truths_flip[p][s] = truths[s][p]
               pred_flip[p][s] = predictions[s][p]

    plots = []
    plt.clf()
    plt.gcf().canvas.mpl_connect('key_release_event',
                                 lambda event: [exit(0) if event.key == 'escape' else None])
    ax = None
    fig,ax = plt.subplots()
    #for pedestrians
    for p in range(num_agents):
        marker, = ax.plot(
            [], [], 'o', linewidth=3.0)
        predicted, = ax.plot(
            [], [], '-', linewidth=2.0, color=marker.get_color())
        truth, = ax.plot(
            [], [], ':', linewidth=3.0, color=marker.get_color())
        plots.append((marker, predicted, truth ))
        

    ##for rbt
    marker, = ax.plot(
        [], [], 'x', linewidth=3.0, color='black')
    path, = ax.plot(
        [], [], '-', linewidth=2.0, color=marker.get_color())

    plots.append((marker,path,path))

    ax.legend(('pedestrian', 'predicted reactions', 'predicted truths'))
    #now plot the thing
    for plot, true, pred in zip(plots, truths_flip, pred_flip):
        plot[0].set_data(true[0,0], true[0,1])
        plot[2].set_data(pred[:,0], pred[:,1])
        plot[1].set_data(true[:,0], true[:,1])

    plt.suptitle('Predictions Vs Reactions', fontsize=12)
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    plt.axis([-13,13,-13,13])
    plt.grid(True,which='major', alpha=1)
    #plt.axis("equal")
    plt.pause(0.1)
    #plt.draw()
    plt.show()




def plot_chosen_path(prediction, rbt_path):
    predictions= prediction.cpu().numpy()
    steps = len(predictions)
    len_rbt_p = len(rbt_path)
    num_agents = len(predictions[0])

    ##need to flip from steps, num_agents, dims to
    #                   num_agents, steps, dims
    #add rbt is as last ped to plot, truth/pred the same
    pred_flip= empty([num_agents+1, steps, 2])
    rbt_p= empty([1, len_rbt_p, 2])
    for s in range(steps):
        for p in range(num_agents+1):
            if p == num_agents:
               pred_flip[p][s] = rbt_path[s] 
            else:
               pred_flip[p][s] = predictions[s][p]

    for s in range(len_rbt_p):
       rbt_p[0][s] = rbt_path[s] 

    plots = []
    plot_rbt = []
    plt.clf()
    plt.gcf().canvas.mpl_connect('key_release_event',
                                 lambda event: [exit(0) if event.key == 'escape' else None])
    ax = None
    fig,ax = plt.subplots()
    ax.legend(('pedestrian', 'predictions', 'rbt path'))

    ##for rbt outside of future reaction (rest of path)
    path, = ax.plot(
        [], [], '-', linewidth=2.0, color='grey')
    plot_rbt.append(path)

    #for pedestrians
    for p in range(num_agents):
        marker, = ax.plot(
            [], [], 'o', linewidth=3.0)
        predicted, = ax.plot(
            [], [], '-', linewidth=2.0, color=marker.get_color())

        plots.append((marker, predicted))
        

    ##for rbt in future reaction steps
    marker, = ax.plot(
        [], [], 'x', linewidth=3.0, color='black')
    path, = ax.plot(
        [], [], '-', linewidth=2.0, color=marker.get_color())
    plots.append((marker, path))



    for plot, rbt in zip(plot_rbt, rbt_p):
        plot.set_data(rbt[:,0], rbt[:,1])

    #now plot the peds with reactive rbt path
    for plot, pred in zip(plots, pred_flip):
        plot[0].set_data(pred[0,0], pred[0,1])
        plot[1].set_data(pred[:,0], pred[:,1])


    plt.suptitle('Final Path and Pedestrian State', fontsize=12)
    plt.xlabel('X(m)')
    plt.ylabel('Y(m)')
    plt.axis([-13,13,-13,13])
    plt.grid(True,which='major', alpha=1)
    #plt.axis("equal")
    #plt.pause(5)
    #plt.draw()
    plt.show()
    
