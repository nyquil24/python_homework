import math 
class Point: 
    def __init__(self,x,y): 
        self.x = float(x)
        self.y = float(y)
    
    def __eq__(self,other): 
        if isinstance(other, Point): 
            return (self.x, self.y) == (other.x, other.y)
        return NotImplemented
    
    def __str__(self): 
        return f"Point(x={self.x}, y={self.y})"
    
    def distance_to(self, other: "Point") -> float: 
        return math.hypot(self.x - other.x, self.y - other.y)

class Vector(Point): 
    def __str__(self): 
        return f"Vector<{self.x}, {self.y}>"
    
    def __add__(self, other): 
        if isinstance(other, Vector): 
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented