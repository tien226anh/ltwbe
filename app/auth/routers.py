from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from pydash import pick

from app.auth.password import get_password_hash, verify_and_update
from app.user.models import UserChangePasswordModel, UserLoginModel
from app.user.services import get_user_by_id, read_user_by_username, update_user

router = APIRouter()


@router.post("/login")
async def login(body: UserLoginModel, authorize: AuthJWT = Depends()):
    user = await read_user_by_username(body.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    verified, updated_password_hash = verify_and_update(
        body.password, user["hashed_password"]
    )

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    # Update password has to a more robust one if needed
    if updated_password_hash is not None:
        await update_user(user["_id"], {"hashed_password": user["hashed_password"]})

    access_token = authorize.create_access_token(subject=str(user["_id"]))
    refresh_token = authorize.create_refresh_token(subject=str(user["_id"]))

    detail = pick(user, "role", "username", "full_name", "avatar_url")

    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)

    return HTTPException(status_code=status.HTTP_200_OK, detail=detail)


@router.put("/change-password")
async def change_user_password(
    body: UserChangePasswordModel, authorize: AuthJWT = Depends()
):
    authorize.jwt_required()
    user_id = ObjectId(authorize.get_jwt_subject())
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    verified = verify_and_update(body.password, user["hashed_password"])

    if not verified or verified[0] is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    # TODO: check schemas password
    hashed_password = get_password_hash(body.new_password)
    try:
        await update_user(user_id, {"hashed_password": hashed_password})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password is valid",
        )

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=None)


@router.post("/refresh")
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_user)

    authorize.set_access_cookies(new_access_token)
    return HTTPException(status_code=status.HTTP_200_OK)


@router.delete("/logout")
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    authorize.unset_jwt_cookies()
    return HTTPException(status_code=status.HTTP_200_OK)
