import asyncio
from typing import List, Annotated

from fastapi import Path
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.api_v1.users.schemas.schemas_order import OrderCreate
from src.core.config import DBConfigurer, IntegrityError
from src.api_v1.users.schemas import (
    UserUpdate, UserCreate, UserPartialUpdate,
    ProfileUpdate, ProfileCreate, ProfilePartialUpdate,
    PostUpdate, PostCreate, PostPartialUpdate,
)

from src.core.models import User, Profile, Post, Order


async def get_users(session: AsyncSession) -> List[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    user: User | None = await session.get(User, user_id)
    return user


async def create_user(session: AsyncSession, instance: UserCreate) -> User:
    user = User(**instance.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(
        session: AsyncSession,
        user: User,
        instance: UserUpdate | UserPartialUpdate,
        is_partial: bool = False
) -> User:
    for key, val in instance.model_dump(
        exclude_unset=is_partial
    ).items():
        setattr(user, key, val)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(
        session: AsyncSession, user: User
) -> None:
    await session.delete(user)
    await session.commit()


async def get_user_by_username(
    username: Annotated[str, Path],
    session: AsyncSession
) -> User | None:
    stmt = select(User).where(User.username == username).order_by(User.id)
    user: User | None = await session.scalar(stmt)
    return user


async def get_user_joined(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id).options(joinedload(User.profile)).options(joinedload(User.posts))
    user: User | None = await session.scalar(stmt)
    return user


async def create_user_profile(
        user_id: Annotated[int, Path],
        session: AsyncSession,
        instance: ProfileCreate,
) -> Profile | None:

    # user: User | None = await get_user_joined(session=session, user_id=user_id)
    # if not user or user.profile:
    #     return None
    profile: Profile = Profile(**instance.model_dump(), user_id=user_id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return profile


async def create_user_post(
        user_id: Annotated[int, Path],
        session: AsyncSession,
        instance: PostCreate,
) -> Post | None:

    # user: User | None = await get_user(session=session, user_id=user_id)
    # if not user:
    #     return None
    post: Post = Post(**instance.model_dump(), user_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


async def get_users_posts_and_profile(
        session: AsyncSession
):
    stmt = select(User).options(
        joinedload(User.profile),
        selectinload(User.posts)
    ).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars()

    for user in users:
        print('----', user)
        print('    ', user.profile)
        for post in user.posts:
            print('          ', post)


async def get_profile_user_posts(
        session: AsyncSession
):
    stmt = select(Profile).options(
        joinedload(Profile.user).selectinload(User.posts)
    ).order_by(Profile.id)
    result: Result = await session.execute(stmt)
    profiles = result.scalars()

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

    for profile in profiles:
        print('----', profile)
        print('    ', profile.user)
        for post in profile.user.posts:
            print('          ', post)


async def get_user_posts(
        session: AsyncSession
):
    stmt = select(User).options(joinedload(User.posts, innerjoin=True)).order_by(User.id)
    # stmt = select(User).options(joinedload(User.posts)).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.unique().scalars()
    for user in users:
        print(user)
        for post in user.posts:
            print('    ', post)


async def get_post_users(
        session: AsyncSession
):
    stmt = (select(Post).
            options(joinedload(Post.user, innerjoin=True)).
            # join(User, Post.user_id == User.id, isouter=True, full=True).
            order_by(Post.user_id))
    result: Result = await session.execute(stmt)
    lines = result.unique().fetchall()
    for line in lines:
        print(line)


async def main_relations(session: AsyncSession):
    # print(await create_user(session=session, instance=UserCreate(username='Ivanide')))
    # print(await create_user(session=session, instance=UserCreate(username='Han')))

    # print(await get_user_by_username(session=session, username='Ivan'))
    # print(await get_user_by_username(session=session, username='Ivan22'))

    # prof1 = await create_user_profile(user_id=1, session=session, instance=ProfileCreate(
    #     firstname='Senia', lastname='Durak', bio="Was born"
    # ))

    # post = await create_user_post(user_id=2, session=session, instance=PostCreate(
    #     title='Understanding', review='I understand nothing'))
    # user = await get_user_joined(session=session, user_id=1)

    # print(user)
    # print(user.profile)
    # print(user.posts)

    # await get_users_posts_and_profile(session=session)

    # profiles = await get_profile_user_posts(session=session)

    posts = await get_user_posts(session=session)
    print()
    print()

    posts = await get_post_users(session=session)


async def create_order(session: AsyncSession, instance: OrderCreate):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", instance.model_dump())
    order: Order = Order(**instance.model_dump())
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def demo_m2m(session: AsyncSession):
    print(
        await create_order(
            session=session, instance=OrderCreate(promocode='123')
        )
    )
    print(
        await create_order(
            session=session, instance=OrderCreate(promocode=None)
        )
    )


async def main():
    async with DBConfigurer.Session() as session:
        # await main_relations(session)

        await demo_m2m(session)



if __name__ == "__main__":

    asyncio.run(main())

