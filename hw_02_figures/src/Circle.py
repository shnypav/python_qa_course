from ..src.Figure import Figure
from math import pi


class Circle(Figure):
    name = "Circle"

    def __init__(self, radius):
        if radius < 0:
            raise ValueError("Radius should be >= 0")
        self._radius = radius

    @property
    def radius(self):
        """
        Get the radius of the circle.
        
        @return: Radius of the circle
        """
        return self._radius

    @property
    def area(self):
        """
        Calculate the area of the circle.
        
        @return: Area of the circle (pi * r^2)
        """
        area = pi * (self.radius ** 2)
        return area

    @property
    def perimeter(self):
        """
        Calculate the perimeter (circumference) of the circle.
        
        @return: Perimeter of the circle (2 * pi * r)
        """
        perimeter = 2 * pi * self.radius
        return perimeter

    @property
    def diameter(self):
        """
        Calculate the diameter of the circle.
        
        @return: Diameter of the circle (2 * r)
        """
        return 2 * self.radius

    def __str__(self):
        """
        Return a string representation of the circle.
        
        @return: String representation
        """
        return f"{self.name}(radius={self.radius})"

    def __repr__(self):
        """
        Return a string representation of the circle.
        
        @return: String representation
        """
        return self.__str__()

    def __eq__(self, other):
        """
        Check if two circles are equal.
        
        @param other: Another object to compare with
        @return: True if the other object is a Circle with the same radius
        """
        if not isinstance(other, Circle):
            return False
        return self.radius == other.radius

    def __hash__(self):
        """
        Return a hash value for the circle.
        
        @return: Hash value based on the radius
        """
        return hash(self.radius)

    def __lt__(self, other):
        """
        Check if this circle is less than another circle.
        
        @param other: Another circle to compare with
        @return: True if this circle's radius is less than the other's radius
        """
        if not isinstance(other, Circle):
            raise TypeError("Cannot compare Circle with non-Circle object")
        return self.radius < other.radius

    def __gt__(self, other):
        """
        Check if this circle is greater than another circle.
        
        @param other: Another circle to compare with
        @return: True if this circle's radius is greater than the other's radius
        """
        if not isinstance(other, Circle):
            raise TypeError("Cannot compare Circle with non-Circle object")
        return self.radius > other.radius

    def __le__(self, other):
        """
        Check if this circle is less than or equal to another circle.
        
        @param other: Another circle to compare with
        @return: True if this circle's radius is less than or equal to the other's radius
        """
        if not isinstance(other, Circle):
            raise TypeError("Cannot compare Circle with non-Circle object")
        return self.radius <= other.radius

    def __ge__(self, other):
        """
        Check if this circle is greater than or equal to another circle.
        
        @param other: Another circle to compare with
        @return: True if this circle's radius is greater than or equal to the other's radius
        """
        if not isinstance(other, Circle):
            raise TypeError("Cannot compare Circle with non-Circle object")
        return self.radius >= other.radius

    def add_area(self, figure):
        """
        Add the area of another figure to this circle's area.
        
        @param figure: Another figure object
        @return: The sum of the areas
        """
        if not hasattr(figure, 'area'):
            raise ValueError(f"Cannot add area of {figure} - it's not a valid figure")
        return self.area + figure.area
