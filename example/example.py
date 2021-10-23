import numpy as np
try:
    import matplotlib.pyplot as plt
    plt_found = True
except ModuleNotFoundError:
    plt_found = False
import proportional_navigation as PN

if __name__ == "__main__":
    pursuer = PN.HeadingVelocity(0,0,0,5)
    target = PN.HeadingVelocity(100,100,50,2)
    options = PN.PNOptions(return_R=True, return_Vc=True)
    dt = 0.01
    N = 3
    
    terminate = False
    t = 0

    log = {'pursuer':{'x':[],'y':[]},'target':{'x':[],'y':[]}}
    log_v = {'pursuer':{'x':[], 'y':[]}, 'target':{'x':[],'y':[]}}
    while not terminate:
        ret = PN.PN(pursuer,target,N=N,options=options).calculate()
        nL = ret['nL']
        R = ret['R']
        Vc = ret['Vc']

        t = t+dt
        print(R)
        if R < 7 or t > 40:
            if Vc < 0:
                terminate = True

        psipd = nL/pursuer.V

        pursuer.x += pursuer.xd*dt
        pursuer.y += pursuer.yd*dt
        target.x += target.xd*dt
        target.y += target.yd*dt

        pursuer.psi = pursuer.psi + np.rad2deg(dt*psipd)
        target.psi = target.psi + np.rad2deg(dt*0.01)
        
        log['pursuer']['x'].append(pursuer.x)
        log['pursuer']['y'].append(pursuer.y)
        log['target']['x'].append(target.x)
        log['target']['y'].append(target.y)
    
        log_v['pursuer']['x'].append(pursuer.xd)
        log_v['pursuer']['y'].append(pursuer.yd)
        log_v['target']['x'].append(target.xd)
        log_v['target']['y'].append(target.yd)
    
    log_short = {'pursuer':{'pos':{'x':[], 'y':[]}, 'vel':{'x':[], 'y':[]}},\
        'target':{'pos':{'x':[], 'y':[]},'vel':{'x':[], 'y':[]}}}

    for i in range(1, len(log['pursuer']['x']), 100):
        log_short['pursuer']['pos']['x'].append(log['pursuer']['x'][i])
        log_short['pursuer']['pos']['y'].append(log['pursuer']['y'][i])
        log_short['pursuer']['vel']['x'].append(log_v['pursuer']['x'][i])
        log_short['pursuer']['vel']['y'].append(log_v['pursuer']['y'][i])

        log_short['target']['pos']['x'].append(log['target']['x'][i])
        log_short['target']['pos']['y'].append(log['target']['y'][i])
        log_short['target']['vel']['x'].append(log_v['target']['x'][i])
        log_short['target']['vel']['y'].append(log_v['target']['y'][i])
    if plt_found:
        # plt.plot(log['pursuer']['y'],log['pursuer']['x'])
        # plt.plot(log['target']['y'],log['target']['x'])
        # plt.show()

        plt.plot(log['pursuer']['y'],log['pursuer']['x'])
        plt.quiver(log_short['pursuer']['pos']['y'], \
            log_short['pursuer']['pos']['x'],\
                  np.array(log_short['pursuer']['vel']['y']),\
                      np.array(log_short['pursuer']['vel']['x'] ))
        plt.plot(log['target']['y'],log['target']['x'])
        plt.quiver(log_short['target']['pos']['y'], \
            log_short['target']['pos']['x'],\
                  np.array(log_short['target']['vel']['y']),\
                      np.array(log_short['target']['vel']['x'] ))
        plt.show()
    else:
        print("matplotlib.pyplot was not found in the env. Plot of xy graph will not be shown")
