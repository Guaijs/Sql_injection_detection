def simplePloter():
    '''
    不适用包，简单绘制
    '''
    N=100
    theta=np.linspace(0.0,2*np.pi,N,endpoint=False)
    radii=10*np.random.rand(N)
    width=np.pi/4*np.random.rand(N)
    ax=plt.subplot(111, projection='polar')
    bars=ax.bar(theta,radii,width=width,bottom=0.0)
    for r, bar in zip(radii,bars):
        bar.set_facecolor(plt.cm.jet(r/10.))
        bar.set_alpha(0.8)
    plt.savefig('simplePloter_windrose.png') 
    plt.show()