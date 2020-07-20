import numpy as np
import matplotlib.pyplot as plt
import proportional_navigation as PN

if __name__ == "__main__":
    pursuer = PN.Body(0,0,0,5)
    target = PN.Body(100,100,50,2)
    options = PN.PNOptions(return_R=True, return_Vc=True)
    dt = 0.01
    N = 3
    
    terminate = False
    t = 0

    log = {'pursuer':{'x':[],'y':[]},'target':{'x':[],'y':[]}}
    while not terminate:
        ret = PN.PN(pursuer,target,N=N,options=options).calculate()
        nL = ret['nL']
        R = ret['R']
        Vc = ret['Vc']

        t = t+dt
        if R < 5 or t > 20:6
            if Vc < 0:
                terminate = True

        psipd = nL/pursuer.V

        pursuer.x += pursuer.xd*dt
        pursuer.y += pursuer.yd*dt
        target.x += target.xd*dt
        target.y += target.yd*dt

        pursuer.psi = pursuer.psi + np.rad2deg(dt*psipd)

        log['pursuer']['x'].append(pursuer.x)
        log['pursuer']['y'].append(pursuer.y)
        log['target']['x'].append(target.x)
        log['target']['y'].append(target.y)
    
    plt.plot(log['pursuer']['y'],log['pursuer']['x'])
    plt.plot(log['target']['y'],log['target']['x'])
    plt.show()