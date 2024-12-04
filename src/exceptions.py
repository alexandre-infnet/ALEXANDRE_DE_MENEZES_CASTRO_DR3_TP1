from fastapi import HTTPException


class InvalidItemIdException(HTTPException):
    def __init__(self, item_id: int):
        self.status_code = 400
        self.detail = f"Invalid item_id: {item_id}. The item_id must be a positive integer."
        super().__init__(status_code=self.status_code, detail=self.detail)