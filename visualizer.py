import numpy as np
import matplotlib.pyplot as plt


def compare_models(type, size, density, n_tests):
    '''
        Function to make graphs of either success rates of CBS vs PRIMAL or duration of CBS vs PRIMAL
        Input:
            type: either success rate or duration
            size: world size (10, 20, 40)
            density: obstacle density (.1, .2, .3)
            n_tests: number of tests run for experiments
    '''
    for i, alg in enumerate(["cbs", "primal"]):
        filename = './stats/{}_{}_size{}_den{}_ntests{}.npy'.format(alg, type, size, density, n_tests)
        data = np.load(filename)
        #print(data)
        n_agents = [2**(2+i) for i in range(len(data))]
        plt.plot(n_agents, data, label=alg)

    title = "Average computing time" if type == "duration" else "Success rate"
    plt.xticks(n_agents)
    plt.title("{} with world size = {} and density = {}".format(title, size, density))
    plt.legend()
    plt.savefig("./stats/{}_size{}_den{}_ntests{}.jpg".format(type, size, density, n_tests))
    plt.show()


if __name__ == '__main__':
    # filename = './stats/{}_suc_rate_size{}_den{}_ntests{}.npy'.format('cbs', '20', '0.1', '50')
    # np.save(filename, [1.00, .98, .60, 0])
    # filename = './stats/{}_suc_rate_size{}_den{}_ntests{}.npy'.format('cbs', '40', '0.1', '50')
    # np.save(filename, [1.00, .78, .14, 0])

    # filename = './stats/{}_duration_size{}_den{}_ntests{}.npy'.format('cbs', '20', '0.1', '50')
    # np.save(filename, [1.59, 9.46, 53.75, 0])

    # filename = './stats/{}_duration_size{}_den{}_ntests{}.npy'.format('cbs', '40', '0.1', '50')
    # np.save(filename, [15.94, 36.94, 82.73, 0])

    compare_models("suc_rate", 20, 0.1, 50)
    compare_models("duration", 20, 0.1, 50)
