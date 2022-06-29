from fastapi import HTTPException, status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

not_found_404 = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="404 not found !",
)

bad_request = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="400 Bad request",
)