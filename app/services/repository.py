class RepositoryService:
    def __init__(self):
        self.repository = Repository()

    def get_repository(self):
        return self.repository
