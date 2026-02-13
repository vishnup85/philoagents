class PhilosopherStyleNotFoundException(ValueError):
    def __init__(self, philosopher_id: str):
        self.message = f"Philosopher style not found for ID: {philosopher_id}"
        super().__init__(self.message)
