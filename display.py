from matplotlib import pyplot as plt
from sympy.geometry import *
from scipy.spatial import ConvexHull

def display_naive(cells, n):
    colors = ['blue', 'green', 'purple', 'orange', 'red', 'pink', 'gray', 'cyan']
    fig, ax = plt.subplots()
    for i, (point, polygon) in enumerate(cells):
        ax.plot(point.x, point.y, 'ro')
        hull = ConvexHull(polygon)
        vertices = polygon[hull.vertices, :]
        color = colors[i % len(colors)]
        ax.fill(vertices[:, 0], vertices[:, 1], color=color, alpha=0.2)
    ax.autoscale()
    plt.title("Naive Algorithm: n = "+str(n))
    fig.savefig('plot/naive_'+str(n)+'.png')
    plt.show()

def display_dnq(voronoi_dict, points, bound):
    x_min, y_min, x_max, y_max = 0,0,bound,bound
    color = "black"
    for p in points:
        plt.plot(p.x, p.y, 'ro')
    for k,v in voronoi_dict[0].items():
        if isinstance(v,Segment2D):
            plt.plot([v.p1.x,v.p2.x],[v.p1.y,v.p2.y],color = color)
        elif isinstance(v,Ray2D):
            a,b,c = Line2D(v).coefficients
            if b:
                if v.direction.x<0:
                    y=(-c-a*x_min)/b
                    if y<=y_max:
                        if y>=y_min:
                            plt.plot([v.source.x,x_min],[v.source.y,(-c-a*x_min)/b],color = color)
                        else:
                            plt.plot([v.source.x,(-c-b*y_min)/a],[v.source.y,y_min],color = color)
                    else:
                        plt.plot([v.source.x,(-c-b*y_max)/a],[v.source.y,y_max],color = color)
                else:
                    y=(-c-a*x_max)/b
                    if y<=y_max:
                        if y>=y_min:
                            plt.plot([v.source.x,x_max],[v.source.y,(-c-a*x_max)/b],color = color)
                        else:
                            plt.plot([v.source.x,(-c-b*y_min)/a],[v.source.y,y_min],color = color)
                    else:
                        plt.plot([v.source.x,(-c-b*y_max)/a],[v.source.y,y_max],color = color)
            else:
                if v.direction.y<0:
                    plt.plot([v.source.x,v.source.x],[v.source.y,y_min],color = color)
                else:
                    plt.plot([v.source.x,v.source.x],[v.source.y,y_max],color = color)
        elif isinstance(v,Line2D):
            a,b,c = v.coefficients
            if b:
                x1,y1 = x_min,(-c-a*x_min)/b
                if y1>y_max:
                    x1,y1 = (-c-b*y_max)/a,y_max
                elif y1<y_min:
                    x1,y1 = (-c-b*y_min)/a,y_min
                x2,y2 = x_max,(-c-a*x_max)/b
                if y2>y_max:
                    x2,y2 = (-c-b*y_max)/a,y_max
                elif y2<y_min:
                    x2,y2 = (-c-b*y_min)/a,y_min
                plt.plot([x1,x2],[y1,y2],color = color)
            else:
                plt.plot([v.p1.x,v.p1.x],[y_max,y_min],color = color)
        elif isinstance(v,Point2D):
            plt.plot([v.x,],[v.y,],'ro')
    plt.xlim(0,bound)
    plt.ylim(0,bound)
    plt.title("Divide-and-Conquer Algorithm: n = "+str(len(points)))
    plt.savefig('plot/dnq_'+str(len(points))+'.png')
    plt.show()

def display_fortune(points, edges, bound):
    for p in points:
        plt.plot(p.x, p.y, 'ro')
    for edge in edges:
        plt.plot(edge[::2], edge[1::2], color = "black")
    plt.xlim(0, bound)
    plt.ylim(0, bound)
    plt.title("Fortune's Algorithm: n = "+str(len(points)))
    plt.savefig('plot/fortune_'+str(len(points))+'.png')
    plt.show()