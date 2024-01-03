from finkchlib.vector import Vector2

# Oversees the space and time of a thing
class Spacetime:
    def __init__(self, step, position: Vector2 = Vector2(), velocity: Vector2 = Vector2(), acceleration: Vector2 = Vector2()) -> None:
        self.step: int = step

        self.position: Vector2 = position
        self.velocity: Vector2 = velocity
        self.acceleration: Vector2 = acceleration

        self.acceleration_preview: Vector2 = Vector2()
    
    # Updates the space and time
    def __call__(self):

        # Updates postion and velocity
        self.velocity += self.acceleration * self.step
        self.position += self.velocity * self.step

        # Resets acceleration
        self.acceleration_preview: Vector2 = self.acceleration
        self.acceleration: Vector2 = Vector2()

    # Applies a force to the craft
    def force(self, mass, amount: Vector2) -> None:
        self.acceleration += amount / mass